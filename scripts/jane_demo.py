"""
OpenJane · Demo Script
Corre un análisis completo con datos reales y produce output para screenshot.

Uso:
    python scripts/jane_demo.py
    python scripts/jane_demo.py CBOE        # microestructura de otro ticker
    python scripts/jane_demo.py ICE CBOE    # stat-arb de otro par
"""

import sys, io, math, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from scripts.massive_client import prev_close, volume_profile
from scripts.eodhd_client import (
    moving_averages, historical_volatility,
    yield_curve_spread, historical_prices
)
from datetime import datetime, timezone

# ── Config ──────────────────────────────────────────────────────────────────
TICKER_A   = sys.argv[1].upper() if len(sys.argv) > 1 else 'ICE'
TICKER_B   = sys.argv[2].upper() if len(sys.argv) > 2 else 'CBOE'
BENCHMARK  = 'SPY'
W          = 64
NOW        = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

# ── Helpers ─────────────────────────────────────────────────────────────────
def hline(c='-'): print('+' + c*(W-2) + '+')
def blank():      print('|' + ' '*(W-2) + '|')
def title(t, c='-'):
    hline(c)
    pad = (W - 2 - len(t)) // 2
    print('|' + ' '*pad + t + ' '*(W - 2 - pad - len(t)) + '|')
    hline(c)

def row(label, value, indent=2):
    line = f'{" "*indent}{label:<28} {value}'
    if len(line) > W-2: line = line[:W-3] + '…'
    print('|' + line + ' '*(W-2-len(line)) + '|')

def note(text, indent=2):
    line = ' '*indent + text
    if len(line) > W-2: line = line[:W-3] + '…'
    print('|' + line + ' '*(W-2-len(line)) + '|')

def corr(a, b):
    n = len(a); ma = sum(a)/n; mb = sum(b)/n
    num = sum((a[i]-ma)*(b[i]-mb) for i in range(n))
    da  = math.sqrt(sum((x-ma)**2 for x in a))
    db  = math.sqrt(sum((x-mb)**2 for x in b))
    return round(num/(da*db), 4) if da*db else 0

def beta_zscore(a, b):
    n = len(a); ma = sum(a)/n; mb = sum(b)/n
    beta   = sum((a[i]-ma)*(b[i]-mb) for i in range(n)) / sum((x-mb)**2 for x in b)
    spread = [a[i] - beta*b[i] for i in range(n)]
    ms     = sum(spread)/n
    std    = math.sqrt(sum((s-ms)**2 for s in spread)/n)
    zscore = round((spread[-1]-ms)/std, 3) if std else 0
    return round(beta,4), round(ms,4), round(std,4), zscore, spread

def halflife(sp):
    n = len(sp)
    y = [sp[i]-sp[i-1] for i in range(1, n)]
    x = sp[:-1]
    mx = sum(x)/len(x); my = sum(y)/len(y)
    b = sum((x[i]-mx)*(y[i]-my) for i in range(len(x))) / sum((v-mx)**2 for v in x)
    return round(-math.log(2)/b, 1) if b and b < 0 else None

# ════════════════════════════════════════════════════════════════════════════
print()
hline('=')
pad = (W - 2 - 44) // 2
print('|' + ' '*pad + 'OpenJane  ·  Quant Analyst  ·  Live Analysis' + ' '*(W-2-pad-44) + '|')
pad2 = (W - 2 - len(NOW)) // 2
print('|' + ' '*pad2 + NOW + ' '*(W-2-pad2-len(NOW)) + '|')
hline('=')
print()

# ── BLOQUE 1: RÉGIMEN ────────────────────────────────────────────────────────
print()
title('[1/3]  REGIMEN DE MERCADO  —  /regime', '=')
blank()

print('  Cargando datos del mercado...')
yc  = yield_curve_spread()
spy = moving_averages(BENCHMARK)
hv  = historical_volatility(BENCHMARK, window=20)

row('Benchmark',       BENCHMARK)
row('Precio cierre',   f"${spy['last_close']:.2f}")
row('MA50  /  MA200',  f"${spy['ma50']:.2f}  /  ${spy['ma200']:.2f}")
pct_vs_200 = (spy['last_close'] / spy['ma200'] - 1) * 100
row('Precio vs MA200', f"{'SOBRE' if pct_vs_200>0 else 'BAJO'} MA200 ({pct_vs_200:+.1f}%)")
row('Tendencia',       spy['trend'].upper())
blank()
row('HV 20d (realizada)',  f"{hv['hv_annual_pct']}%  anualizada  /  {hv['hv_daily_pct']}% diaria")
blank()
row('Treasury 10Y  /  2Y', f"{yc['us10y']}%  /  {yc['us2y']}%")
row('Spread 10Y - 2Y',     f"{yc['spread_10y_2y']:+.3f}%")
row('Yield curve label',   yc['yield_curve_label'][:38])
blank()

