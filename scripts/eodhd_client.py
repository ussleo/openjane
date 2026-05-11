"""
OpenJane — EODHD API client
Documentación oficial: https://eodhd.com/financial-apis

Tier gratuito: 20 llamadas/día, históricos EOD, fundamentales limitados.
Sin tarjeta de crédito. Registro en https://eodhd.com
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

EODHD_BASE = "https://eodhd.com/api"
API_KEY = os.environ.get("EODHD_API_KEY", "")


def _get(endpoint: str, params: dict = None) -> dict | list:
    if not API_KEY:
        raise RuntimeError(
            "EODHD_API_KEY no configurada. "
            "Copia .env.example como .env y añade tu API key de https://eodhd.com"
        )
    base_params = {"api_token": API_KEY, "fmt": "json"}
    if params:
        base_params.update(params)
    url = f"{EODHD_BASE}{endpoint}?" + urllib.parse.urlencode(base_params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


# ── Precios históricos EOD ──────────────────────────────────────────────────

def historical_prices(ticker: str, exchange: str = "US", days: int = 252) -> list[dict]:
    """
    Precios de cierre ajustados para los últimos N días.
    Suficiente para calcular medias móviles, correlaciones y backtesting básico.

    ticker: símbolo sin exchange (ej: 'AAPL')
    exchange: 'US' para acciones USA, 'FOREX' para divisas, etc.
    days: días hacia atrás desde hoy

    Retorna lista de dicts: [{date, open, high, low, close, volume, adjusted_close}, ...]
    """
    date_from = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    symbol = f"{ticker.upper()}.{exchange}"
    data = _get(f"/eod/{symbol}", {"from": date_from, "order": "a"})
    return data if isinstance(data, list) else []


def moving_averages(ticker: str, exchange: str = "US") -> dict:
    """
    Calcula MA50 y MA200 a partir de históricos.
    Usado por regime-classification para clasificar tendencia.
    """
    prices = historical_prices(ticker, exchange, days=252)
    if len(prices) < 50:
        return {"error": "Datos insuficientes para calcular medias móviles"}

    closes = [float(p["adjusted_close"]) for p in prices]
    ma50 = round(sum(closes[-50:]) / 50, 4)
    ma200 = round(sum(closes[-200:]) / 200, 4) if len(closes) >= 200 else None
    last_close = closes[-1]

    trend = "insuficiente"
    if ma200:
        if last_close > ma200 and ma50 > ma200:
            trend = "alcista"
        elif last_close < ma200 and ma50 < ma200:
            trend = "bajista"
        else:
            trend = "transicion"

    return {
        "symbol": ticker.upper(),
        "last_close": last_close,
        "ma50": ma50,
        "ma200": ma200,
        "trend": trend,
        "data_points": len(closes),
    }


# ── Volatilidad histórica ───────────────────────────────────────────────────

def historical_volatility(ticker: str, exchange: str = "US", window: int = 20) -> dict:
    """
    Volatilidad histórica realizada en ventana de N días.
    Comparada con la IV de Massive para calcular prima de vol.

    Retorna HV en términos anualizados (como VIX: porcentaje).
    """
    import math

    prices = historical_prices(ticker, exchange, days=window + 10)
    if len(prices) < window + 1:
        return {"error": "Datos insuficientes"}

    closes = [float(p["adjusted_close"]) for p in prices]
    returns = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
    returns = returns[-window:]

    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
    hv_daily = math.sqrt(variance)
    hv_annual = round(hv_daily * math.sqrt(252) * 100, 2)  # en %

    return {
        "symbol": ticker.upper(),
        "hv_window_days": window,
        "hv_annual_pct": hv_annual,
        "hv_daily_pct": round(hv_daily * 100, 4),
    }


# ── Yield Curve (spread 10Y - 2Y) ──────────────────────────────────────────

def yield_curve_spread() -> dict:
    """
    Spread entre Treasury 10Y y 2Y — indicador clave de régimen macroeconómico.
    Curva invertida (spread < 0) = señal histórica de recesión futura.
    """
    us10y = _get("/eod/US10Y.INDX", {"period": "d", "order": "d", "limit": 1})
    us2y = _get("/eod/US02Y.INDX", {"period": "d", "order": "d", "limit": 1})

    rate10 = float(us10y[0]["close"]) if us10y else None
    rate2 = float(us2y[0]["close"]) if us2y else None
    spread = round(rate10 - rate2, 4) if rate10 and rate2 else None

    if spread is None:
        label = "Sin datos"
    elif spread > 0.5:
        label = "Curva normal — expansión económica"
    elif spread > 0:
        label = "Curva plana — transición, señal de alerta"
    elif spread > -0.5:
        label = "Curva levemente invertida — alerta de recesión"
    else:
        label = "Curva invertida — señal histórica de recesión en 6-18 meses"

    return {
        "us10y": rate10,
        "us2y": rate2,
        "spread_10y_2y": spread,
        "yield_curve_label": label,
    }


# ── Fundamentales básicos ───────────────────────────────────────────────────

def fundamentals(ticker: str, exchange: str = "US") -> dict:
    """
    Datos fundamentales: market cap, P/E, sector, descripción.
    Solo disponibles para acciones USA en el tier gratuito.
    """
    symbol = f"{ticker.upper()}.{exchange}"
    data = _get(f"/fundamentals/{symbol}")

    general = data.get("General", {})
    highlights = data.get("Highlights", {})
    valuation = data.get("Valuation", {})

    return {
        "symbol": ticker.upper(),
        "name": general.get("Name"),
        "sector": general.get("Sector"),
        "industry": general.get("Industry"),
        "market_cap": highlights.get("MarketCapitalization"),
        "pe_ratio": highlights.get("PERatio"),
        "eps": highlights.get("EarningsShare"),
        "dividend_yield": highlights.get("DividendYield"),
        "52w_high": highlights.get("52WeekHigh"),
        "52w_low": highlights.get("52WeekLow"),
        "price_to_book": valuation.get("PriceBookMRQ"),
    }


# ── CLI rápido para pruebas ─────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python eodhd_client.py <TICKER>")
        print("Ejemplo: python eodhd_client.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1].upper()

    print(f"\n── Moving Averages: {ticker} ───────────")
    print(json.dumps(moving_averages(ticker), indent=2))

    print(f"\n── Historical Volatility (20d): {ticker} ─")
    print(json.dumps(historical_volatility(ticker), indent=2))

    print(f"\n── Yield Curve ─────────────────────────")
    print(json.dumps(yield_curve_spread(), indent=2))

    print(f"\n── Fundamentals: {ticker} ──────────────")
    print(json.dumps(fundamentals(ticker), indent=2))
