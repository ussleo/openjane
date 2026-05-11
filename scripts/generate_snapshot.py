"""
OpenJane — Generador de snapshot para GitHub Pages
Uso: python scripts/generate_snapshot.py

Genera docs/data/snapshot.json con datos reales de Massive y EODHD.
Correr este script y hacer commit/push refresca los datos en la landing page.

Frecuencia recomendada: una vez al día (EODHD tiene límite de 20 llamadas/día en free tier).
"""

import os, sys, json, time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # sin python-dotenv, leer variables de entorno del sistema

from scripts.massive_client import prev_close, volume_profile, ticker_details
from scripts.eodhd_client import moving_averages, historical_volatility, yield_curve_spread

# Tickers a incluir en el snapshot
TICKERS = ['SPY', 'AAPL', 'ICE', 'CBOE']

# Pausa entre llamadas para respetar rate limits
DELAY = 2.5  # segundos

def fetch_ticker(symbol: str) -> dict:
    snap = {}
    print(f"  [{symbol}] prev_close...", end=" ", flush=True)
    try:
        snap['prev_close'] = prev_close(symbol)
        print("OK", flush=True)
    except Exception as e:
        print(f"SKIP ({e})", flush=True)
    time.sleep(DELAY)

    print(f"  [{symbol}] volume_profile...", end=" ", flush=True)
    try:
        snap['volume'] = volume_profile(symbol, days=20)
        print("OK", flush=True)
    except Exception as e:
        print(f"SKIP ({e})", flush=True)
    time.sleep(DELAY)

    print(f"  [{symbol}] moving_averages...", end=" ", flush=True)
    try:
        snap['trend'] = moving_averages(symbol)
        print("OK", flush=True)
    except Exception as e:
        print(f"SKIP ({e})", flush=True)
    time.sleep(DELAY)

    print(f"  [{symbol}] historical_volatility...", end=" ", flush=True)
    try:
        snap['hv'] = historical_volatility(symbol, window=20)
        print("OK", flush=True)
    except Exception as e:
        print(f"SKIP ({e})", flush=True)
    time.sleep(DELAY)

    print(f"  [{symbol}] ticker_details...", end=" ", flush=True)
    try:
        snap['details'] = ticker_details(symbol)
        print("OK", flush=True)
    except Exception as e:
        print(f"SKIP ({e})", flush=True)
    time.sleep(DELAY)

    return snap

def main():
    print(f"\nOpenJane · generate_snapshot.py")
    print(f"Fecha: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Tickers: {', '.join(TICKERS)}")
    print("=" * 50)

    output = {
        "generated_utc": datetime.utcnow().isoformat() + "Z",
        "tickers": {},
        "macro": {}
    }

    # Tickers
    for symbol in TICKERS:
        print(f"\n── {symbol} ──")
        output["tickers"][symbol] = fetch_ticker(symbol)

    # Macro global
    print(f"\n── Macro global ──")
    print("  yield_curve_spread...", end=" ", flush=True)
    try:
        output["macro"]["yield_curve"] = yield_curve_spread()
        print("OK", flush=True)
    except Exception as e:
        print(f"SKIP ({e})", flush=True)

    # Guardar
    out_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'data', 'snapshot.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Guardado en docs/data/snapshot.json")
    print(f"  Tickers con datos: {sum(1 for v in output['tickers'].values() if v)}/{len(TICKERS)}")
    print(f"\nPróximo paso: git add docs/data/snapshot.json && git push")
    print("Los datos aparecerán en la landing page de GitHub Pages automáticamente.\n")

if __name__ == "__main__":
    main()