score = sum([
    spy['last_close'] > spy['ma200'],
    spy['ma50']       > spy['ma200'],
    yc['spread_10y_2y'] > 0,
    hv['hv_annual_pct'] < 20,
])
regime_label = {4:'ALCISTA FUERTE',3:'ALCISTA MODERADO',2:'MIXTO',
                1:'BAJISTA MODERADO',0:'BAJISTA / CRISIS'}.get(score,'—')

hline()
row('SCORE DE REGIMEN', f"+{score} / +4   →   {regime_label}")
hline()
blank()
note('Interpretacion:')
if score >= 3:
    note('  Condiciones macro favorables para estrategias largas,')
    note('  momentum y stat-arb. Volatilidad baja — opciones baratas.')
elif score == 2:
    note('  Mercado mixto. Reducir tamano de posiciones,')
    note('  esperar confirmacion antes de nuevas entradas.')
else:
    note('  Regimen desfavorable. Priorizar preservacion de capital.')
blank()
note(f'Fuentes: EODHD (MA50/MA200/HV) + EODHD (yield curve)')
note(f'Datos: EOD  |  Actualizado: {NOW}')
blank()
hline()

# ── BLOQUE 2: MICROESTRUCTURA ────────────────────────────────────────────────
print()
title(f'[2/3]  MICROESTRUCTURA  —  /spread-analysis {TICKER_A}', '=')
blank()

print(f'  Cargando datos de {TICKER_A}...')
pc  = prev_close(TICKER_A)
vol = volume_profile(TICKER_A, days=20)
tr  = moving_averages(TICKER_A)
hva = historical_volatility(TICKER_A, window=20)

row('Ticker',            pc['symbol'])
row('Precio cierre',     f"${pc['close']:.2f}  ({pc['date']})")
row('Apertura',          f"${pc['open']:.2f}")
row('Maximo  /  Minimo', f"${pc['high']:.2f}  /  ${pc['low']:.2f}")
row('VWAP sesion',       f"${pc['vwap']:.2f}")
blank()
intraday = round((pc['high'] - pc['low']) / pc['close'] * 100, 3)
liq_label = 'ALTA — institucional' if intraday < 1.0 else 'NORMAL' if intraday < 3.0 else 'REDUCIDA'
row('Rango intraday',    f"{intraday}%  →  Liquidez {liq_label}")
row('Costo transaccion', f"~{intraday*0.4:.3f}%  round-trip (estimado)")
blank()
row('ADV 20d',           f"{vol['adv']:,} acciones / dia")
row('Volumen sesion',    f"{vol['last_session_volume']:,}  ({vol['volume_ratio']}x ADV)")
row('Senal de flujo',    vol['flow_signal'])
blank()
row('MA50  /  MA200',    f"${tr['ma50']:.2f}  /  ${tr['ma200']:.2f}")
row('Tendencia',         tr['trend'].upper())
pct200 = (tr['last_close'] / tr['ma200'] - 1) * 100
row('Precio vs MA200',   f"{pct200:+.2f}%  ({'SOBRE' if pct200>0 else 'BAJO'} MA200)")
row('HV 20d',            f"{hva.get('hv_annual_pct','?')}%  anualizada")
blank()

hline()
note('VEREDICTO DE MICROESTRUCTURA:')
blank()
if intraday < 2.0 and vol['volume_ratio'] and 0.7 <= vol['volume_ratio'] <= 1.5:
    note(f'  Liquidez en condiciones normales. Volumen en linea con ADV.')
elif vol['volume_ratio'] and vol['volume_ratio'] > 1.5:
    note(f'  Volumen elevado ({vol["volume_ratio"]}x ADV) — posible flujo informado.')
else:
    note(f'  Volumen bajo ({vol.get("volume_ratio","?")}x ADV) — liquidez reducida.')

if tr['trend'] == 'alcista':
    note(f'  Tendencia alcista confirmada (precio sobre MA200).')
