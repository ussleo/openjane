"""
OpenJane — Massive.com API client
Documentación oficial: https://docs.massive.com/api

Tier gratuito: datos con ~15min de retraso, acciones USA, opciones, forex, crypto.
Sin tarjeta de crédito. Registro en https://massive.com
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

MASSIVE_BASE = "https://api.massive.com/v1"
API_KEY = os.environ.get("MASSIVE_API_KEY", "")


def _get(endpoint: str, params: dict = None) -> dict:
    if not API_KEY:
        raise RuntimeError(
            "MASSIVE_API_KEY no configurada. "
            "Copia .env.example como .env y añade tu API key de https://massive.com"
        )
    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}
    url = f"{MASSIVE_BASE}{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


# ── Cotización en tiempo real (delayed 15min en free tier) ──────────────────

def quote(ticker: str) -> dict:
    """
    Retorna precio, bid, ask, volumen y timestamp para un ticker USA.

    Ejemplo de respuesta:
    {
        "symbol": "AAPL",
        "price": 189.45,
        "bid": 189.44,
        "ask": 189.46,
        "spread_pct": 0.011,
        "volume": 42_381_200,
        "timestamp": "2024-01-15T16:00:00Z"
    }
    """
    data = _get(f"/quote/{ticker.upper()}")
    bid = data.get("bid", 0)
    ask = data.get("ask", 0)
    spread_pct = round((ask - bid) / ask * 100, 4) if ask else None
    return {
        "symbol": data.get("symbol"),
        "price": data.get("last") or data.get("price"),
        "bid": bid,
        "ask": ask,
        "spread_pct": spread_pct,
        "volume": data.get("volume"),
        "timestamp": data.get("timestamp") or datetime.utcnow().isoformat() + "Z",
    }


# ── Spread bid-ask ──────────────────────────────────────────────────────────

def spread_analysis(ticker: str) -> dict:
    """
    Análisis de microestructura: spread relativo y clasificación de liquidez.
    Usado por la skill microstructure-analysis.
    """
    q = quote(ticker)
    spread = q["spread_pct"]

    if spread is None:
        liquidity_label = "Sin datos"
    elif spread < 0.05:
        liquidity_label = "Alta — institucional"
    elif spread < 0.15:
        liquidity_label = "Normal"
    elif spread < 0.5:
        liquidity_label = "Reducida"
    else:
        liquidity_label = "Ilíquida / Estrés"

    return {
        **q,
        "liquidity_label": liquidity_label,
        "transaction_cost_pct": round((spread or 0) * 2, 4),
    }


# ── Volumen y ADV ───────────────────────────────────────────────────────────

def volume_profile(ticker: str, days: int = 20) -> dict:
    """
    Volumen de hoy vs promedio de los últimos N días (ADV).
    Usado para calcular VPIN conceptual y señal de flujo.
    """
    data = _get(f"/volume/{ticker.upper()}", {"days": days})
    adv = data.get("avg_daily_volume")
    today_vol = data.get("today_volume") or data.get("volume")
    ratio = round(today_vol / adv, 2) if adv and today_vol else None

    flow_signal = "Neutral"
    if ratio:
        if ratio > 2.0:
            flow_signal = "Volumen extremo — posible evento informado"
        elif ratio > 1.5:
            flow_signal = "Volumen alto — flujo direccional probable"
        elif ratio < 0.5:
            flow_signal = "Volumen bajo — mercado ilíquido"

    return {
        "symbol": ticker.upper(),
        "adv_days": days,
        "adv": adv,
        "today_volume": today_vol,
        "volume_ratio": ratio,
        "flow_signal": flow_signal,
    }


# ── Opciones: volatilidad implícita ────────────────────────────────────────

def options_iv(ticker: str, expiry: str = None) -> dict:
    """
    Volatilidad implícita at-the-money y skew básico.
    expiry: formato YYYY-MM-DD. Si None, usa el vencimiento más próximo.
    Usado por la skill vol-surface.
    """
    params = {}
    if expiry:
        params["expiry"] = expiry
    data = _get(f"/options/iv/{ticker.upper()}", params)
    return {
        "symbol": ticker.upper(),
        "expiry": data.get("expiry"),
        "iv_atm": data.get("iv_atm"),           # IV call ATM
        "iv_25d_call": data.get("iv_25d_call"),  # 25-delta call
        "iv_25d_put": data.get("iv_25d_put"),    # 25-delta put (skew)
        "put_call_ratio": data.get("put_call_ratio"),
        "timestamp": data.get("timestamp") or datetime.utcnow().isoformat() + "Z",
    }


# ── VIX y régimen de volatilidad ────────────────────────────────────────────

def vix_current() -> dict:
    """
    Nivel actual del VIX y clasificación de régimen de volatilidad.
    Usado por regime-classification y vol-surface.
    """
    data = _get("/quote/VIX")
    vix = data.get("last") or data.get("price", 0)

    if vix < 15:
        regime = "Calma — estrategias de venta de vol favorecidas"
    elif vix < 20:
        regime = "Normal"
    elif vix < 30:
        regime = "Volatilidad elevada — reducir exposición"
    elif vix < 40:
        regime = "Crisis — preservar capital"
    else:
        regime = "Pánico extremo — históricamente señal de agotamiento"

    return {
        "vix": vix,
        "vol_regime": regime,
        "timestamp": data.get("timestamp") or datetime.utcnow().isoformat() + "Z",
    }


# ── CLI rápido para pruebas ─────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python massive_client.py <TICKER>")
        print("Ejemplo: python massive_client.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    print(f"\n── Quote: {ticker} ──────────────────────")
    print(json.dumps(quote(ticker), indent=2))

    print(f"\n── Spread Analysis: {ticker} ──────────")
    print(json.dumps(spread_analysis(ticker), indent=2))

    print(f"\n── Volume Profile: {ticker} (20d) ─────")
    print(json.dumps(volume_profile(ticker), indent=2))

    print(f"\n── VIX ─────────────────────────────────")
    print(json.dumps(vix_current(), indent=2))
