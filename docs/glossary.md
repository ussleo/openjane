# Glosario OpenJane · Glossary · Glossário

> 28 términos del análisis cuantitativo explicados en lenguaje claro.
> 28 quantitative analysis terms explained in plain language.
> 28 termos de análise quantitativa explicados em linguagem clara.

Cada término incluye: definición · cómo se mide · qué implica · ejemplo real.

---

## Microestructura de mercado / Market Microstructure

### Spread bid-ask
**Definición:** La diferencia entre el precio más alto que un comprador está dispuesto a pagar (bid) y el precio más bajo al que un vendedor está dispuesto a vender (ask). Es el costo invisible más frecuente en cualquier operación de mercado.

**Cómo se mide:** `Spread = Ask − Bid`. En porcentaje: `(Ask − Bid) / Precio medio × 100`

**Qué implica:** Un spread alto significa que pagas más por entrar y recibes menos al salir. Es la comisión que cobra el mercado, no el broker. En activos ilíquidos puede ser tu mayor costo de operación.

**Ejemplo real:** ICE cotiza bid $155.60 / ask $155.65. Spread = $0.05 = 0.032%. Si compras y vendes inmediatamente, pierdes ese 0.032% solo por el spread.

---

### Market maker
**Definición:** Firma o entidad que ofrece simultáneamente precios de compra y venta de un activo, garantizando liquidez al mercado. Ganan la diferencia (spread) entre ambos precios a cambio de asumir el riesgo de inventario.

**Cómo se mide:** Se identifica por su presencia constante en el order book con órdenes a ambos lados del mercado.

**Qué implica:** Jane Street, Citadel Securities y Virtu Financial son los market makers más grandes del mundo. Sin ellos, el mercado sería mucho más caro y difícil de operar.

**Ejemplo real:** Cuando compras acciones de Apple en tu broker, en muchos casos quien te las vende no es otro inversor, sino un market maker que mantiene inventario para ese propósito.

---

### Liquidez
**Definición:** La capacidad de comprar o vender un activo rápidamente sin que el propio acto de comprar/vender cambie significativamente el precio.

**Cómo se mide:** Volumen diario promedio (ADV), ratio volumen/capitalización, spread bid-ask, profundidad del order book.

**Qué implica:** Baja liquidez significa que tu orden puede mover el precio en tu contra antes de ejecutarse. Especialmente crítico en activos pequeños, cripto de nicho o momentos de crisis.

**Ejemplo real:** Apple negocia más de 50 millones de acciones por día. Una empresa pequeña puede negociar solo 50,000 — una orden tuya puede mover su precio.

---

### Flujo de órdenes (Order flow)
**Definición:** El conjunto de órdenes de compra y venta que llegan al mercado en un período dado. Permite detectar si el mercado está siendo presionado por compradores o vendedores, y si ese flujo proviene de inversores informados o de ruido.

**Cómo se mide:** Ratio compras/ventas en tick data. Indicadores como VPIN (Volume-Synchronized Probability of Informed Trading).

**Qué implica:** Las firmas quant pagan millones por acceso a datos de flujo porque es información privilegiada legal: ver quién está comprando y vendiendo antes de que el precio lo refleje.

**Ejemplo real:** Si el 70% del volumen de una acción en la última hora fue a precios del ask (compras agresivas), hay presión compradora fuerte — algo puede estar ocurriendo antes de la noticia.

---

### Volatilidad implícita
**Definición:** La volatilidad esperada por el mercado para un activo en el futuro, derivada matemáticamente del precio de sus opciones. No es la volatilidad pasada — es lo que el mercado colectivamente cree que pasará.

**Cómo se mide:** Se invierte el modelo Black-Scholes: dado el precio de una opción, se calcula qué volatilidad produce ese precio.

**Qué implica:** Cuando la volatilidad implícita es mucho mayor que la histórica, el mercado está pagando mucho por protección. Las firmas quant venden esa volatilidad cara y compran la historia barata.

**Ejemplo real:** Antes de resultados de una empresa, las opciones suben de precio aunque el subyacente no se mueva. El mercado anticipa un movimiento grande en cualquier dirección.

---

## Arbitraje estadístico / Statistical Arbitrage

### Arbitraje estadístico (Stat-arb)
**Definición:** Estrategia cuantitativa que explota divergencias temporales en la relación histórica entre dos o más activos cointegrados. No apuesta a que el precio suba o baje — apuesta a que la relación entre dos precios vuelva a su media histórica.