elif tr['trend'] == 'bajista':
    note(f'  Tendencia bajista — precio {abs(pct200):.1f}% bajo MA200.')
else:
    note(f'  Tendencia en transicion — zona de indecision.')
blank()
note(f'Fuentes: Massive.com (precio/vol)  +  EODHD (MA/HV)')
note(f'Datos: EOD  |  Actualizado: {NOW}')
blank()
hline()

# ── BLOQUE 3: STAT-ARB ───────────────────────────────────────────────────────
print()
title(f'[3/3]  STAT-ARB  —  /stat-arb {TICKER_A} {TICKER_B}', '=')
blank()

print(f'  Calculando relacion historica {TICKER_A}/{TICKER_B}...')
prices_a = [d['adjusted_close'] for d in historical_prices(TICKER_A, days=365)]
prices_b = [d['adjusted_close'] for d in historical_prices(TICKER_B, days=365)]
n = min(len(prices_a), len(prices_b))
pa = prices_a[-n:]; pb = prices_b[-n:]

co = corr(pa, pb)
beta, mean_sp, std_sp, zscore, spreads = beta_zscore(pa, pb)
hl = halflife(spreads)

row('Par',               f"{TICKER_A}  vs  {TICKER_B}")
row('Ventana historica', f"{n} dias  (~1 año)")
blank()
row('Correlacion 252d',  f"{co}  ({'FUERTE' if co>0.75 else 'MODERADA' if co>0.5 else 'DEBIL — verificar'})")
row('Beta (regresion)',   str(beta))
row('Spread medio',      f"${mean_sp:.2f}")
row('Spread std dev',    f"${std_sp:.2f}")
blank()
entry_up   = round(mean_sp + 2*std_sp, 2)
entry_down = round(mean_sp - 2*std_sp, 2)
stop_up    = round(mean_sp + 3.5*std_sp, 2)
stop_down  = round(mean_sp - 3.5*std_sp, 2)

row('Z-score actual',    f"{zscore}  ({'ENTRADA' if abs(zscore)>=2 else 'MONITOREAR' if abs(zscore)>=1.5 else 'NEUTRAL'})")
row('Half-life reversión', f"{hl} dias" if hl else "No estacionario — par no valido")
blank()
row('Zona entrada larga', f"spread < ${entry_down:.2f}  (Z < -2.0)")
row('Zona entrada corta', f"spread > ${entry_up:.2f}  (Z > +2.0)")
row('Objetivo (exit)',    f"spread = ${mean_sp:.2f}  (Z = 0)")
row('Stop-loss',          f"spread < ${stop_down:.2f}  o  > ${stop_up:.2f}  (Z = +-3.5)")
blank()

hline()
if abs(zscore) >= 2.0:
    note('  *** SENAL ACTIVA ***')
    if zscore < -2.0:
        note(f'  {TICKER_A} BARATO vs {TICKER_B}  →  COMPRAR {TICKER_A} / VENDER {TICKER_B}')
    else:
        note(f'  {TICKER_A} CARO vs {TICKER_B}   →  VENDER {TICKER_A} / COMPRAR {TICKER_B}')
    note(f'  Confianza: {"ALTA" if co>0.75 else "MEDIA — correlacion moderada"}')
    note(f'  Horizonte estimado: {hl} dias hasta convergencia' if hl else '  Horizonte: indefinido')
elif abs(zscore) >= 1.5:
    note(f'  Divergencia moderada (Z={zscore}). Monitorear.')
    note(f'  Senal de entrada si Z supera +-2.0.')
else:
    note(f'  Sin senal activa. Par dentro de rango normal (Z={zscore}).')
    note(f'  Proxima entrada cuando spread salga de ${entry_down:.2f} — ${entry_up:.2f}.')

if co < 0.75:
    blank()
    note(f'  AVISO: correlacion baja ({co}). Este par requiere')
    note(f'  validacion adicional antes de operar.')
blank()
note(f'Fuentes: EODHD (historicos ajustados 252d)')
note(f'Datos: EOD  |  Calculo: OLS beta + Z-score + Ornstein-Uhlenbeck')
blank()
hline()

print()
print(f'  OpenJane  |  {NOW}')
print(f'  Fuentes: Massive.com + EODHD  |  Datos EOD (no tiempo real)')
print(f'  Este analisis es educativo y no constituye asesoramiento financiero.')
print(f'  El usuario es responsable de sus propias decisiones de inversion.')
print()
