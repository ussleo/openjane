"""
OpenJane · FastAPI server
Sirve la landing estática + endpoints de análisis en tiempo real.

Endpoints:
  GET  /                    → landing page (docs/index.html)
  GET  /static/*            → assets de docs/
  POST /api/regime          → régimen de mercado global
  POST /api/microstructure  → microestructura de un ticker
  POST /api/statarb         → stat-arb entre dos tickers
  GET  /api/health          → healthcheck

Seguridad:
  - Tickers validados con regex estricto (solo alfanumérico + . -)
  - API keys nunca se loguean ni almacenan
  - Rate limiting por IP real (X-Forwarded-For → fallback client)
  - Clientes HTTP instanciados por request (thread-safe, sin env vars globales)
  - Timeout de 10s en todas las llamadas externas
"""

import os, math, time, re, json
from pathlib import Path
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import urllib.request, urllib.parse
from datetime import datetime, timedelta

# ── paths ────────────────────────────────────────────────────────────────────
BASE  = Path(__file__).parent.parent
DOCS  = BASE / "docs"

import sys
sys.path.insert(0, str(BASE))

app = FastAPI(title="OpenJane", docs_url=None, redoc_url=None)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ussleo.github.io", "https://openjane.onrender.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# ── rate limit ────────────────────────────────────────────────────────────────
_hits: dict = defaultdict(list)
RATE_WINDOW = 60
RATE_LIMIT  = 10

def _real_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def check_rate(ip: str):
    now = time.time()
    _hits[ip] = [t for t in _hits[ip] if now - t < RATE_WINDOW]
    if len(_hits[ip]) >= RATE_LIMIT:
        raise HTTPException(429, "Too many requests — espera un momento.")
    _hits[ip].append(now)

# ── validación de tickers ─────────────────────────────────────────────────────
TICKER_RE = re.compile(r'^[A-Z0-9.\-]{1,12}$')

def validate_ticker(raw: str) -> str:
    """Sanitiza y valida un ticker. Lanza 422 si el formato es inválido."""
    t = raw.strip().upper()[:12]
    if not TICKER_RE.match(t):
        raise HTTPException(422, f"Ticker inválido: '{raw}'. Solo letras, números, puntos y guiones (máx 12 caracteres).")
    return t

# ── clientes HTTP thread-safe (instanciados por request, no globales) ─────────
MASSIVE_BASE = "https://api.massive.com"
EODHD_BASE   = "https://eodhd.com/api"

def _massive_get(key: str, endpoint: str, params: dict = None) -> dict:
    """GET a Massive.com con la key del usuario (no env var global)."""
    if not key or len(key) > 200:
        raise HTTPException(422, "Massive API key inválida.")
    url = f"{MASSIVE_BASE}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {key}", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise HTTPException(502, f"Massive.com error {e.code}: {e.reason}")
    except Exception as e:
        raise HTTPException(502, f"Massive.com no disponible: {str(e)[:80]}")

def _eodhd_get(key: str, endpoint: str, params: dict = None) -> dict | list:
    """GET a EODHD con la key del usuario (no env var global)."""
    if not key or len(key) > 200:
        raise HTTPException(422, "EODHD API key inválida.")
    p = {"api_token": key, "fmt": "json"}
    if params:
        p.update(params)
    url = f"{EODHD_BASE}{endpoint}?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise HTTPException(502, f"EODHD error {e.code}: {e.reason}")
    except Exception as e:
        raise HTTPException(502, f"EODHD no disponible: {str(e)[:80]}")

# ── helpers de análisis (puros, sin estado global) ────────────────────────────
def _corr(a, b):
    n = len(a); ma = sum(a)/n; mb = sum(b)/n
    num = sum((a[i]-ma)*(b[i]-mb) for i in range(n))
    da  = math.sqrt(sum((x-ma)**2 for x in a))
    db  = math.sqrt(sum((x-mb)**2 for x in b))
    return round(num/(da*db), 4) if da*db else 0

def _beta_zscore(a, b):
    n = len(a); ma = sum(a)/n; mb = sum(b)/n
    beta   = sum((a[i]-ma)*(b[i]-mb) for i in range(n)) / sum((x-mb)**2 for x in b)
    spread = [a[i] - beta*b[i] for i in range(n)]
    ms     = sum(spread)/n
    std    = math.sqrt(sum((s-ms)**2 for s in spread)/n)
    zscore = round((spread[-1]-ms)/std, 3) if std else 0
    return round(beta,4), round(ms,4), round(std,4), zscore, spread