**Cómo se mide:** Identificar par cointegrado → calcular spread histórico → detectar Z-score extremo → entrar cuando Z > ±2.0 → salir cuando Z regresa a 0.

**Qué implica:** Es market-neutral: si el mercado entero cae, tu posición larga y corta simultánea se protegen mutuamente. El riesgo principal es que la relación entre los dos activos se rompa permanentemente.

**Ejemplo real:** ICE sube 5% por una noticia positiva pero CBOE no se mueve. Históricamente se mueven juntos. Vendes ICE y compras CBOE esperando que la divergencia se corrija. Eso es stat-arb.

---

### Cointegración
**Definición:** Relación matemática entre dos activos donde, aunque ambos se mueven de forma aleatoria, su diferencia tiende siempre a volver a un valor medio. Es más fuerte que la correlación: garantiza que las divergencias se corrijan.

**Cómo se mide:** Test de Engle-Granger o Johansen. Se verifica que el spread entre los dos activos sea estacionario (sin tendencia, con media constante).

**Qué implica:** La cointegración es la base matemática del arbitraje estadístico. Sin ella, la relación entre dos activos puede desaparecer permanentemente.

**Ejemplo real:** SPY e IVV (dos ETFs del S&P 500 de distintas gestoras) están cointegrados: si uno se separa del otro, los mecanismos de arbitraje lo corrigen en minutos.

---

### Z-score
**Definición:** Medida estadística que indica cuántas desviaciones estándar está un valor alejado de su media histórica. En arbitraje estadístico, mide qué tan anormal es la divergencia actual entre dos activos.

**Cómo se mide:** `Z-score = (Valor actual − Media histórica) ÷ Desviación estándar`

**Qué implica:** Un Z-score de +2.0 significa que la divergencia es 2 veces la variación normal histórica. Las firmas quant usan ±2.0 como señal de entrada y 0 como objetivo de salida.

**Ejemplo real:** Si el spread entre ICE y CBOE tiene media $10 y desviación $2, y hoy el spread es $14, el Z-score = (14−10)/2 = +2.0. ICE está caro relativo a CBOE.

---

### Correlación
**Definición:** Medida estadística entre -1 y +1 que indica qué tan sincronizados se mueven dos activos. +1 = se mueven perfectamente juntos. -1 = dirección opuesta. 0 = sin relación.

**Cómo se mide:** Coeficiente de Pearson sobre los retornos diarios en una ventana histórica (típicamente 252 días hábiles = 1 año).

**Qué implica:** Correlación alta es condición necesaria pero no suficiente para stat-arb. Dos activos pueden estar correlacionados sin estar cointegrados.

**Ejemplo real:** XOM y CVX tienen correlación ~0.92 porque ambas suben y bajan con el precio del petróleo. Pero su correlación puede caer si una tiene un problema específico de empresa.

---

### Half-life de reversión
**Definición:** El tiempo promedio que tarda una divergencia entre dos activos en reducirse a la mitad. Mide qué tan rápido el mercado corrige la anomalía estadística que se está explotando.

**Cómo se mide:** Se estima con regresión de Ornstein-Uhlenbeck sobre la serie del spread.

**Qué implica:** Half-life < 2 días requiere ejecución automatizada de alta velocidad. Entre 2 y 30 días es manejable para un inversor con acceso normal. Más de 60 días ata capital demasiado tiempo.

**Ejemplo real:** Si el spread entre dos ETFs del mismo índice tiene un half-life de 1 día, solo firmas HFT pueden explotarlo. Si es de 15 días, un inversor normal puede participar.

---

## Régimen de mercado / Market Regime

### Régimen de mercado
**Definición:** El estado estructural del mercado en un momento dado. Los mercados alternan entre tendencia alcista, bajista, lateralidad y crisis. Cada régimen favorece diferentes estrategias.

**Cómo se mide:** Combinación de indicadores: posición respecto a medias móviles (MA50, MA200), VIX, amplitud de mercado, curva de rendimientos.

**Qué implica:** La misma estrategia que genera ganancias en un régimen puede destruir capital en otro. Las firmas quant adaptan sus estrategias al régimen — los inversores tradicionales generalmente no lo hacen.

**Ejemplo real:** Una estrategia de comprar caídas funciona bien en tendencia alcista. En mercado bajista, cada caída puede llevar a otra mayor.

---

