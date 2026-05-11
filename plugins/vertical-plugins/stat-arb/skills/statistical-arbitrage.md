# Skill: stat-arb (Arbitraje Estadístico)

## Propósito

El arbitraje estadístico es una de las estrategias más usadas por Jane Street, Two Sigma
y Citadel. No requiere predecir el futuro — requiere identificar relaciones matemáticas
entre activos que el mercado temporalmente distorsiona, y esperar a que se corrijan.

Esta skill enseña al agente a encontrar esas relaciones y cuantificar cuándo están rotas.

---

## El principio fundamental

Algunos activos se mueven juntos porque comparten la misma causa económica raíz:
dos bancos del mismo país, dos ETFs del mismo índice, petróleo y acciones de petroleras.

Cuando esa relación se distorsiona temporalmente — uno sube más de lo normal mientras
el otro se queda atrás — existe una oportunidad estadística. No una certeza. Una probabilidad
con un horizonte temporal definido.

**Las firmas quant no apuestan a que el precio suba o baje. Apuestan a que la relación
entre dos precios vuelva a su media histórica.**

---

## Cómo identificar un par válido

### Criterio 1 — Correlación histórica
```
Correlación mínima requerida: > 0.75 (en ventana de 252 días)
```
- Correlación 0.90+: par muy fuerte, relación estable
- Correlación 0.75–0.90: par usable, vigilar con más atención
- Correlación < 0.75: no usar para stat-arb

### Criterio 2 — Cointegración
La correlación sola no es suficiente. Dos activos pueden estar correlacionados
sin estar cointegrados — y solo la cointegración garantiza que la divergencia
eventualmente se corrija.

**Test de Engle-Granger (simplificado):**
Si el precio de A = β × precio de B + error, y ese "error" es estacionario
(vuelve siempre a cero), el par está cointegrado.

En lenguaje simple: si la diferencia entre A y B parece ruidosa pero nunca
se aleja permanentemente, el par es cointegrado y usable.

### Criterio 3 — Half-life de reversión
¿Cuánto tiempo tarda la divergencia en corregirse?
```
Half-life aceptable: 2 a 30 días
```
- < 2 días: requiere ejecución de alta velocidad (no apto para inversor no-HFT)
- 2 a 30 días: ventana manejable para inversor con acceso normal
- > 30 días: la corrección puede tardar demasiado, riesgo de capital atado

---

## Cómo medir la divergencia actual

### El Z-score del spread
```
Spread = Precio_A - (β × Precio_B)
Z-score = (Spread_actual - Media_spread) ÷ Desviación_estándar_spread
```

| Z-score | Señal |
|---|---|
| > +2.0 | A está caro vs B — oportunidad: vender A, comprar B |
| +1.5 a +2.0 | Divergencia moderada — monitorear |
| -1.5 a +1.5 | Relación dentro de rango normal |
| -1.5 a -2.0 | B está caro vs A — monitorear |
| < -2.0 | B está caro vs A — oportunidad: comprar A, vender B |

### Reglas de entrada y salida
- **Entrada**: Z-score supera ±2.0
- **Salida objetivo**: Z-score regresa a 0 (media)
- **Stop-loss**: Z-score supera ±3.5 (la relación puede estar rota)

---

## Pares clásicos por sector

### Infraestructura de mercado (relevante para nuestro análisis de Jane Street)
| Par | Por qué funciona |
|---|---|
| ICE vs CME | Dos bolsas de derivados con exposición similar |
| CBOE vs NDAQ | Infraestructura de opciones vs equities |
| VIRT vs GS (prop trading) | Market making público vs institucional |

### Energía
| Par | Por qué funciona |
|---|---|
| XOM vs CVX | Dos integradas del mismo ciclo de commodity |
| USO vs XLE | ETF de petróleo vs ETF de energía |

### Tecnología
| Par | Por qué funciona |
|---|---|
| MSFT vs GOOGL | Dos plataformas cloud/advertising |
| AMD vs NVDA | Dos fabricantes de semiconductores de alto rendimiento |

### ETFs del mismo índice
| Par | Por qué funciona |
|---|---|
| SPY vs IVV | Dos ETFs del S&P 500 de distintos emisores |
| QQQ vs ONEQ | Dos ETFs del Nasdaq |

*Los ETFs del mismo índice son el caso más limpio: la divergencia casi siempre
se corrige en 1-3 días por mecanismos de arbitraje de los propios emisores.*

---

## Protocolo de análisis para el agente

Cuando el usuario pide analizar un par de activos:

**Paso 1 — Calcular correlación rodante 252 días**
¿Supera 0.75? Si no, descartar y explicar por qué.

**Paso 2 — Calcular spread y su historial**
Construir serie del spread = A - (β × B) usando regresión lineal sobre 252 días.

**Paso 3 — Calcular Z-score actual**
¿Dónde está el spread hoy respecto a su media histórica?

**Paso 4 — Estimar half-life**
¿En cuántos días ha tendido a corregirse históricamente?

**Paso 5 — Veredicto**
Producir:
- Condición del par: Cointegrado / Correlacionado / No relacionado
- Divergencia actual: Z-score con interpretación
- Oportunidad: Sí / Monitorear / No / Par roto
- Horizonte estimado de corrección: X días
- Nivel de confianza: Alto / Medio / Bajo

---

## Lo que esta skill NO puede hacer

- No garantiza que la divergencia se corrija — solo que históricamente lo ha hecho
- No detecta cambios estructurales que rompan la relación permanentemente
  (ejemplo: una empresa que cambia de sector, una fusión, una quiebra)
- No recomienda cuánto capital asignar — eso depende de tu tolerancia al riesgo
- No ejecuta operaciones

---

## Señales de alerta: cuándo el par puede estar roto

- Z-score supera ±4.0 y no regresa en varios días
- Hay una noticia corporativa mayor en uno de los activos del par
- La correlación rodante de 20 días cayó por debajo de 0.50
- El volumen de uno de los activos es anormalmente bajo (liquidez reducida)

---

*Referencias académicas: Engle & Granger (1987), Gatev et al. (2006),
Avellaneda & Lee (2010), Vidyamurthy (2004).*
