# Comando: /spread-analysis

**Uso:** `/spread-analysis [TICKER]`

**Ejemplo:** `/spread-analysis ICE`

## Qué hace

Ejecuta un análisis completo de microestructura para el ticker indicado:

1. Obtiene precio actual, bid, ask y volumen via Massive.com API
2. Calcula spread absoluto y relativo (% del precio)
3. Compara con ADV histórico de 20 días
4. Clasifica condición de liquidez
5. Estima costo real de transacción (entrada + salida)
6. Detecta señales anómalas en el flujo

## Output

```
🔬 SPREAD ANALYSIS — [TICKER] — [timestamp]

Precio actual:     $XXX.XX
Bid / Ask:         $XXX.XX / $XXX.XX
Spread absoluto:   $X.XX
Spread relativo:   X.XX%

Volumen hoy:       X.XM
ADV 20 días:       X.XM
Ratio vol/ADV:     X.XX (normal / alto / bajo)

💧 CONDICIÓN DE LIQUIDEZ
[Alta / Normal / Reducida / Ilíquida]
[Explicación en 1-2 oraciones]

📊 SEÑAL DE FLUJO
[Comprador / Vendedor / Neutral / Mixto]
[Evidencia observada]

💰 COSTO ESTIMADO DE TRANSACCIÓN
Entrada + salida: X.XX% del precio
Equivalente en $: $X.XX por cada $10,000 operados

⚠️ Datos con ~15min de retraso | Fuente: Massive.com
```

## Notas

- En el free tier de Massive, el bid/ask puede no estar disponible para todos los tickers.
  En ese caso el agente usa el spread estimado basado en volatilidad histórica.
- Para mercados no-USA, usar EODHD como fuente alternativa.