### VIX
**Definición:** Índice de volatilidad del mercado calculado por CBOE a partir de opciones del S&P 500. Mide la volatilidad esperada para los próximos 30 días. Conocido como el índice del miedo.

**Cómo se mide:** Es un índice directo: VIX = 18 significa que el mercado espera movimientos anualizados del 18%, equivalente a ~1.1% diario.

**Qué implica:** VIX < 15: calma. VIX 15-25: normal. VIX > 30: miedo y mercado estresado. VIX > 40: pánico — históricamente señal de agotamiento de la caída.

**Ejemplo real:** Durante COVID en marzo 2020, el VIX llegó a 82. En mercados normales ronda 15-20. Cuando el VIX sube abruptamente, todos los spreads se amplían y la liquidez se retira.

---

### Media móvil (MA)
**Definición:** El promedio del precio de cierre de un activo durante los últimos N días. Suaviza el ruido diario y revela la tendencia subyacente. Las más usadas son MA50 y MA200.

**Cómo se mide:** `MA(N) = suma de los últimos N precios de cierre ÷ N`. Se recalcula cada día.

**Qué implica:** MA200 es el indicador de tendencia más seguido por instituciones. Precio sobre MA200 = tendencia alcista de largo plazo. Precio bajo MA200 = tendencia bajista.

**Ejemplo real:** Si SPY está a $520 y su MA200 está a $495, el mercado está en tendencia alcista sana. Si SPY cae a $490, cruzó por debajo de la MA200 — señal de alerta mayor.

---

### Amplitud de mercado (Market breadth)
**Definición:** Medida de cuántas acciones dentro de un índice participan de su movimiento. Un índice puede subir aunque la mayoría de sus acciones bajen si unas pocas muy grandes suben mucho.

**Cómo se mide:** Porcentaje de acciones del S&P 500 sobre su MA200. También: línea Avance-Descenso.

**Qué implica:** Amplitud > 70%: alza sana. Amplitud < 40% con índice alto: señal de alerta — el rally lo llevan pocas acciones y es frágil.

**Ejemplo real:** El S&P 500 sube 1% pero 300 de sus 500 acciones están bajando. Solo 10 acciones muy grandes compensan todo. Eso es baja amplitud — el rally es frágil.

---

### Curva de rendimientos (Yield curve)
**Definición:** Representación gráfica de las tasas de interés de bonos del gobierno a distintos plazos. Normalmente los bonos a largo plazo pagan más. Cuando se invierte (corto paga más que largo), históricamente precede recesiones.

**Cómo se mide:** Spread 10Y-2Y: tasa del bono a 10 años menos la del bono a 2 años. Positivo = normal. Negativo = invertida.

**Qué implica:** La curva invertida precedió todas las recesiones de EEUU en los últimos 50 años. El tiempo entre inversión y recesión varía de 6 a 24 meses.

**Ejemplo real:** En 2022-2023, la curva 10Y-2Y estuvo invertida durante meses. Muchos esperaban recesión en 2024 — no llegó. La señal fue real pero el timing fue incierto.

---

## Riesgo y ejecución / Risk and Execution

### Slippage
**Definición:** La diferencia entre el precio al que esperabas ejecutar una orden y el precio al que realmente se ejecutó. Ocurre porque el mercado se mueve mientras tu orden se procesa, o porque tu propia orden mueve el precio.

**Cómo se mide:** `Slippage = Precio ejecutado − Precio esperado`. En %: `(Ejecutado − Esperado) / Esperado × 100`

**Qué implica:** En órdenes pequeñas de activos líquidos es mínimo. En órdenes grandes o activos ilíquidos puede costar más que la comisión del broker. Es el costo oculto más subestimado.

**Ejemplo real:** Quieres comprar 1,000 acciones a $100. Las primeras 200 se ejecutan a $100, las siguientes a $100.05, las últimas a $100.12. Tu precio promedio real fue $100.08 — eso es slippage.

---

### Impacto de mercado (Market impact)
**Definición:** El efecto que tiene tu propia orden sobre el precio del activo. Cuando compras en cantidad, empujas el precio hacia arriba contra ti mismo.

**Cómo se mide:** Modelos como Almgren-Chriss calculan el impacto óptimo distribuyendo órdenes en el tiempo.

**Qué implica:** Jane Street dedica equipos enteros a minimizar el impacto de sus propias órdenes. Para un inversor normal con órdenes pequeñas, es irrelevante. Para fondos grandes, puede costar millones.

