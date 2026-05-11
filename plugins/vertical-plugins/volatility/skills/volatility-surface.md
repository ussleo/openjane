# Skill: vol-surface (Superficie de Volatilidad)

## Propósito

La volatilidad no es un número — es una estructura tridimensional que las firmas quant
leen como un mapa del miedo y la expectativa del mercado.

Esta skill traduce esa estructura a lenguaje claro: qué dice el mercado de opciones
sobre el riesgo percibido de un activo, si ese riesgo está caro o barato históricamente,
y qué señal envía para el análisis de régimen.

---

## El concepto central: IV vs HV

Toda la inteligencia de la superficie de volatilidad se reduce a una pregunta:

**¿El mercado está cobrando más (o menos) por protección de lo que el activo
ha movido históricamente?**

```
Prima de volatilidad = IV (volatilidad implícita) - HV (volatilidad histórica realizada)
```

| Prima | Señal |
|---|---|
| IV > HV + 10 puntos | Opciones caras — el mercado espera más movimiento del que ha habido |
| IV ≈ HV ± 5 puntos | Opciones con precio justo |
| IV < HV - 10 puntos | Opciones baratas — el mercado espera menos movimiento del que ha habido |

**Las firmas quant no predicen si el activo sube o baja. Predicen si la volatilidad
va a ser mayor o menor que lo que el mercado está cobrando por ella.**

---

## Los tres ejes de la superficie de volatilidad

### Eje 1 — Nivel (¿cuánto miedo hay?)

La IV at-the-money (ATM) es el nivel base: cuánto movimiento anualizado está
"descontando" el mercado para ese activo.

```
IV ATM de 30% = el mercado espera movimientos de ±30% anualizado
             = ±1.9% diario en promedio (30% ÷ √252)
```

**Clasificación práctica:**

| IV ATM | Qué indica |
|---|---|
| < 15% | Activo muy estable (ej: SPY en bull market tranquilo) |
| 15% – 30% | Normal para acciones individuales de gran capitalización |
| 30% – 60% | Activo con riesgo elevado o evento próximo |
| > 60% | Activo especulativo, binario o en crisis |

---

### Eje 2 — Skew (¿el miedo es simétrico?)

El skew mide si el mercado paga más por protección bajista (puts) que alcista (calls).

```
Skew = IV del put 25-delta - IV del call 25-delta
```

| Skew | Señal |
|---|---|
| Skew positivo alto (> 5 puntos) | Miedo a caída fuerte — inversores comprando protección |
| Skew neutro (0 – 3 puntos) | Expectativas simétricas |
| Skew negativo (< 0) | Miedo a subida fuerte (raro, típico en commodities o short squeezes) |

**El skew del S&P 500 es siempre positivo** — los gestores de cartera sistemáticamente
pagan más por protección bajista que por calls. Eso es una prima estructural que
las firmas quant explotan vendiendo ese skew de forma sistemática.

---

### Eje 3 — Estructura temporal (¿cuándo es el miedo?)

La curva de IV a través de distintos vencimientos dice en qué momento el mercado
concentra su incertidumbre.

```
Curva normal (contango): IV corto plazo < IV largo plazo
→ El mercado espera más movimiento en el futuro que ahora
→ Régimen de calma actual, incertidumbre estructural a largo plazo

Curva invertida (backwardation): IV corto plazo > IV largo plazo
→ El mercado está asustado AHORA
→ Típico en crisis, earnings, elecciones, decisiones de la Fed
```

---

## Protocolo de análisis vol-surface para el agente

Cuando el usuario pide `/vol-surface [TICKER]`:

**Paso 1 — Obtener IV actual (Massive.com)**
```python
from scripts.massive_client import options_iv, vix_current
iv_data = options_iv(ticker)
vix_data = vix_current()
```
Extraer: IV ATM, IV put 25-delta, IV call 25-delta, put/call ratio.

**Paso 2 — Obtener HV histórica (EODHD)**
```python
from scripts.eodhd_client import historical_volatility
hv_20 = historical_volatility(ticker, window=20)   # 20 días
hv_60 = historical_volatility(ticker, window=60)   # 60 días
```