def _halflife(sp):
    n = len(sp)
    y = [sp[i]-sp[i-1] for i in range(1, n)]
    x = sp[:-1]
    mx = sum(x)/len(x); my = sum(y)/len(y)
    b = sum((x[i]-mx)*(y[i]-my) for i in range(len(x))) / sum((v-mx)**2 for v in x)
    return round(-math.log(2)/b, 1) if b and b < 0 else None

# ── funciones de datos (thread-safe: reciben key como parámetro) ──────────────
def _moving_averages(eodhd_key: str, ticker: str) -> dict:
    data = _eodhd_get(eodhd_key, f"/technical/{ticker}", {
        "function": "SMA", "period": 200, "order": "d", "limit": 1
    })
    if not isinstance(data, list) or not data:
        raise HTTPException(502, f"Sin datos de MA200 para {ticker}")
    ma200 = data[0].get("sma") or data[0].get("value") or data[0].get("sma_200")

    data50 = _eodhd_get(eodhd_key, f"/technical/{ticker}", {
        "function": "SMA", "period": 50, "order": "d", "limit": 1
    })
    ma50 = (data50[0].get("sma") or data50[0].get("value")) if isinstance(data50, list) and data50 else None

    eod = _eodhd_get(eodhd_key, f"/eod/{ticker}", {"order": "d", "limit": 1})
    last_close = (eod[0]["adjusted_close"] if isinstance(eod, list) and eod else None)

    trend = "insuficiente"
    if last_close and ma200:
        trend = "alcista" if last_close > ma200 else "bajista"
        if ma50 and abs(last_close/ma200 - 1) < 0.02:
            trend = "transicion"

    return {"last_close": last_close, "ma50": ma50, "ma200": ma200, "trend": trend}

def _historical_volatility(eodhd_key: str, ticker: str, window: int = 20) -> dict:
    days_needed = window * 2
    date_from = (datetime.utcnow() - timedelta(days=days_needed)).strftime("%Y-%m-%d")
    prices_raw = _eodhd_get(eodhd_key, f"/eod/{ticker}", {
        "order": "d", "limit": days_needed, "from": date_from
    })
    if not isinstance(prices_raw, list) or len(prices_raw) < window + 1:
        return {"error": f"Datos insuficientes ({len(prices_raw) if isinstance(prices_raw, list) else 0} días)"}
    closes = [p["adjusted_close"] for p in reversed(prices_raw[-window-1:])]
    returns = [math.log(closes[i]/closes[i-1]) for i in range(1, len(closes))]
    mr = sum(returns)/len(returns)
    variance = sum((r-mr)**2 for r in returns)/(len(returns)-1)
    hv_daily = math.sqrt(variance)
    return {
        "hv_daily_pct": round(hv_daily*100, 3),
        "hv_annual_pct": round(hv_daily*math.sqrt(252)*100, 2),
        "window": window,
    }

def _yield_curve(eodhd_key: str) -> dict:
    us10 = _eodhd_get(eodhd_key, "/eod/US10Y.INDX", {"period": "d", "order": "d", "limit": 1})
    us2  = _eodhd_get(eodhd_key, "/eod/US2Y.INDX",  {"period": "d", "order": "d", "limit": 1})
    y10  = us10[0]["adjusted_close"] if isinstance(us10, list) and us10 else None
    y2   = us2[0]["adjusted_close"]  if isinstance(us2,  list) and us2  else None
    spread = round(y10 - y2, 3) if y10 and y2 else None
    label = ("Normal / positiva" if spread and spread > 0.5
             else "Plana" if spread and -0.5 <= spread <= 0.5
             else "Invertida — alerta recesión" if spread else "Sin datos")
    return {"us10y": y10, "us2y": y2, "spread_10y_2y": spread, "yield_curve_label": label}

def _prev_close_massive(massive_key: str, ticker: str) -> dict:
    data = _massive_get(massive_key, f"/v2/aggs/ticker/{ticker}/prev")
    results = data.get("results", [])
    if not results:
        return {"symbol": ticker, "error": "Sin datos"}
    r = results[0]
    ts = r.get("t", 0)
    date_str = datetime.utcfromtimestamp(ts/1000).strftime("%Y-%m-%d") if ts else "N/A"
    return {"symbol": ticker, "close": r.get("c"), "open": r.get("o"),
            "high": r.get("h"), "low": r.get("l"),
            "volume": int(r.get("v",0)), "vwap": r.get("vw"), "date": date_str}

