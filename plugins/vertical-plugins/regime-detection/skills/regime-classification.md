# Skill: regime-detection (Detección de Régimen de Mercado)

## Propósito

Antes de aplicar cualquier estrategia, las firmas cuantitativas clasifican el estado
actual del mercado. Una estrategia de mean-reversion funciona bien en mercados laterales
y destruye capital en mercados tendenciales. Una estrategia de momentum funciona al revés.

Esta skill permite al agente responder la pregunta más importante antes de cualquier análisis:
**¿en qué tipo de mercado estamos hoy?**

---

## Los cuatro regímenes de mercado

### Régimen 1 — Tendencia alcista (Bull Trend)
**Características:**
- Precio sobre su media móvil de 200 días
- Media de 50 días sobre media de 200 días
- Volatilidad moderada o baja (VIX < 20)
- Volumen acompañando las subidas

**Qué funciona:** momentum, buy-and-hold, ETFs de índice, estrategias largas
**Qué no funciona:** estrategias de reversión a la media en índices generales

---

### Régimen 2 — Tendencia bajista (Bear Trend)
**Características:**
- Precio bajo su media móvil de 200 días
- Media de 50 días bajo media de 200 días
- Volatilidad elevada (VIX > 25)
- Volumen acompañando las bajadas

**Qué funciona:** protección con opciones, activos defensivos, cash, short selectivo
**Qué no funciona:** comprar caídas sin análisis de soporte, apalancamiento

---

### Régimen 3 — Mercado lateral (Range / Mean-Reversion)
**Características:**
- Precio oscila entre soporte y resistencia definidos
- Volatilidad baja a moderada y estable
- Sin dirección clara en medias móviles
- Volumen bajo o irregular

**Qué funciona:** stat-arb, venta de opciones, estrategias de reversión a la media
**Qué no funciona:** momentum, estrategias de breakout

---

### Régimen 4 — Crisis / Alta volatilidad (Stress Regime)
**Características:**
- VIX > 30, movimientos diarios > 2% frecuentes
- Correlaciones entre activos se disparan hacia 1.0
- Spreads bid-ask se amplían en todos los activos
- Liquidez se retira de los mercados

**Qué funciona:** cash, oro, treasuries de corto plazo, opciones de protección
**Qué no funciona:** casi todo lo demás — incluyendo el stat-arb, porque las correlaciones
se rompen temporalmente en crisis

---

## Cómo clasificar el régimen actual

### Indicadores primarios

**1. Posición relativa a medias móviles (S&P 500 como referencia)**
```
Si SPY > MA200: tendencia alcista base
Si SPY < MA200: tendencia bajista base
Si SPY entre MA50 y MA200: zona de transición
```

**2. VIX (índice de volatilidad implícita)**
```
VIX < 15: calma, régimen favorable para mayoría de estrategias
VIX 15–20: normal
VIX 20–30: volatilidad elevada, reducir tamaño de posiciones
VIX > 30: régimen de crisis, preservar capital
VIX > 40: pánico extremo — históricamente señal de agotamiento de la caída
```

**3. Pendiente de la curva de rendimientos (Yield Curve)**
```
Curva normal (positiva): economía en expansión, riesgo moderado
Curva plana: transición, señal de alerta
Curva invertida (negativa): señal histórica de recesión en 6–18 meses
```

**4. Amplitud de mercado (Market Breadth)**
```
Porcentaje de acciones S&P 500 sobre su MA200:
> 70%: mercado alcista amplio y saludable
50–70%: mercado mixto
< 50%: debilidad interna aunque el índice no lo muestre
< 30%: deterioro severo de amplitud — señal de alerta mayor
```

---

## Protocolo de clasificación para el agente

**Paso 1 — Leer los 4 indicadores primarios**
Obtener via Massive API: precio SPY vs MA50 y MA200, VIX actual.
Obtener via EODHD: datos de yield curve (10Y-2Y spread).

**Paso 2 — Construir score de régimen**
```
Score alcista: +1 por cada condición alcista presente
Score bajista: -1 por cada condición bajista presente
```

Condiciones alcistas: SPY>MA200, VIX<20, yield curve positiva, amplitud>60%
Condiciones bajistas: SPY<MA200, VIX>25, yield curve invertida, amplitud<40%

**Paso 3 — Clasificar**
```
Score +3 a +4: Tendencia alcista fuerte
Score +1 a +2: Tendencia alcista moderada
Score 0: Mercado mixto / lateral
Score -1 a -2: Tendencia bajista moderada
Score -3 a -4: Tendencia bajista fuerte o crisis
```

**Paso 4 — Veredicto de régimen**
Producir:
- Régimen actual: nombre + score
- Duración estimada del régimen actual (días desde que cambió)
- Estrategias más adecuadas para este régimen
- Estrategias a evitar
- Señales a monitorear que indicarían cambio de régimen

---

## Señales de cambio de régimen

Las firmas quant monitorean estos eventos como señales de transición:

| Señal | Qué puede indicar |
|---|---|
| VIX sube > 25% en un solo día | Inicio posible de régimen de stress |
| SPY cruza MA200 (golden/death cross) | Cambio de tendencia mayor |
| Yield curve se invierte | Alerta de recesión futura |
| Amplitud cae < 40% mientras índice sube | Divergencia peligrosa |
| Spread de crédito high yield se amplía > 2% | Estrés en el sistema financiero |

---

## Por qué esto importa para el inversor común

La mayoría de inversores aplican la misma estrategia en todos los mercados.
Las firmas quant adaptan su estrategia al régimen. Esa diferencia explica gran parte
de la diferencia en rendimientos.

No es necesario tener los algoritmos de Jane Street para beneficiarse de esta lógica.
Solo necesitas saber en qué régimen estás antes de tomar cualquier decisión.

---

*Referencias: Hamilton (1989) — Hidden Markov Models para regímenes,
Ang & Bekaert (2002), Lo (2004) — Adaptive Markets Hypothesis.*