**Paso 3 — Calcular prima de volatilidad**
```
Prima = IV_ATM - HV_20d
```
Clasificar según tabla de prima arriba.

**Paso 4 — Leer skew**
```
Skew = IV_put_25d - IV_call_25d
```
Clasificar según tabla de skew arriba.

**Paso 5 — Contexto VIX**
¿El VIX está en qué régimen? (ver régimen de volatilidad en massive_client)
¿La IV de este activo se mueve en línea con el VIX o diverge?

**Paso 6 — Veredicto de volatilidad**
Producir 4 componentes:
1. **Nivel de IV**: bajo / normal / elevado / extremo
2. **Prima de vol**: opciones caras / precio justo / opciones baratas
3. **Skew**: miedo bajista / neutro / miedo alcista
4. **Señal de régimen**: qué implica esta estructura para el análisis del activo

---

## Ejemplos de interpretación

### Ejemplo A — Activo tranquilo antes de earnings

```
Ticker: MSFT — 3 días antes de resultados trimestrales

IV ATM: 42%  (normal para MSFT es 22%)
HV 20d: 18%
Prima: +24 puntos → opciones MUY caras
Skew: +8 puntos → miedo bajista fuerte

Veredicto: El mercado está comprando protección agresivamente antes del earnings.
Las opciones están cotizando el doble de lo que MSFT se ha movido históricamente.
Quien vende opciones aquí cobra una prima alta, pero asume el riesgo del anuncio.
Quien las compra paga cara la protección.
```

### Ejemplo B — Post-crash, vol barata

```
Ticker: SPY — 2 semanas después de caída del 15%

IV ATM: 22%
HV 20d: 45%  (el activo se movió mucho en las últimas 3 semanas)
Prima: -23 puntos → opciones baratas
VIX: 19 (ya normalizándose)
Skew: +3 → neutro

Veredicto: El mercado ya descontó el miedo. Las opciones son baratas respecto
al movimiento reciente. Señal de régimen: la calma post-crisis puede ser
oportunidad para estrategias largas de volatilidad si se espera segunda ola.
```

---

## Put/Call Ratio como termómetro de sentimiento

El ratio de volumen de puts vs calls es un indicador contrario:

| P/C Ratio | Señal |
|---|---|
| > 1.5 | Extremo miedo bajista — históricamente señal contraria alcista |
| 1.0 – 1.5 | Sesgo bajista moderado |
| 0.7 – 1.0 | Normal |
| < 0.7 | Complacencia — posible exceso de optimismo |

**Importante:** el P/C ratio de un solo activo es menos confiable que el del
mercado en conjunto (S&P 500 total). Usar SPY como referencia de sentimiento global.

---

## Integración con las otras skills

Esta skill se conecta naturalmente con:

- **regime-classification**: el VIX y la estructura de vol son inputs directos
  al score de régimen
- **microstructure-analysis**: en activos con IV alta, los spreads bid-ask
  suelen ampliarse — los market makers cobran más por el riesgo de inventario
- **statistical-arbitrage**: en régimen de alta vol, las correlaciones entre pares
  se disparan hacia 1.0 y el stat-arb pierde efectividad

---

## Lo que esta skill NO puede hacer

- No predice si la IV va a subir o bajar
- No tiene acceso a la superficie completa (todos los strikes y vencimientos)
  en el tier gratuito — solo los puntos clave (ATM, 25-delta)
- No calcula Greeks (delta, gamma, vega) — eso requiere un modelo de pricing (Black-Scholes)
- No detecta si el volumen de opciones viene de cobertura institucional o especulación minorista

---

## Fuentes de datos

- **Massive.com API** (`options_iv`, `vix_current`): IV actual, skew, put/call ratio
- **EODHD API** (`historical_volatility`): HV realizada en múltiples ventanas

---

*Referencias: Black & Scholes (1973), Derman & Kani (1994) — local vol model,
Gatheral (2006) — The Volatility Surface, CBOE VIX methodology (2003).*