def _volume_profile_massive(massive_key: str, ticker: str, days: int = 20) -> dict:
    date_to   = datetime.utcnow().strftime("%Y-%m-%d")
    date_from = (datetime.utcnow() - timedelta(days=days+10)).strftime("%Y-%m-%d")
    data = _massive_get(massive_key, f"/v2/aggs/ticker/{ticker}/range/1/day/{date_from}/{date_to}",
                        {"adjusted": "true", "sort": "asc", "limit": days})
    results = data.get("results", [])
    if not results:
        return {"symbol": ticker, "error": "Sin datos de volumen"}
    volumes = [r.get("v", 0) for r in results]
    adv = int(sum(volumes)/len(volumes)) if volumes else 0
    last = int(volumes[-1]) if volumes else 0
    ratio = round(last/adv, 2) if adv else None
    signal = ("Volumen extremo" if ratio and ratio > 2
              else "Volumen alto" if ratio and ratio > 1.5
              else "Volumen bajo" if ratio and ratio < 0.5
              else "Neutral")
    return {"symbol": ticker, "adv": adv, "last_session_volume": last,
            "volume_ratio": ratio, "flow_signal": signal}

def _historical_prices_eodhd(eodhd_key: str, ticker: str, days: int = 365) -> list:
    date_from = (datetime.utcnow() - timedelta(days=int(days*1.5))).strftime("%Y-%m-%d")
    data = _eodhd_get(eodhd_key, f"/eod/{ticker}", {
        "order": "a", "limit": days, "from": date_from
    })
    return data if isinstance(data, list) else []

# ── modelos de request ────────────────────────────────────────────────────────
class KeysBase(BaseModel):
    massive_key: str
    eodhd_key:   str

    @field_validator("massive_key", "eodhd_key")
    @classmethod
    def key_not_empty(cls, v):
        v = v.strip()
        if not v or len(v) < 8 or len(v) > 200:
            raise ValueError("API key inválida (longitud fuera de rango)")
        return v

class TickerRequest(KeysBase):
    ticker: str

    @field_validator("ticker")
    @classmethod
    def ticker_clean(cls, v):
        t = v.strip().upper()[:12]
        if not TICKER_RE.match(t):
            raise ValueError(f"Ticker inválido: '{v}'")
        return t

class PairRequest(KeysBase):
    ticker_a: str
    ticker_b: str

    @field_validator("ticker_a", "ticker_b")
    @classmethod
    def tickers_clean(cls, v):
        t = v.strip().upper()[:12]
        if not TICKER_RE.match(t):
            raise ValueError(f"Ticker inválido: '{v}'")
        return t

class PortfolioSnapshotReq(BaseModel):
    eodhd_key: str
    tickers: list[str]

    @field_validator("eodhd_key")
    @classmethod
    def key_ok(cls, v):
        v = v.strip()
        if not v or len(v) < 8 or len(v) > 200:
            raise ValueError("EODHD API key inválida")
        return v

    @field_validator("tickers")
    @classmethod
    def tickers_ok(cls, v):
        if not v or len(v) > 10:
            raise ValueError("Envía entre 1 y 10 tickers")
        cleaned = []
        for t in v:
            t2 = t.strip().upper()[:12]
            if not TICKER_RE.match(t2):
                raise ValueError(f"Ticker inválido: '{t}'")
            cleaned.append(t2)
        return cleaned

# ── endpoints ─────────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "OpenJane"}

@app.post("/api/regime")
def regime(req: KeysBase, request: Request):
    check_rate(_real_ip(request))
    try:
        spy = _moving_averages(req.eodhd_key, "SPY")
        hv  = _historical_volatility(req.eodhd_key, "SPY", window=20)
        yc  = _yield_curve(req.eodhd_key)
        score = sum([
            bool(spy.get("last_close") and spy.get("ma200") and spy["last_close"] > spy["ma200"]),
            bool(spy.get("ma50") and spy.get("ma200") and spy["ma50"] > spy["ma200"]),
            bool(yc.get("spread_10y_2y") and yc["spread_10y_2y"] > 0),
            bool(hv.get("hv_annual_pct") and hv["hv_annual_pct"] < 20),
        ])
        labels = {4:"ALCISTA FUERTE", 3:"ALCISTA MODERADO", 2:"MIXTO",
                  1:"BAJISTA MODERADO", 0:"BAJISTA / CRISIS"}
        return {"spy": spy, "hv_20d": hv, "yield_curve": yc,
                "score": score, "regime": labels.get(score, "—")}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e)[:200])

