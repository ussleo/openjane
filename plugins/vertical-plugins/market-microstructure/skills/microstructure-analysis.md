# Skill: market-microstructure

## Propósito

Esta skill enseña al agente a leer el mercado como lo hace una firma cuantitativa:
no mirando el precio, sino mirando la **estructura** detrás del precio.

Jane Street, Citadel Securities y Hudson River Trading generan la mayor parte de sus ganancias
no prediciendo hacia dónde va el mercado, sino explotando las fricciones en cómo funciona el
mercado en este momento. Esta skill traduce esa lógica a análisis accionable.

---

## Concepto central: el mercado tiene estructura interna

Cada activo cotizado tiene, en cualquier momento dado, cuatro dimensiones que el precio
por sí solo no revela:

1. **Spread bid-ask** — la diferencia entre lo que el mercado paga y lo que cobra
2. **Profundidad de mercado** — cuánto dinero real está esperando a cada precio
3. **Flujo de órdenes** — quién está comprando y vendiendo, y con qué urgencia
4. **Toxicidad del flujo** — si las órdenes entrantes tienen información privilegiada o son ruido

Las firmas cuantitativas viven en estas cuatro dimensiones. El análisis tradicional las ignora.

---

## Cómo analizar el spread bid-ask

### Qué es
El spread es la diferencia entre el precio al que alguien está dispuesto a vender (ask)
y el precio al que alguien está dispuesto a comprar (bid).

**Ejemplo real:**
- Bid: $155.60 (el mercado compra aquí)
- Ask: $155.65 (el mercado vende aquí)
- Spread: $0.05 = 0.032% del precio

### Cómo interpretarlo

| Spread relativo | Señal |
|---|---|
| < 0.05% | Liquidez institucional alta — los market makers compiten agresivamente |
| 0.05% – 0.15% | Normal para acciones de mediana capitalización |
| 0.15% – 0.5% | Liquidez reducida — costo de entrada/salida notable |
| > 0.5% | Mercado ilíquido o estrés — cuidado con el slippage |

### Por qué importa para el inversor común
Si compras con un spread de 0.3% y vendes con otro 0.3%, ya perdiste 0.6% antes de que el
mercado se mueva. En acciones de alta frecuencia esto es irrelevante. En ETFs de nicho,
criptomonedas o acciones de baja capitalización, puede ser tu pérdida más grande.

**Regla práctica:** antes de cualquier operación, verifica que el spread no supere el 0.1%
de tu ganancia esperada mínima. Si esperas ganar 2% y el spread es 0.5%, ya perdiste 25%
de tu ganancia potencial solo en costos de entrada y salida.

---

## Cómo analizar la liquidez

### Qué medir
La liquidez real de un activo se mide con tres indicadores:

**1. Volumen promedio diario (ADV)**
Cuántas acciones/unidades se negocian en un día normal.
- ADV alto = puedes entrar y salir sin mover el precio
- ADV bajo = tu orden puede mover el precio en tu contra

**2. Ratio volumen/capitalización**
```
Liquidez relativa = Volumen diario ÷ Capitalización de mercado
```
- > 0.5%: muy líquido
- 0.1% – 0.5%: líquido normal
- < 0.1%: ilíquido, riesgo de impacto de mercado

**3. Días para liquidar posición**
```
Días para salir = Tamaño de posición ÷ (ADV × 0.10)
```
Regla: no quieras ser más del 10% del volumen diario.
Si necesitas más de 5 días para salir, la posición es demasiado grande para ese activo.

---

## Cómo leer el flujo de órdenes

### El principio
Las órdenes no son iguales. Una orden de $1,000 de un inversor minorista que vio una noticia
es diferente a una orden de $1,000 de un algoritmo cuantitativo que detectó una anomalía.

Las firmas quant intentan distinguir entre:
- **Órdenes informadas**: provienen de alguien con información real sobre el valor del activo
- **Órdenes de ruido**: provienen de inversores reaccionando emocionalmente o siguiendo tendencias

### Señales de flujo informado
- Volumen anormalmente alto antes de un anuncio
- Spread que se amplía justo antes de movimientos grandes
- Compras/ventas sostenidas en una dirección sin noticias visibles
- Opciones out-of-the-money con volumen inusual

### Señal práctica: el indicador VPIN conceptual
```
Presión compradora = Volumen en subidas ÷ Volumen total
Presión vendedora = Volumen en bajadas ÷ Volumen total
Desequilibrio = |Presión compradora - 0.5| × 2
```
- Desequilibrio > 0.3: hay flujo direccional fuerte — algo está pasando
- Desequilibrio < 0.1: mercado equilibrado, rango lateral probable

---

## Cómo aplicar esto al análisis de cualquier activo

### Protocolo de análisis de microestructura

Cuando el agente recibe un ticker para analizar, sigue este orden:

**Paso 1 — Diagnóstico de liquidez**
- ¿Cuál es el ADV de los últimos 20 días?
- ¿El volumen de hoy es normal, alto o bajo vs el promedio?
- ¿El spread actual está dentro del rango histórico normal?

**Paso 2 — Señal de flujo**
- ¿El volumen está concentrado en compras o ventas?
- ¿Hay divergencia entre precio y volumen? (precio sube pero volumen cae = señal débil)
- ¿Hay opciones con actividad inusual?

**Paso 3 — Contexto de mercado**
- ¿El spread se amplió recientemente? (señal de estrés o incertidumbre)
- ¿La liquidez cayó sin razón aparente? (señal de que los market makers se retiraron)
- ¿El activo opera cerca de máximos/mínimos de 52 semanas? (liquidez tiende a cambiar en extremos)

**Paso 4 — Veredicto de microestructura**
El agente produce un veredicto en 3 componentes:
1. **Condición de liquidez**: Alta / Normal / Reducida / Ilíquida
2. **Señal de flujo**: Comprador / Vendedor / Neutral / Mixto
3. **Costo de transacción estimado**: spread + impacto de mercado como % del precio

---

## Ejemplos de interpretación

### Ejemplo A — Ticker líquido saludable (ICE)
- Spread: 0.03% ✅
- ADV: 1.85M acciones, volumen de hoy: normal ✅
- Flujo: equilibrado, sin desequilibrio notable ✅
- **Veredicto**: condiciones óptimas para análisis. Costo de transacción estimado: 0.06%

### Ejemplo B — Ticker con señal de alerta
- Spread: 0.45% ⚠️
- ADV: 200K, volumen de hoy: 3x el promedio ⚠️
- Flujo: 72% vendedor en las últimas 2 horas ⚠️
- **Veredicto**: liquidez bajo presión, flujo vendedor fuerte. Esperar antes de entrar.
  Costo de transacción estimado: 0.9%

---

## Lo que esta skill NO puede hacer

- No predice el precio futuro del activo
- No reemplaza el análisis fundamental (ganancias, deuda, sector)
- No tiene acceso a datos de nivel 2 (order book completo) en el tier gratuito
- No detecta manipulación de mercado — solo señala anomalías estadísticas

---

## Fuentes de datos usados por esta skill

- **Massive.com API**: precios, volumen, bid/ask en tiempo real (delayed 15min en free tier)
- **EODHD API**: históricos, fundamentales, datos globales
- **yfinance**: históricos sin límite para cálculos de ADV y backtesting

---

*Esta skill está basada en investigación académica pública sobre microestructura de mercados.
Referencias: Glosten & Milgrom (1985), Kyle (1985), Easley & O'Hara (1992),
Amihud (2002), Hasbrouck (2007).*
