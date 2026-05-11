# OpenJane · by Claude

> **"Jane Street no gana prediciendo el futuro. Gana optimizando fricción, liquidez y ejecución a escala masiva con una cultura técnica obsesiva."**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude%20Code-orange.svg)](https://claude.ai/code)
[![Live on Render](https://img.shields.io/badge/Live-Render.com-green.svg)](https://openjane.onrender.com)
[![GitHub Pages](https://img.shields.io/badge/Landing-GitHub%20Pages-blue.svg)](https://ussleo.github.io/openjane/)
[![Data: EODHD](https://img.shields.io/badge/Data-EODHD-green.svg)](https://eodhd.com)
[![Data: Massive.com](https://img.shields.io/badge/Data-Massive.com-green.svg)](https://massive.com)

---

## 🌎 Léeme en tu idioma / Read in your language / Leia no seu idioma

- [🇪🇸 Español](#-español)
- [🇺🇸 English](#-english)
- [🇧🇷 Português (Brasil)](#-português-brasil)

---

# 🇪🇸 Español

## Lo que se construyó

**OpenJane pasó de idea a producción en una sola sesión de trabajo con Claude Code.**

No es un proyecto de meses ni de un equipo. Es la demostración práctica de lo que un desarrollador con Claude puede construir en horas — con calidad de producción, seguro, desplegado y documentado.

---

## Mapa completo de páginas y endpoints

### Páginas públicas

| Página | URL GitHub Pages | URL Render | Descripción |
|---|---|---|---|
| **Landing trilingüe** | [/](https://ussleo.github.io/openjane/) | [/](https://openjane.onrender.com/) | ES/EN/PT con auto-detect, globo animado, CTAs |
| **Analizar en vivo** | [/analyze](https://ussleo.github.io/openjane/analyze.html) | [/analyze](https://openjane.onrender.com/analyze) | Análisis de régimen, microestructura y stat-arb |
| **📊 Backtester histórico** | [/backtester](https://ussleo.github.io/openjane/backtester.html) | [/backtester](https://openjane.onrender.com/backtester) | P&L histórico con fechas, ventana rodante, CSV export |
| **🎯 Teatro de Operaciones** | [/portfolio](https://ussleo.github.io/openjane/portfolio.html) | [/portfolio](https://openjane.onrender.com/portfolio) | Paper trading con $100 virtuales, P&L real EOD |
| **Educación** | [/paper-trading-edu](https://ussleo.github.io/openjane/paper-trading-edu.html) | [/paper-trading-edu](https://openjane.onrender.com/paper-trading-edu) | Cómo gana Jane Street: spread, escala, estrategias |
| **Claude Setup** | [/claude-setup](https://ussleo.github.io/openjane/claude-setup.html) | [/claude-setup](https://openjane.onrender.com/claude-setup) | Guía para usar Jane en Claude.ai Projects gratis |
| **Glosario** | [/glossary](https://ussleo.github.io/openjane/glossary.html) | [/glossary](https://openjane.onrender.com/glossary) | 35+ términos de quant finance explicados |
| **API Keys** | [/api-keys](https://ussleo.github.io/openjane/api-keys.html) | [/api-keys](https://openjane.onrender.com/api-keys) | Guía paso a paso para obtener keys gratuitas |

### API endpoints (Render.com)

| Método | Endpoint | Keys necesarias | Descripción |
|---|---|---|---|
| `GET` | `/api/health` | — | Healthcheck del servidor |
| `POST` | `/api/regime` | Massive + EODHD | Régimen de mercado global (score 0-4) |
| `POST` | `/api/microstructure` | Massive + EODHD | Microestructura de un ticker |
| `POST` | `/api/statarb` | EODHD | Stat-arb entre dos tickers (Z-score, half-life) |
| `POST` | `/api/portfolio-snapshot` | EODHD | Precio EOD actual de N tickers (Teatro) |
| `POST` | `/api/backtest` | EODHD | P&L histórico completo con serie diaria (Backtester) |

---

## Las tres rutas para el usuario

**Ruta 1 — Cero fricción (Claude.ai)**
→ [openjane.onrender.com/claude-setup](https://openjane.onrender.com/claude-setup)

Sin API keys. Sin instalar. Sin formularios. El usuario crea un Project en claude.ai, pega el system prompt con un clic, y habla con Jane en lenguaje natural. Jane responde con el formato quant completo y aclara siempre cuándo no tiene datos en vivo.

**Ruta 2 — Datos reales (Render)**
→ [openjane.onrender.com/analyze](https://openjane.onrender.com/analyze)

El usuario ingresa sus propias API keys gratuitas de Massive.com y EODHD. La plataforma corre análisis en tiempo real (EOD): régimen de mercado, microestructura, stat-arb. Las keys nunca se almacenan.

**Ruta 3 — Deploy propio (Docker)**
```bash
git clone https://github.com/ussleo/openjane
docker build -t openjane .
docker run -p 8000:8000 openjane
```

---

## Las herramientas de aprendizaje

### 📊 Backtester histórico (`/backtester`)

```
Input:  EODHD key · tickers · $$ virtuales · fecha inicio · fecha fin
Output: P&L por ticker · valor final · drawdown máximo · serie diaria · CSV descargable

Ejemplo:
  ICE $30 + CBOE $25 + VIRT $20 + SPY $25 · 2025-01-02 → 2025-04-30
  Jane responde en segundos con el resultado real de esos 87 días hábiles.
```

Botones de ventana rápida: 30 días · 3 meses · 6 meses · 1 año · 2 años.
Distribución igual automática ($100 o $1000 en partes iguales entre tickers).
Gráfico de evolución día a día con Chart.js. CSV exportable con serie completa.

### 🎯 Teatro de Operaciones (`/portfolio`)

```
Input:  EODHD key · tickers · $$ virtuales por ticker
Output: Snapshot de entrada (precio EOD actual) → P&L al evaluar días después

Flujo:
  1. Hoy: "Abrir posición" → Jane obtiene precios actuales → guarda en localStorage
  2. Mañana: "Evaluar P&L" → Jane compara con nuevos precios → resultado real
  3. Historial de evaluaciones con timestamps
  4. "Copiar resultado" para compartir
```

Sin servidor involucrado — todo el estado vive en localStorage del browser.
Los precios EOD se actualizan una vez al día después del cierre de mercado.

### 📚 Educación (`/paper-trading-edu`)

7 secciones con SVGs explicativos:
- El secreto del centavo: $0.02 × 50M transacciones = $1M/día
- La magia de la escala
- Paper trading vs trading real
- Backtesting con ventana rodante
- Teatro de operaciones con ejemplo ($100 en ICE/CBOE/VIRT/SPY)
- Estrategias de Jane Street: ETF Arbitrage, Index Rebalancing, Stat-Arb, Cross-venue, Options MM, Regime-Based
- Glosario visceral de 12 términos

---

## El stack completo

```
GitHub (source of truth)
├── docs/                    → GitHub Pages (frontend estático)
│   ├── index.html           ← Landing trilingüe ES/EN/PT
│   ├── analyze.html         ← Análisis en vivo
│   ├── backtester.html      ← Backtester histórico
│   ├── portfolio.html       ← Teatro de Operaciones
│   ├── paper-trading-edu.html ← Educación
│   ├── claude-setup.html    ← Setup en Claude.ai
│   ├── glossary.html        ← Glosario 35+ términos
│   └── api-keys.html        ← Guía de API keys
│
└── app/
    └── main.py              → Render.com (FastAPI + uvicorn + Docker)
        ├── GET  /api/health
        ├── POST /api/regime
        ├── POST /api/microstructure
        ├── POST /api/statarb
        ├── POST /api/portfolio-snapshot
        └── POST /api/backtest
```

---

## De dónde viene esto

**OpenJane nació de una investigación profunda sobre Jane Street Capital.**

Jane Street generó aproximadamente **$39 mil millones en 2024** — más que Goldman Sachs en ese mismo concepto. No cotiza en bolsa. No hace publicidad. Y sin embargo es posiblemente la firma más influyente en la microestructura de los mercados financieros modernos.

**La conclusión fue clara: la lógica detrás de esos $39 mil millones no es magia. Es matemática, datos y cultura técnica obsesiva. Y puede documentarse y ponerse al alcance de cualquier persona.**

### Ghost tickers — los proxies públicos de Jane Street

| Ticker | Empresa | Por qué es un ghost ticker |
|---|---|---|
| **CBOE** | Cboe Global Markets | Proxy más cercano: opciones, vol, microestructura |
| **ICE** | Intercontinental Exchange | Proxy sistémico e infraestructural |
| **VIRT** | Virtu Financial | Market making público, comparable directo |
| **NDAQ** | Nasdaq | Market structure e infraestructura |
| **MKTX** | MarketAxess | Liquidez electrónica en renta fija institucional |

### Modelos implementados

| Modelo | Aplicación |
|---|---|
| OLS regression + Z-score | Stat-arb: calibración de spread y señal de entrada |
| Ornstein-Uhlenbeck | Half-life de reversión a la media |
| Volatilidad histórica (log-returns) | HV 20d anualizada |
| Drawdown máximo | Backtester: riesgo histórico por ticker |

---

## Arquitectura de seguridad

| Amenaza | Mitigación implementada |
|---|---|
| **Prompt injection vía ticker** | Regex `^[A-Z0-9.\-]{1,12}$` — 422 en cualquier otro formato |
| **Crossover de keys entre requests concurrentes** | Clientes HTTP instanciados por request, sin `os.environ` global |
| **API flooding** | Rate limiting 10 req/60s por IP real (X-Forwarded-For) |
| **Keys expuestas en logs** | Error messages truncados a 200 chars, keys nunca se loguean |
| **Inyección de paths en URLs externas** | Tickers validados antes de construir cualquier URL |
| **CORS abierto** | Orígenes permitidos explícitos (GitHub Pages + Render) |
| **Payloads masivos** | Validación de longitud en API keys (8-200 chars) |

**El servidor no almacena nada.** Sin base de datos. Sin sesiones. Sin cookies. Sin persistencia.
Ver [`SECURITY.md`](SECURITY.md) para el modelo completo.

---

## Datos de mercado — completamente gratuitos

| Proveedor | Qué aporta | Usado en |
|---|---|---|
| [Massive.com](https://massive.com) | Precios EOD, volumen OHLCV, VWAP | `/api/regime`, `/api/microstructure` |
| [EODHD](https://eodhd.com) | MA50/MA200, HV, yield curve, histórico completo | Todos los endpoints, Backtester, Teatro |

Ambos gratuitos. Sin tarjeta de crédito.
→ [Guía paso a paso para obtener ambas keys](https://openjane.onrender.com/api-keys)

---

## Estructura del repositorio

```
openjane/
├── app/
│   ├── main.py              ← FastAPI server (thread-safe, validado, seguro)
│   └── requirements.txt     ← fastapi, uvicorn, python-dotenv
│
├── docs/                    ← GitHub Pages (frontend completo)
│   ├── index.html
│   ├── analyze.html
│   ├── backtester.html      ← NUEVO v1
│   ├── portfolio.html       ← NUEVO v1
│   ├── paper-trading-edu.html ← NUEVO v1
│   ├── claude-setup.html
│   ├── glossary.html
│   ├── api-keys.html
│   └── screenshots/
│
├── plugins/
│   └── vertical-plugins/    ← Skills de análisis cuantitativo
│
├── Dockerfile               ← Python 3.12-slim
├── render.yaml              ← Configuración Render.com free tier
├── SECURITY.md              ← Modelo de seguridad completo
└── README.md
```

---

## API Reference

**Base URL:** `https://openjane.onrender.com`  
**Rate limit:** 10 requests / 60 segundos por IP  
**Validación de tickers:** `^[A-Z0-9.\-]{1,12}$`

### POST /api/regime
```json
{ "massive_key": "...", "eodhd_key": "..." }
```
Respuesta: score 0-4, clasificación ALCISTA/BAJISTA/TRANSICIÓN, SPY MA50/MA200, HV 20d, yield curve.

### POST /api/microstructure
```json
{ "massive_key": "...", "eodhd_key": "...", "ticker": "ICE" }
```
Respuesta: precio EOD, VWAP, ADV, rango intraday, liquidez, tendencia, HV 20d.

### POST /api/statarb
```json
{ "massive_key": "...", "eodhd_key": "...", "ticker_a": "ICE", "ticker_b": "CBOE" }
```
Respuesta: correlación, beta, Z-score, half-life, entrada/stop/salida, señal LONG/SHORT/NEUTRAL.

### POST /api/portfolio-snapshot
```json
{ "eodhd_key": "...", "tickers": ["ICE", "CBOE", "VIRT", "SPY"] }
```
Respuesta: precio EOD más reciente por ticker con fecha. Usado por el Teatro de Operaciones.

### POST /api/backtest
```json
{
  "eodhd_key": "...",
  "positions": [
    { "ticker": "ICE", "invested": 30 },
    { "ticker": "CBOE", "invested": 25 }
  ],
  "date_from": "2025-01-02",
  "date_to": "2025-04-30"
}
```
Respuesta: P&L por ticker, valor final, drawdown máximo, serie diaria completa para gráfico.

### GET /api/health
```json
{ "status": "ok", "service": "OpenJane" }
```

---

## Comandos del agente (Claude.ai)

| Comando | Acción |
|---|---|
| `/regime` | Régimen actual del mercado (score 0-4 + clasificación) |
| `/spread-analysis [TICKER]` | Microestructura completa: spread, liquidez, ADV, flujo |
| `/stat-arb [A] [B]` | Par estadístico: correlación, Z-score, half-life, señal |
| `/vol-surface [TICKER]` | IV vs HV, skew, estructura temporal, prima de vol |
| `/help` | Menú de comandos |

---

## Contribuir

Todo es código abierto bajo Apache 2.0.

- **Nueva skill:** `plugins/vertical-plugins/<vertical>/skills/`
- **Corrección o mejora:** abre un issue o PR en GitHub
- **Traducción:** el glosario y las páginas te esperan
- **Reporte de seguridad:** ver [`SECURITY.md`](SECURITY.md)

---

# 🇺🇸 English

## What was built

**OpenJane went from idea to production in a single working session with Claude Code.**

### Full page map

| Page | URL | Description |
|---|---|---|
| **Trilingual landing** | [/](https://ussleo.github.io/openjane/) | ES/EN/PT auto-detect, globe switcher |
| **Live analysis** | [/analyze](https://openjane.onrender.com/analyze) | Regime, microstructure, stat-arb |
| **📊 Historical Backtester** | [/backtester](https://openjane.onrender.com/backtester) | P&L with date range, CSV export |
| **🎯 Operations Theater** | [/portfolio](https://openjane.onrender.com/portfolio) | Paper trading, real EOD P&L |
| **Education** | [/paper-trading-edu](https://openjane.onrender.com/paper-trading-edu) | How Jane Street makes money |
| **Claude Setup** | [/claude-setup](https://openjane.onrender.com/claude-setup) | Use Jane in Claude.ai for free |
| **Glossary** | [/glossary](https://openjane.onrender.com/glossary) | 35+ quant finance terms |

### Three paths for the user

**Path 1 — Zero friction (Claude.ai)**  
No API keys. No install. Create a Project on claude.ai, paste the system prompt, talk to Jane.

**Path 2 — Real data (Render)**  
Enter free API keys from Massive.com and EODHD. Live EOD analysis. Keys never stored.

**Path 3 — Self-host (Docker)**
```bash
git clone https://github.com/ussleo/openjane
docker build -t openjane . && docker run -p 8000:8000 openjane
```

### Security architecture

| Threat | Mitigation |
|---|---|
| Prompt injection via ticker | Strict regex `^[A-Z0-9.\-]{1,12}$` — 422 on mismatch |
| Key crossover between concurrent requests | HTTP clients instantiated per-request, no global state |
| API flooding | Rate limit: 10 req/60s per real IP (X-Forwarded-For) |
| Keys in logs | Error messages capped at 200 chars, keys never logged |
| Open CORS | Explicit allowed origins (GitHub Pages + Render) |

**The server stores nothing.** No database. No sessions. No cookies.  
See [`SECURITY.md`](SECURITY.md) for the full model.

### Ghost tickers

| Ticker | Company | Why it's a ghost ticker |
|---|---|---|
| **CBOE** | Cboe Global Markets | Closest proxy: options, vol, microstructure |
| **ICE** | Intercontinental Exchange | Systemic infrastructure proxy |
| **VIRT** | Virtu Financial | Public market maker, direct comparable |

### Free market data

| Provider | What it contributes | Credit card |
|---|---|---|
| [Massive.com](https://massive.com) | EOD prices, volume, OHLCV | ❌ None |
| [EODHD](https://eodhd.com) | MA50/200, HV, yield curve, 150k+ tickers | ❌ None |

---

# 🇧🇷 Português (Brasil)

## O que foi construído

**O OpenJane foi de ideia à produção em uma única sessão de trabalho com o Claude Code.**

### Mapa completo de páginas

| Página | URL | Descrição |
|---|---|---|
| **Landing trilíngue** | [/](https://ussleo.github.io/openjane/) | ES/EN/PT com detecção automática |
| **Análise ao vivo** | [/analyze](https://openjane.onrender.com/analyze) | Regime, microestrutura, stat-arb |
| **📊 Backtester Histórico** | [/backtester](https://openjane.onrender.com/backtester) | P&L com intervalo de datas, export CSV |
| **🎯 Teatro de Operações** | [/portfolio](https://openjane.onrender.com/portfolio) | Paper trading, P&L real EOD |
| **Educação** | [/paper-trading-edu](https://openjane.onrender.com/paper-trading-edu) | Como a Jane Street ganha dinheiro |
| **Claude Setup** | [/claude-setup](https://openjane.onrender.com/claude-setup) | Use a Jane no Claude.ai de graça |
| **Glossário** | [/glossary](https://openjane.onrender.com/glossary) | 35+ termos de finanças quant |

### Três caminhos para o usuário

**Caminho 1 — Zero fricção (Claude.ai)**  
Sem API keys. Sem instalar. Crie um Project no claude.ai, cole o system prompt, converse com a Jane.

**Caminho 2 — Dados reais (Render)**  
Insira suas próprias API keys gratuitas. Análise EOD em tempo real. Keys nunca armazenadas.

**Caminho 3 — Deploy próprio (Docker)**
```bash
git clone https://github.com/ussleo/openjane
docker build -t openjane . && docker run -p 8000:8000 openjane
```

### Dados de mercado — completamente gratuitos

| Provedor | O que oferece | Cartão de crédito |
|---|---|---|
| [Massive.com](https://massive.com) | Preços EOD, volume, histórico OHLCV | ❌ Não |
| [EODHD](https://eodhd.com) | MA50/200, HV, curva de juros, 150k+ tickers | ❌ Não |

### Ghost tickers

| Ticker | Empresa | Por que é um ghost ticker |
|---|---|---|
| **CBOE** | Cboe Global Markets | Proxy mais próximo: opções, vol, microestrutura |
| **ICE** | Intercontinental Exchange | Proxy sistêmico e infraestrutural |
| **VIRT** | Virtu Financial | Market maker público, comparável direto |

---

## Créditos / Credits / Créditos

| | |
|---|---|
| Investigación, diseño y desarrollo | **ussleo** + **Claude Code** (Anthropic) |
| Motor de análisis | Claude Sonnet (Anthropic) |
| Servidor | FastAPI + uvicorn · Render.com (free tier) |
| Frontend | GitHub Pages |
| Datos de mercado | [Massive.com](https://massive.com) · [EODHD](https://eodhd.com) |
| Licencia | Apache 2.0 |

---

*OpenJane · Apache 2.0 · [github.com/ussleo/openjane](https://github.com/ussleo/openjane)*