@app.post("/api/microstructure")
def microstructure(req: TickerRequest, request: Request):
    check_rate(_real_ip(request))
    try:
        ticker = req.ticker
        pc  = _prev_close_massive(req.massive_key, ticker)
        vol = _volume_profile_massive(req.massive_key, ticker)
        tr  = _moving_averages(req.eodhd_key, ticker)
        hv  = _historical_volatility(req.eodhd_key, ticker, window=20)
        intraday = round((pc["high"]-pc["low"])/pc["close"]*100, 3) if pc.get("close") else None
        liq = ("ALTA" if intraday and intraday < 1.0
               else "NORMAL" if intraday and intraday < 3.0
               else "REDUCIDA" if intraday else "Sin datos")
        return {"ticker": ticker, "price": pc, "volume": vol, "trend": tr, "hv_20d": hv,
                "intraday_range_pct": intraday, "liquidity": liq,
                "transaction_cost_pct": round(intraday*0.4, 3) if intraday else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e)[:200])

@app.post("/api/statarb")
def statarb(req: PairRequest, request: Request):
    check_rate(_real_ip(request))
    try:
        ta, tb = req.ticker_a, req.ticker_b
        if ta == tb:
            raise HTTPException(422, "Los dos tickers deben ser diferentes.")
        pa = [d["adjusted_close"] for d in _historical_prices_eodhd(req.eodhd_key, ta, days=365)]
        pb = [d["adjusted_close"] for d in _historical_prices_eodhd(req.eodhd_key, tb, days=365)]
        n  = min(len(pa), len(pb))
        if n < 30:
            raise HTTPException(422, f"Datos insuficientes para el análisis ({n} días comunes).")
        pa = pa[-n:]; pb = pb[-n:]
        co = _corr(pa, pb)
        beta, mean_sp, std_sp, z, spreads = _beta_zscore(pa, pb)
        hl = _halflife(spreads)
        signal = ("ENTRADA LARGA"  if z < -2.0
                  else "ENTRADA CORTA" if z >  2.0
                  else "MONITOREAR"    if abs(z) >= 1.5
                  else "NEUTRAL")
        return {"pair": f"{ta}/{tb}", "n_days": n, "correlation": co, "beta": beta,
                "spread_mean": mean_sp, "spread_std": std_sp, "zscore": z,
                "halflife_days": hl, "entry_long": round(mean_sp-2*std_sp, 2),
                "entry_short": round(mean_sp+2*std_sp, 2), "stop": round(3.5*std_sp, 2),
                "exit_target": round(mean_sp, 2), "signal": signal}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e)[:200])

@app.post("/api/portfolio-snapshot")
def portfolio_snapshot(req: PortfolioSnapshotReq, request: Request):
    """
    Devuelve el último precio de cierre EOD para cada ticker.
    Usado por el Teatro de Operaciones para abrir y evaluar posiciones.
    Solo necesita EODHD key (no Massive).
    """
    check_rate(_real_ip(request))
    prices = {}
    errors = {}
    for ticker in req.tickers:
        try:
            eod = _eodhd_get(req.eodhd_key, f"/eod/{ticker}", {"order": "d", "limit": 1})
            if isinstance(eod, list) and eod:
                row = eod[0]
                prices[ticker] = {
                    "date":           row.get("date", ""),
                    "close":          row.get("adjusted_close") or row.get("close"),
                    "adjusted_close": row.get("adjusted_close"),
                }
            else:
                errors[ticker] = "Sin datos EOD"
        except HTTPException as e:
            errors[ticker] = f"Error {e.status_code}"
        except Exception as e:
            errors[ticker] = str(e)[:80]
    return {
        "prices":    prices,
        "errors":    errors,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

# ── archivos estáticos ────────────────────────────────────────────────────────
if DOCS.exists():
    if (DOCS / "screenshots").exists():
        app.mount("/screenshots", StaticFiles(directory=str(DOCS/"screenshots")), name="screenshots")
    if (DOCS / "data").exists():
        app.mount("/data", StaticFiles(directory=str(DOCS/"data")), name="data")

@app.get("/glossary")
@app.get("/glossary.html")
def glossary():   return FileResponse(str(DOCS/"glossary.html"))

@app.get("/api-keys")
@app.get("/api-keys.html")
def api_keys():   return FileResponse(str(DOCS/"api-keys.html"))

@app.get("/analyze")
@app.get("/analyze.html")
def analyze_page(): return FileResponse(str(DOCS/"analyze.html"))

@app.get("/claude-setup")
@app.get("/claude-setup.html")
def claude_setup(): return FileResponse(str(DOCS/"claude-setup.html"))

@app.get("/paper-trading-edu")
@app.get("/paper-trading-edu.html")
def paper_trading_edu(): return FileResponse(str(DOCS/"paper-trading-edu.html"))

@app.get("/portfolio")
@app.get("/portfolio.html")
def portfolio_page(): return FileResponse(str(DOCS/"portfolio.html"))

@app.get("/")
@app.get("/index.html")
def index():      return FileResponse(str(DOCS/"index.html"))
