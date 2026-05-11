# OpenJane · by Claude

> **"Jane Street no gana prediciendo el futuro. Gana optimizando fricción, liquidez y ejecución a escala masiva con una cultura técnica obsesiva."**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude%20Code-orange.svg)](https://claude.ai/code)
[![Live on Render](https://img.shields.io/badge/Live-Render.com-green.svg)](https://openjane.onrender.com)
[![GitHub Pages](https://img.shields.io/badge/Landing-GitHub%20Pages-blue.svg)](https://ussleo.github.io/openjane/)
[![Data: Massive.com](https://img.shields.io/badge/Data-Massive.com-green.svg)](https://massive.com)
[![Data: EODHD](https://img.shields.io/badge/Data-EODHD-green.svg)](https://eodhd.com)

---

## 🌎 Léeme en tu idioma / Read in your language / Leia no seu idioma

- [🇪🇸 Español](#-español)
- [🇺🇸 English](#-english)
- [🇧🇷 Português (Brasil)](#-português-brasil)

---

# 🇪🇸 Español

## Lo que se construyó — en menos de 24 horas

**OpenJane pasó de idea a producción en una sola sesión de trabajo con Claude Code.**

Este no es un proyecto de meses ni de un equipo. Es la demostración práctica de lo que un desarrollador con Claude puede construir en horas — con calidad de producción, seguro, desplegado y documentado.

### Lo que existe hoy

| Componente | URL | Estado |
|---|---|---|
| Landing page trilingüe | [ussleo.github.io/openjane](https://ussleo.github.io/openjane/) | ✅ Live |
| Plataforma de análisis en vivo | [openjane.onrender.com/analyze](https://openjane.onrender.com/analyze) | ✅ Live |
| Guía de setup en Claude.ai | [openjane.onrender.com/claude-setup](https://openjane.onrender.com/claude-setup) | ✅ Live |
| Glosario interactivo (35+ términos) | [openjane.onrender.com/glossary](https://openjane.onrender.com/glossary) | ✅ Live |
| API pública con rate limiting | [openjane.onrender.com/api/health](https://openjane.onrender.com/api/health) | ✅ Live |

### El stack completo

```
GitHub (source)
  ├── docs/           → GitHub Pages (landing estática, glosario, guías)
  └── app/            → Render.com (FastAPI + uvicorn, Docker, free tier)
       ├── /api/regime          POST · régimen de mercado global
       ├── /api/microstructure  POST · microestructura de un ticker
       └── /api/statarb         POST · stat-arb entre dos tickers
```

### Las tres rutas para el usuario

**Ruta 1 — Cero fricción (Claude.ai)**
→ [openjane.onrender.com/claude-setup](https://openjane.onrender.com/claude-setup)
Sin API keys. Sin instalar. Sin formularios. El usuario crea un Project en claude.ai, pega el system prompt con un clic, y habla con Jane en lenguaje natural. Jane responde con el formato quant completo y aclara siempre cuándo no tiene datos en vivo.

**Ruta 2 — Datos reales (Render)**
→ [openjane.onrender.com/analyze](https://openjane.onrender.com/analyze)
El usuario ingresa sus propias API keys gratuitas de Massive.com y EODHD. La plataforma corre análisis en tiempo real (EOD): régimen de mercado, microestructura de cualquier ticker, stat-arb de cualquier par. Las keys nunca se almacenan — cada request las usa y las descarta.

**Ruta 3 — Deploy propio (Docker)**
```bash
git clone https://github.com/ussleo/openjane
docker build -t openjane .
docker run -p 8000:8000 openjane
```

---

## De dónde viene esto

**OpenJane nació de una investigación profunda sobre uno de los actores más secretos del mercado financiero global: Jane Street.**

Jane Street Capital generó aproximadamente **$39 mil millones en 2024** — más que Goldman Sachs en ese mismo concepto. No cotiza en bolsa. No hace publicidad. Y sin embargo es posiblemente la firma más influyente en la microestructura de los mercados financieros modernos.

**La conclusión fue clara: la lógica detrás de esos $39 mil millones no es magia. Es matemática, datos y cultura técnica obsesiva. Y puede documentarse y ponerse al alcance de cualquier persona.**

### Ghost tickers — los proxies públicos de Jane Street

| Ticker | Empresa | Por qué es un ghost ticker |
|---|---|---|
| **CBOE** | Cboe Global Markets | Proxy más cercano: opciones, vol, microestructura |
| **ICE** | Intercontinental Exchange | Proxy sistémico e infraestructural |
| **VIRT** | Virtu Financial | Market making público, comparable directo |
| **NDAQ** | Nasdaq | Market structure e infraestructura |
| **MKTX** | MarketAxess | Liquidez electrónica en renta fija institucional |

### Modelos de machine learning del ecosistema

| Modelo | Aplicación |
|---|---|
| OLS regression + Z-score | Stat-arb: calibración de spread y señal de entrada |
| Ornstein-Uhlenbeck | Half-life de reversión a la media |
| Volatilidad histórica (log-returns) | HV 20d anualizada |
| Hidden Markov Models | Detección de régimen de mercado |
| LSTM / Random Forest | Forecasting de volatilidad y microestructura |
| VPIN | Detección de flujo informado |
| Almgren-Chriss | Ejecución óptima de órdenes |

---

## Arquitectura de seguridad

### Modelo de amenazas

| Amenaza | Mitigación implementada |
|---|---|
| **Prompt injection vía ticker** | Regex estricto `^[A-Z0-9.\-]{1,12}$` — rechazo con 422 |
| **Crossover de keys entre requests concurrentes** | Clientes HTTP instanciados por request, sin `os.environ` global |
| **Abuso de API (flooding)** | Rate limiting 10 req/60s por IP real (X-Forwarded-For) |
| **Keys expuestas en logs** | Error messages truncados a 200 chars, keys nunca se loguean |
| **Inyección de paths en URLs externas** | Tickers validados antes de construir cualquier URL |
| **CORS abierto** | Orígenes permitidos explícitos (GitHub Pages + Render) |
| **Payloads masivos** | Validación de longitud en API keys (8-200 chars) |

### Lo que el servidor no hace (nunca)
- No almacena API keys en memoria, disco ni base de datos
- No loguea el contenido de las requests (solo IP y timestamp para rate limiting)
- No tiene base de datos ni persistencia de ningún tipo
- No ejecuta código del usuario

Ver [`SECURITY.md`](SECURITY.md) para el modelo completo.

---

## Estructura del repositorio

```
openjane/
├── app/
│   ├── main.py              ← FastAPI server (thread-safe, validado)
│   └── requirements.txt     ← fastapi, uvicorn, python-dotenv
│
├── scripts/
│   ├── massive_client.py    ← Cliente Massive.com (EOD, volumen, históricos)
│   ├── eodhd_client.py      ← Cliente EODHD (MA, HV, yield curve)
│   ├── jane_demo.py         ← Demo CLI completo (3 bloques de análisis)
│   └── generate_snapshot.py ← Genera docs/data/snapshot.json
│
├── plugins/
│   ├── agent-plugins/
│   │   └── quant-analyst/agents/quant-analyst.md  ← System prompt del agente
│   └── vertical-plugins/
│       ├── market-microstructure/  ← Skills de spread y liquidez
│       ├── stat-arb/               ← Skills de arbitraje estadístico
│       ├── regime-detection/       ← Skills de clasificación de régimen
│       └── volatility/             ← Skills de superficie de volatilidad
│
├── docs/                    ← GitHub Pages (se sirve como landing)
│   ├── index.html           ← Landing trilingüe ES/EN/PT con auto-detect
│   ├── analyze.html         ← Plataforma de análisis en vivo
│   ├── claude-setup.html    ← Guía de setup en Claude.ai
│   ├── glossary.html        ← Glosario interactivo (35+ términos)
│   ├── api-keys.html        ← Guía para obtener API keys gratuitas
│   ├── screenshots/         ← Screenshots reales del demo
│   └── data/snapshot.json   ← Datos pre-generados (EOD)
│
├── Dockerfile               ← Python 3.12-slim, listo para cualquier cloud
├── render.yaml              ← Configuración para Render.com (free tier)
├── .env.example             ← Template de variables de entorno
├── SECURITY.md              ← Modelo de seguridad y reporte de vulnerabilidades
└── README.md                ← Este archivo
```

---

## Datos de mercado — completamente gratuitos

| Proveedor | Qué aporta | Free tier | Tarjeta |
|---|---|---|---|
| [Massive.com](https://massive.com) | Precios EOD, volumen, históricos OHLCV USA | Ilimitado EOD | ❌ No |
| [EODHD](https://eodhd.com) | MA50/MA200, HV, yield curve, 150k+ tickers | 20 calls/día | ❌ No |

→ [Guía paso a paso para obtener ambas keys](https://openjane.onrender.com/api-keys)

---

## API Reference

Base URL: `https://openjane.onrender.com`

### POST /api/regime
Régimen de mercado global (SPY).
```json
{ "massive_key": "...", "eodhd_key": "..." }
```
Respuesta: score 0-4, clasificación, SPY MA50/MA200, HV 20d, yield curve.

### POST /api/microstructure
Microestructura de un ticker.
```json
{ "massive_key": "...", "eodhd_key": "...", "ticker": "ICE" }
```
Respuesta: precio EOD, VWAP, ADV, rango intraday, liquidez, tendencia, HV.

### POST /api/statarb
Arbitraje estadístico entre dos tickers.
```json
{ "massive_key": "...", "eodhd_key": "...", "ticker_a": "ICE", "ticker_b": "CBOE" }
```
Respuesta: correlación, beta, Z-score, half-life, zonas de entrada/stop/salida, señal.

### GET /api/health
```json
{ "status": "ok", "service": "OpenJane" }
```

**Rate limiting:** 10 requests / 60 segundos por IP.
**Validación de tickers:** `^[A-Z0-9.\-]{1,12}$` — cualquier otro formato retorna 422.

---

## Comandos del agente

| Comando | Acción |
|---|---|
| `/regime` | Régimen actual del mercado (score 0-4 + clasificación) |
| `/spread-analysis [TICKER]` | Microestructura completa: spread, liquidez, ADV, flujo |
| `/stat-arb [A] [B]` | Par estadístico: correlación, Z-score, half-life, señal |
| `/vol-surface [TICKER]` | IV vs HV, skew, estructura temporal, prima de vol |
| `/help` | Menú de comandos |

También responde en lenguaje natural sin necesidad de comandos.

---

## Contribuir

Todo es código abierto bajo Apache 2.0.

- **Nueva skill:** `plugins/vertical-plugins/<vertical>/skills/`
- **Corrección o mejora:** abre un issue o PR en GitHub
- **Traducción:** el glosario y las páginas te esperan
- **Reporte de seguridad:** ver [`SECURITY.md`](SECURITY.md)

---

# 🇺🇸 English

## What was built — in under 24 hours

**OpenJane went from idea to production in a single working session with Claude Code.**

This is not a months-long project or a team effort. It is a practical demonstration of what a developer with Claude can build in hours — production quality, secure, deployed, and documented.

### What exists today

| Component | URL | Status |
|---|---|---|
| Trilingual landing page | [ussleo.github.io/openjane](https://ussleo.github.io/openjane/) | ✅ Live |
| Live analysis platform | [openjane.onrender.com/analyze](https://openjane.onrender.com/analyze) | ✅ Live |
| Claude.ai setup guide | [openjane.onrender.com/claude-setup](https://openjane.onrender.com/claude-setup) | ✅ Live |
| Interactive glossary (35+ terms) | [openjane.onrender.com/glossary](https://openjane.onrender.com/glossary) | ✅ Live |
| Public API with rate limiting | [openjane.onrender.com/api/health](https://openjane.onrender.com/api/health) | ✅ Live |

### Three paths for the user

**Path 1 — Zero friction (Claude.ai)**
→ [openjane.onrender.com/claude-setup](https://openjane.onrender.com/claude-setup)
No API keys. No install. No forms. Create a Project on claude.ai, paste the system prompt with one click, and talk to Jane in natural language.

**Path 2 — Real data (Render)**
→ [openjane.onrender.com/analyze](https://openjane.onrender.com/analyze)
Enter your own free API keys from Massive.com and EODHD. The platform runs live EOD analysis. Keys are never stored — used per request and discarded.

**Path 3 — Self-host (Docker)**
```bash
git clone https://github.com/ussleo/openjane
docker build -t openjane .
docker run -p 8000:8000 openjane
```

### Security architecture

| Threat | Mitigation |
|---|---|
| **Prompt injection via ticker** | Strict regex `^[A-Z0-9.\-]{1,12}$` — 422 on mismatch |
| **Key crossover between concurrent requests** | HTTP clients instantiated per request, no global `os.environ` |
| **API flooding** | Rate limit: 10 req/60s per real IP (X-Forwarded-For) |
| **Keys leaked in logs** | Error messages capped at 200 chars, keys never logged |
| **Path injection into external URLs** | Tickers validated before any URL construction |
| **Open CORS** | Explicit allowed origins (GitHub Pages + Render) |

See [`SECURITY.md`](SECURITY.md) for the full model.

### Free market data

- [Massive.com](https://massive.com) — US EOD prices, volume, historical OHLCV. Free. No credit card.
- [EODHD](https://eodhd.com) — MA50/MA200, HV, yield curve, 150k+ tickers. Free. No credit card.

### Ghost tickers — Jane Street's public proxies

| Ticker | Company | Why it's a ghost ticker |
|---|---|---|
| **CBOE** | Cboe Global Markets | Closest proxy: options, vol, microstructure |
| **ICE** | Intercontinental Exchange | Systemic infrastructure proxy |
| **VIRT** | Virtu Financial | Public market maker, direct comparable |

---

# 🇧🇷 Português (Brasil)

## O que foi construído — em menos de 24 horas

**O OpenJane foi de ideia à produção em uma única sessão de trabalho com o Claude Code.**

Este não é um projeto de meses nem de uma equipe. É a demonstração prática do que um desenvolvedor com o Claude pode construir em horas — com qualidade de produção, seguro, implantado e documentado.

### O que existe hoje

| Componente | URL | Status |
|---|---|---|
| Landing page trilíngue | [ussleo.github.io/openjane](https://ussleo.github.io/openjane/) | ✅ Live |
| Plataforma de análise ao vivo | [openjane.onrender.com/analyze](https://openjane.onrender.com/analyze) | ✅ Live |
| Guia de setup no Claude.ai | [openjane.onrender.com/claude-setup](https://openjane.onrender.com/claude-setup) | ✅ Live |
| Glossário interativo (35+ termos) | [openjane.onrender.com/glossary](https://openjane.onrender.com/glossary) | ✅ Live |
| API pública com rate limiting | [openjane.onrender.com/api/health](https://openjane.onrender.com/api/health) | ✅ Live |

### Três caminhos para o usuário

**Caminho 1 — Zero fricção (Claude.ai)**
→ [openjane.onrender.com/claude-setup](https://openjane.onrender.com/claude-setup)
Sem API keys. Sem instalar. Sem formulários. Crie um Project no claude.ai, cole o system prompt com um clique e converse com a Jane em linguagem natural.

**Caminho 2 — Dados reais (Render)**
→ [openjane.onrender.com/analyze](https://openjane.onrender.com/analyze)
Insira suas próprias API keys gratuitas de Massive.com e EODHD. A plataforma executa análises EOD em tempo real. As keys nunca são armazenadas.

**Caminho 3 — Deploy próprio (Docker)**
```bash
git clone https://github.com/ussleo/openjane
docker build -t openjane .
docker run -p 8000:8000 openjane
```

### Ghost tickers — os proxies públicos da Jane Street

| Ticker | Empresa | Por que é um ghost ticker |
|---|---|---|
| **CBOE** | Cboe Global Markets | Proxy mais próximo: opções, vol, microestrutura |
| **ICE** | Intercontinental Exchange | Proxy sistêmico e infraestrutural |
| **VIRT** | Virtu Financial | Market maker público, comparável direto |

### Dados de mercado — completamente gratuitos

- [Massive.com](https://massive.com) — Preços EOD, volume, histórico OHLCV EUA. Gratuito. Sem cartão.
- [EODHD](https://eodhd.com) — MA50/MA200, HV, curva de juros, 150k+ tickers. Gratuito. Sem cartão.

---

## Créditos / Credits / Créditos

| | |
|---|---|
| Investigación y desarrollo | **ussleo** + **Claude Code** (Anthropic) |
| Motor de análisis | Claude Sonnet (Anthropic) |
| Servidor | FastAPI + uvicorn · Render.com (free tier) |
| Landing | GitHub Pages |
| Datos de mercado | [Massive.com](https://massive.com) · [EODHD](https://eodhd.com) |
| Inspiración | [`anthropics/financial-services`](https://github.com/anthropics/financial-services) |
| Investigación académica | FGV · USP · Mackenzie · Trinity College Dublin · Drexel · UDLAP |

## Licencia / License / Licença

[Apache License 2.0](LICENSE)

---

<div align="center">

**OpenJane · by Claude · 2025–2026**

*"Todos tenemos derecho a una parte del pastel."*
*"Everyone deserves a piece of the pie."*
*"Todos merecem um pedaço do bolo."*

**[ussleo.github.io/openjane](https://ussleo.github.io/openjane/) · [openjane.onrender.com](https://openjane.onrender.com)**

</div>

---

> ⚠️ **Aviso legal / Disclaimer / Aviso legal:**
> Nada en este repositorio constituye asesoramiento financiero, legal o de inversión.
> Nothing in this repository constitutes financial, legal, or investment advice.
> Nada neste repositório constitui assessoria financeira, jurídica ou de investimento.
> OpenJane produce análisis educativo. No ejecuta transacciones. Tú decides siempre.
