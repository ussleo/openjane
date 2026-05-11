"""
OpenJane · FastAPI server
Sirve la landing estática + endpoints de análisis en tiempo real.

Endpoints:
  GET  /                    → landing page (docs/index.html)
  GET  /static/*            → assets de docs/
  POST /api/regime          → régimen de mercado global
  POST /api/microstructure  → microestructura de un ticker
  POST /api/statarb         → stat-arb entre dos tickers
  GET  /api/health          → healthcheck para Fly.io
"""

import os, math, time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# ── paths ────────────────────────────────────────────────────────────────────
BASE  = Path(__file__).parent.parent          # raíz del repo
DOCS  = BASE / "docs"
SCRIP = BASE / "scripts"

import sys
sys.path.insert(0, str(BASE))

app = FastAPI(title="OpenJane", docs_url=None, redoc_url=None)

# ── rate limit simple en memoria ────────────────────────────────────────────
from collections import defaultdict
_hits: dict = defaultdict(list)
RATE_WINDOW = 60   # segundos
RATE_LIMIT  = 10   # llamadas por ventana por IP

def check_rate(ip: str):
    now = time.time()
    _hits[ip] = [t for t in _hits[ip] if now - t < RATE_WINDOW]
    if len(_hits[ip]) >= RATE_LIMIT:
        raise HTTPException(429, "Too many requests — espera un momento.")
    _hits[ip].append(now)

# ── helpers de análisis ──────────────────────────────────────────────────────
def _load_clients(massive_key: str, eodhd_key: str):
    os.environ["MASSIVE_API_KEY"] = massive_key
    os.environ["EODHD_API_KEY"]   = eodhd_key
    # re-importar para que lean las vars actualizadas
    import importlib
    import scripts.massive_client as mc
    import scripts.eodhd_client   as ec
    importlib.reload(mc)
    importlib.reload(ec)
    return mc, ec

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

# ── modelos de request ────────────────────────────────────────────────────────
class KeysBase(BaseModel):
    massive_key: str
    eodhd_key:   str

class TickerRequest(KeysBase):
    ticker: str

class PairRequest(KeysBase):
    ticker_a: str
    ticker_b: str

# ── endpoints de análisis ─────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "service": "OpenJane"}

@app.post("/api/regime")
def regime(req: KeysBase, request_ip: str = "unknown"):
    check_rate(request_ip)
    try:
        mc, ec = _load_clients(req.massive_key, req.eodhd_key)
        spy = ec.moving_averages("SPY")
        hv  = ec.historical_volatility("SPY", window=20)
        yc  = ec.yield_curve_spread()

        score = sum([
            spy["last_close"] > spy["ma200"],
            spy["ma50"]       > spy["ma200"],
            yc["spread_10y_2y"] > 0,
            hv.get("hv_annual_pct", 99) < 20,
        ])
        labels = {4:"ALCISTA FUERTE", 3:"ALCISTA MODERADO", 2:"MIXTO",
                  1:"BAJISTA MODERADO", 0:"BAJISTA / CRISIS"}

        return {
            "spy":        spy,
            "hv_20d":     hv,
            "yield_curve": yc,
            "score":      score,
            "regime":     labels.get(score, "—"),
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/microstructure")
def microstructure(req: TickerRequest, request_ip: str = "unknown"):
    check_rate(request_ip)
    try:
        mc, ec = _load_clients(req.massive_key, req.eodhd_key)
        ticker = req.ticker.upper()
        pc     = mc.prev_close(ticker)
        vol    = mc.volume_profile(ticker, days=20)
        tr     = ec.moving_averages(ticker)
        hv     = ec.historical_volatility(ticker, window=20)

        intraday = round((pc["high"]-pc["low"])/pc["close"]*100, 3) if pc.get("close") else None
        liq = ("ALTA" if intraday and intraday < 1.0
               else "NORMAL" if intraday and intraday < 3.0
               else "REDUCIDA" if intraday else "Sin datos")

        return {
            "ticker":     ticker,
            "price":      pc,
            "volume":     vol,
            "trend":      tr,
            "hv_20d":     hv,
            "intraday_range_pct": intraday,
            "liquidity":  liq,
            "transaction_cost_pct": round(intraday * 0.4, 3) if intraday else None,
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/api/statarb")
def statarb(req: PairRequest, request_ip: str = "unknown"):
    check_rate(request_ip)
    try:
        mc, ec = _load_clients(req.massive_key, req.eodhd_key)
        ta = req.ticker_a.upper()
        tb = req.ticker_b.upper()

        pa = [d["adjusted_close"] for d in ec.historical_prices(ta, days=365)]
        pb = [d["adjusted_close"] for d in ec.historical_prices(tb, days=365)]
        n  = min(len(pa), len(pb))
        pa = pa[-n:]; pb = pb[-n:]

        co                          = _corr(pa, pb)
        beta, mean_sp, std_sp, z, spreads = _beta_zscore(pa, pb)
        hl                          = _halflife(spreads)

        signal = ("ENTRADA LARGA"  if z < -2.0
                  else "ENTRADA CORTA" if z >  2.0
                  else "MONITOREAR"    if abs(z) >= 1.5
                  else "NEUTRAL")

        return {
            "pair":         f"{ta}/{tb}",
            "n_days":       n,
            "correlation":  co,
            "beta":         beta,
            "spread_mean":  mean_sp,
            "spread_std":   std_sp,
            "zscore":       z,
            "halflife_days": hl,
            "entry_long":   round(mean_sp - 2*std_sp, 2),
            "entry_short":  round(mean_sp + 2*std_sp, 2),
            "stop":         round(3.5*std_sp, 2),
            "exit_target":  round(mean_sp, 2),
            "signal":       signal,
        }
    except Exception as e:
        raise HTTPException(500, str(e))

# ── archivos estáticos y SPA ──────────────────────────────────────────────────
# Servir docs/ como static (screenshots, data, etc.)
if DOCS.exists():
    app.mount("/screenshots", StaticFiles(directory=str(DOCS / "screenshots")), name="screenshots")
    app.mount("/data",        StaticFiles(directory=str(DOCS / "data")),        name="data")

@app.get("/glossary")
@app.get("/glossary.html")
def glossary():
    return FileResponse(str(DOCS / "glossary.html"))

@app.get("/api-keys")
@app.get("/api-keys.html")
def api_keys():
    return FileResponse(str(DOCS / "api-keys.html"))

@app.get("/analyze")
@app.get("/analyze.html")
def analyze_page():
    return FileResponse(str(DOCS / "analyze.html"))

@app.get("/claude-setup")
@app.get("/claude-setup.html")
def claude_setup():
    return FileResponse(str(DOCS / "claude-setup.html"))

@app.get("/")
@app.get("/index.html")
def index():
    return FileResponse(str(DOCS / "index.html"))