**Ejemplo real:** Un fondo quiere comprar el 5% de las acciones de una empresa en un día. Solo ese intento subirá el precio antes de que terminen — pagando más por las últimas que por las primeras.

---

### Drawdown
**Definición:** La caída máxima desde un pico de valor hasta el valle más bajo subsecuente, antes de recuperarse. Es la medida más importante del riesgo real que experimenta un inversor.

**Cómo se mide:** `Max Drawdown = (Valor mínimo − Valor máximo previo) ÷ Valor máximo previo × 100`

**Qué implica:** Un drawdown del 30% requiere un retorno del 43% solo para recuperarse. Por eso las firmas quant son obsesivas con limitar drawdowns — no es solo psicológico, es matemático.

**Ejemplo real:** Tu portafolio vale $100,000, sube a $120,000 y cae a $84,000. Drawdown = (84,000−120,000)/120,000 = −30%. Necesitas subir 43% desde $84,000 para volver al pico.

---

### TWAP
**Definición:** Time-Weighted Average Price. Estrategia de ejecución que divide una orden grande en partes iguales distribuidas uniformemente en el tiempo, para reducir el impacto de mercado.

**Cómo se mide:** Orden total ÷ número de intervalos de tiempo = tamaño de cada orden parcial.

**Qué implica:** Es la estrategia de ejecución más simple y transparente. Los fondos la usan cuando necesitan demostrar que no manipularon el precio.

**Ejemplo real:** Un fondo necesita comprar $10M de acciones en un día. En vez de hacerlo todo de una vez, lo divide en 24 órdenes de $417,000 cada 30 minutos.

---

### VWAP
**Definición:** Volume-Weighted Average Price. Precio promedio ponderado por volumen durante un período. Es el benchmark de ejecución más usado por instituciones.

**Cómo se mide:** `VWAP = Suma(Precio × Volumen de cada transacción) ÷ Volumen total del período`

**Qué implica:** Comprar por debajo del VWAP = buena ejecución. Comprar por encima = pagaste más que el precio promedio del mercado ese día.

**Ejemplo real:** El VWAP de ICE hoy fue $155.50. Si tu broker ejecutó a $155.30, ejecutó 0.13% mejor que el mercado. Si ejecutó a $155.70, fue 0.13% peor.

---

## Datos y métricas / Data and Metrics

### ADV (Average Daily Volume)
**Definición:** Volumen diario promedio: la cantidad de acciones negociadas en un día típico, calculada como promedio de los últimos 20 o 30 días. Es la referencia base para medir liquidez.

**Cómo se mide:** `ADV = suma del volumen de los últimos N días ÷ N` (típicamente N = 20 días hábiles)

**Qué implica:** Regla práctica: nunca quieras ser más del 10% del ADV en una sola sesión. Si el ADV es 1M y quieres comprar 500,000 acciones, necesitas varios días para entrar sin impactar el precio.

**Ejemplo real:** ICE tiene un ADV de ~1.85M acciones. Para un inversor retail comprando 100 acciones, irrelevante. Para un fondo comprando 500,000, necesita distribuir la orden en varios días.

---

### Sharpe ratio
**Definición:** Medida del retorno ajustado por riesgo de una estrategia. Indica cuánto retorno obtienes por cada unidad de riesgo que asumes. Creado por William Sharpe, Premio Nobel de Economía.

**Cómo se mide:** `Sharpe = (Retorno promedio − Tasa libre de riesgo) ÷ Desviación estándar de los retornos`

**Qué implica:** Sharpe < 0.5: débil. 0.5-1.0: aceptable. 1.0-2.0: buena. > 2.0: excelente (y sospechoso si viene solo de backtesting).

**Ejemplo real:** Tu estrategia gana 15% anual con volatilidad del 10%, tasa libre de riesgo al 5%. Sharpe = (15%-5%)/10% = 1.0. Buena estrategia para ese nivel de riesgo.

---

### Backtesting
**Definición:** Proceso de probar una estrategia sobre datos históricos para evaluar cómo habría funcionado en el pasado. Método estándar para validar una estrategia antes de arriesgar capital real.

**Cómo se mide:** Aplicar reglas de la estrategia sobre datos históricos, registrar cada operación simulada, calcular retornos, drawdown, Sharpe ratio.

**Qué implica:** Riesgo principal: overfitting — ajustar la estrategia hasta que funcione perfectamente en el pasado sin que funcione en el futuro. Una buena estrategia debe validarse en datos NO usados para diseñarla.

