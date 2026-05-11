"""
OpenJane — Massive.com API client
Documentación: https://massive.com/docs
Registro gratuito: https://massive.com (sin tarjeta de crédito)

Nota sobre el free tier:
- Disponible: históricos EOD, cierre anterior, detalles de ticker, agrupados diarios
- No disponible en free: real-time snapshots, opciones, last trade (requieren plan de pago)
- Para datos de opciones e IV, usar EODHD + yfinance como alternativa
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

MASSIVE_BASE = "https://api.massive.com"
API_KEY = os.environ.get("MASSIVE_API_KEY", "")


def _get(endpoint: str, params: dict = None) -> dict:
    if not API_KEY:
        raise RuntimeError(
            "MASSIVE_API_KEY no configurada. "
            "Copia .env.example como .env y añade tu key de https://massive.com"
        )
    url = f"{MASSIVE_BASE}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


# ── Cierre anterior (free tier) ─────────────────────────────────────────────

def prev_close(ticker: str) -> dict:
    """
    Retorna el cierre, apertura, máximo, mínimo y volumen del día anterior.
    Es el endpoint más fiable del free tier — siempre disponible.

    Ejemplo de retorno:
    {
        "symbol": "AAPL",
        "close": 213.49,
        "open": 211.20,
        "high": 214.08,
        "low": 210.10,
        "volume": 48_200_000,
        "date": "2026-05-08"
    }
    """
    data = _get(f"/v2/aggs/ticker/{ticker.upper()}/prev")
    results = data.get("results", [])
    if not results:
        return {"symbol": ticker.upper(), "error": "Sin datos disponibles"}
    r = results[0]
    ts = r.get("t", 0)
    date_str = datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d") if ts else "N/A"
    return {
        "symbol": ticker.upper(),
        "close": r.get("c"),
        "open": r.get("o"),
        "high": r.get("h"),
        "low": r.get("l"),
        "volume": int(r.get("v", 0)),
        "vwap": r.get("vw"),
        "date": date_str,
        "source": "Massive.com (free tier — datos EOD)",
    }


# ── Históricos OHLCV ────────────────────────────────────────────────────────

def historical_bars(ticker: str, days: int = 20, timespan: str = "day") -> list[dict]:
    """
    Barras históricas OHLCV para los últimos N días.
    timespan: 'day', 'week', 'month'
    """
    date_to = datetime.utcnow().strftime("%Y-%m-%d")
    date_from = (datetime.utcnow() - timedelta(days=days + 10)).strftime("%Y-%m-%d")
    data = _get(
        f"/v2/aggs/ticker/{ticker.upper()}/range/1/{timespan}/{date_from}/{date_to}",
        {"adjusted": "true", "sort": "asc", "limit": days},
    )
    results = data.get("results", [])
    bars = []
    for r in results:
        ts = r.get("t", 0)
        bars.append({
            "date": datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d"),
            "open": r.get("o"),
            "high": r.get("h"),
            "low": r.get("l"),
            "close": r.get("c"),
            "volume": int(r.get("v", 0)),
            "vwap": r.get("vw"),
        })
    return bars


# ── Spread bid-ask estimado (free tier) ─────────────────────────────────────

def spread_estimate(ticker: str) -> dict:
    """
    Estima spread bid-ask usando el rango intraday del día anterior (high - low).
    En free tier no hay bid/ask en tiempo real — esto es una aproximación
    basada en la volatilidad intraday.

    Interpretación:
    - spread_pct < 0.5%: activo líquido
    - spread_pct 0.5–2%: liquidez moderada
    - spread_pct > 2%: activo ilíquido o jornada volátil
    """
    pc = prev_close(ticker)
    if "error" in pc:
        return pc

    high = pc.get("high", 0)
    low = pc.get("low", 0)
    close = pc.get("close", 0)

    intraday_range_pct = round((high - low) / close * 100, 4) if close else None

    if intraday_range_pct is None:
        liquidity = "Sin datos"
    elif intraday_range_pct < 0.5:
        liquidity = "Alta — institucional"
    elif intraday_range_pct < 2.0:
        liquidity = "Normal"
    elif intraday_range_pct < 5.0:
        liquidity = "Reducida"
    else:
        liquidity = "Ilíquida / Estrés"

    return {
        **pc,
        "intraday_range_pct": intraday_range_pct,
        "liquidity_label": liquidity,
        "note": "Spread estimado via rango intraday (free tier — no hay bid/ask en tiempo real)",
    }


# ── Perfil de volumen ────────────────────────────────────────────────────────

def volume_profile(ticker: str, days: int = 20) -> dict:
    """
    Volumen del día anterior vs ADV de los últimos N días.
    Señal de flujo basada en volumen relativo.
    """
    bars = historical_bars(ticker, days=days)
    if not bars:
        return {"symbol": ticker.upper(), "error": "Sin datos de volumen"}

    volumes = [b["volume"] for b in bars if b["volume"]]
    adv = int(sum(volumes) / len(volumes)) if volumes else 0
    today_vol = volumes[-1] if volumes else 0
    ratio = round(today_vol / adv, 2) if adv else None

    flow_signal = "Neutral"
    if ratio:
        if ratio > 2.0:
            flow_signal = "Volumen extremo — posible evento informado"
        elif ratio > 1.5:
            flow_signal = "Volumen alto — flujo direccional probable"
        elif ratio < 0.5:
            flow_signal = "Volumen bajo — mercado inactivo"

    return {
        "symbol": ticker.upper(),
        "adv_days": days,
        "adv": adv,
        "last_session_volume": today_vol,
        "volume_ratio": ratio,
        "flow_signal": flow_signal,
        "date": bars[-1]["date"] if bars else "N/A",
        "source": "Massive.com (free tier)",
    }


# ── Detalles del ticker ──────────────────────────────────────────────────────

def ticker_details(ticker: str) -> dict:
    """
    Nombre, sector, mercado, descripción, capitalización estimada.
    Endpoint /v3/reference/tickers — disponible en free tier.
    """
    data = _get(f"/v3/reference/tickers/{ticker.upper()}")
    r = data.get("results", {})
    return {
        "symbol": ticker.upper(),
        "name": r.get("name"),
        "market": r.get("market"),
        "locale": r.get("locale"),
        "primary_exchange": r.get("primary_exchange"),
        "type": r.get("type"),
        "active": r.get("active"),
        "currency": r.get("currency_name"),
        "description": (r.get("description") or "")[:300],
        "homepage": r.get("homepage_url"),
        "employees": r.get("total_employees"),
        "list_date": r.get("list_date"),
        "source": "Massive.com (free tier)",
    }


# ── CLI rápido para pruebas ─────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    ticker = sys.argv[1].upper() if len(sys.argv) > 1 else "AAPL"
    print(f"\n── Prev Close: {ticker} ─────────────────")
    print(json.dumps(prev_close(ticker), indent=2))

    print(f"\n── Spread Estimate: {ticker} ───────────")
    print(json.dumps(spread_estimate(ticker), indent=2))

    print(f"\n── Volume Profile: {ticker} (20d) ──────")
    print(json.dumps(volume_profile(ticker), indent=2))

    print(f"\n── Ticker Details: {ticker} ────────────")
    print(json.dumps(ticker_details(ticker), indent=2))