**Ejemplo real:** Diseñas stat-arb entre ICE y CBOE usando datos 2015-2020, y validas con datos 2020-2024 que nunca usaste. Si funciona en ambos períodos, es más robusta.

---

### MCP (Model Context Protocol)
**Definición:** Protocolo estándar creado por Anthropic que permite conectar modelos de lenguaje (como Claude) con herramientas y fuentes de datos externas. En OpenJane, MCP conecta el agente con Massive.com y EODHD.

**Cómo se mide:** Se configura en `.mcp.json` con la URL del servidor y la API key.

**Qué implica:** Gracias a MCP, el usuario no necesita programar para acceder a datos de mercado. El agente habla con los datos en nombre del usuario.

**Ejemplo real:** Escribes `/spread-analysis ICE` y el agente, via MCP, llama a Massive.com, obtiene bid/ask y volumen actuales, los procesa y te entrega el análisis en español.

---

### API key
**Definición:** Código único que identifica a tu usuario ante un servicio de datos externo. Como una contraseña personalizada que permite al agente hacer solicitudes de datos en tu nombre.

**Cómo se mide:** Se obtiene registrándose en el sitio del proveedor. Se almacena como variable de entorno.

**Qué implica:** Nunca compartas tu API key públicamente. En OpenJane va en el archivo `.env` como variable de entorno, nunca en código expuesto en el repo.

**Ejemplo real:** Te registras en massive.com, recibes una key como `pk_abc123xyz`. La añades a tu `.env` y el agente puede hacer hasta 5 llamadas por minuto a datos de mercado.

---

## Conceptos generales / General Concepts

### Ticker
**Definición:** El código abreviado que identifica a un activo en los mercados financieros. Cada acción, ETF o instrumento negociable tiene un ticker único en cada exchange.

**Cómo se mide:** Es simplemente el símbolo: ICE, CBOE, VIRT, SPY, BTC-USD.

**Ejemplo real:** ICE = Intercontinental Exchange. CBOE = Cboe Global Markets. VIRT = Virtu Financial. SPY = ETF del S&P 500.

---

### ETF (Exchange-Traded Fund)
**Definición:** Fondo de inversión que cotiza en bolsa como una acción. Replica el desempeño de un índice, sector o activo. Combina diversificación con facilidad de compra/venta.

**Cómo se mide:** Se compra y vende igual que una acción, con el mismo ticker. El precio cambia durante el día.

**Qué implica:** Los ETFs del mismo índice son el caso más limpio de cointegración — su precio no puede divergir mucho porque los mecanismos de arbitraje lo corrigen automáticamente.

**Ejemplo real:** SPY e IVV replican exactamente el mismo índice (S&P 500) pero de distintas gestoras. Si su diferencia de precio se sale de lo normal, los arbitrajistas la corrigen en minutos.

---

### Ghost ticker
**Definición:** Término de OpenJane para un activo cotizado que se mueve de forma estadísticamente similar a una firma privada (como Jane Street) sin tener relación directa con ella. Sirve como proxy de comportamiento.

**Cómo se mide:** Comparando patrones de correlación, sensibilidad a volatilidad y comportamiento en distintos regímenes de mercado.

**Qué implica:** CBOE e ICE son los mejores ghost tickers de Jane Street: se benefician de la misma volatilidad y estructura de mercado que alimenta las ganancias de Jane Street, pero son públicos y observables.

**Ejemplo real:** Jane Street no cotiza. Pero CBOE cotiza y su precio sube cuando la volatilidad aumenta — igual que probablemente las ganancias de Jane Street. CBOE es el fantasma público de una firma privada.

---

### HFT (High-Frequency Trading)
**Definición:** Trading de alta frecuencia: estrategias completamente automatizadas que ejecutan miles de operaciones por segundo, aprovechando ventajas de latencia medidas en microsegundos.

**Cómo se mide:** Latencia en microsegundos. Servidores co-ubicados físicamente en los edificios de los exchanges.

**Qué implica:** HFT es el nivel donde operan Jane Street, Citadel y Virtu. Es completamente inaccesible para inversores individuales por costo de infraestructura. OpenJane replica la lógica conceptual, no la velocidad.

**Ejemplo real:** Cuando el S&P 500 cae 0.1% en Chicago, los HFTs ajustan los precios de miles de acciones relacionadas en Nueva York en microsegundos — antes de que cualquier humano pueda reaccionar.

---

*OpenJane · by Claude · Apache 2.0 · github.com/ussleo/openjane*
