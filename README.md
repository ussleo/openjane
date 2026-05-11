# OpenJane · by Claude

> Democratizando la lógica de las firmas cuantitativas más grandes del mundo.
> Democratizing the logic of the world's largest quantitative trading firms.
> Democratizando a lógica das maiores firmas quantitativas do mundo.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Built with Claude](https://img.shields.io/badge/Built%20with-Claude-orange.svg)](https://anthropic.com)
[![Data: Massive.com](https://img.shields.io/badge/Data-Massive.com-green.svg)](https://massive.com)
[![Data: EODHD](https://img.shields.io/badge/Data-EODHD-green.svg)](https://eodhd.com)

---

## 🇪🇸 Español

**OpenJane** es un conjunto de skills, comandos y un agente de análisis cuantitativo
construido sobre el ecosistema de Claude (Anthropic), inspirado en los principios operativos
de Jane Street, Citadel Securities y Hudson River Trading.

**Para quién:** cualquier persona con conocimiento básico de inversión que quiera entender
cómo piensan las firmas cuantitativas más exitosas del planeta, sin necesidad de saber programar.

**Filosofía:** Jane Street no gana prediciendo el futuro. Gana optimizando fricción, liquidez
y ejecución a escala masiva con una cultura técnica obsesiva. Este repo traduce esa lógica
a skills accionables y accesibles para cualquier persona.

**¿Por qué OpenJane?** Porque $39 mil millones en ganancias anuales representan una cantidad
obscena de conocimiento concentrado en pocas manos. Creemos que todos merecen acceso
a esa lógica — aunque sea al 1% del pastel.

> ⚠️ **Aviso legal:** Nada en este repositorio constituye asesoramiento financiero, legal
> o de inversión. OpenJane produce análisis educativo para revisión humana. No ejecuta
> transacciones ni recomienda compras o ventas. Tú decides siempre.

---

## 🇺🇸 English

**OpenJane** is a collection of skills, commands, and a quantitative analysis agent
built on the Claude (Anthropic) ecosystem, inspired by the operational principles of
Jane Street, Citadel Securities, and Hudson River Trading.

**Who it's for:** anyone with basic investment knowledge who wants to understand how
the world's most successful quantitative firms think — without needing to write code.

**Philosophy:** Jane Street doesn't win by predicting the future. It wins by optimizing
friction, liquidity, and execution at massive scale with an obsessive technical culture.
This repo translates that logic into actionable, accessible skills for everyone.

**Why OpenJane?** Because $39 billion in annual revenue represents an obscene concentration
of knowledge in very few hands. We believe everyone deserves access to that logic —
even if it's just 1% of the pie.

> ⚠️ **Disclaimer:** Nothing in this repository constitutes financial, legal, or investment
> advice. OpenJane produces educational analysis for human review. It does not execute
> transactions or recommend buys or sells. You always decide.

---

## 🇧🇷 Português (Brasil)

**OpenJane** é um conjunto de skills, comandos e um agente de análise quantitativa
construído sobre o ecossistema Claude (Anthropic), inspirado nos princípios operacionais
da Jane Street, Citadel Securities e Hudson River Trading.

**Para quem:** qualquer pessoa com conhecimento básico de investimento que queira entender
como as firmas quantitativas mais bem-sucedidas do planeta pensam — sem precisar programar.

**Filosofia:** A Jane Street não ganha prevendo o futuro. Ganha otimizando fricção, liquidez
e execução em escala massiva com uma cultura técnica obsessiva. Este repositório traduz
essa lógica em skills acionáveis e acessíveis para qualquer pessoa.

**Por que OpenJane?** Porque US$ 39 bilhões em receita anual representam uma concentração
obscena de conhecimento em poucas mãos. Acreditamos que todos merecem acesso a essa
lógica — mesmo que seja apenas 1% do bolo.

> ⚠️ **Aviso legal:** Nada neste repositório constitui assessoria financeira, jurídica
> ou de investimento. O OpenJane produz análises educacionais para revisão humana.
> Não executa transações nem recomenda compras ou vendas. Você sempre decide.

---

## Estructura / Structure / Estrutura

```
plugins/
  vertical-plugins/
    market-microstructure/   ← spreads, liquidez, flujo de órdenes
    stat-arb/                ← arbitraje estadístico entre pares
    regime-detection/        ← estado actual del mercado
    volatility/              ← superficie de volatilidad implícita
  agent-plugins/
    quant-analyst/           ← agente principal integrado
docs/
  glossary.md                ← glosario completo de 28+ términos
  concepts.md                ← guía de conceptos para principiantes
scripts/
  setup.sh                   ← instalación en un comando
```

## Instalación rápida / Quick install / Instalação rápida

```bash
# Claude Code
claude plugin install quant-analyst@openjane

# O clonar directamente / Clone directly / Ou clonar diretamente
git clone https://github.com/ussleo/openjane
cd openjane
cp .env.example .env
# Añade tus API keys en .env / Add your API keys to .env
```

## Datos de mercado — gratis / Market data — free / Dados de mercado — gratuitos

| Proveedor | Qué aporta | Free tier | MCP nativo |
|---|---|---|---|
| [Massive.com](https://massive.com) | Precios, opciones, tick data USA | ✅ Sin tarjeta | ✅ |
| [EODHD](https://eodhd.com) | Fundamentales, global, forex | ✅ Sin tarjeta | ✅ |

## Comandos / Commands / Comandos

| Comando | Descripción |
|---|---|
| `/spread-analysis [TICKER]` | Análisis de microestructura: spread, liquidez, flujo |
| `/stat-arb [A] [B]` | Par estadístico: correlación, Z-score, half-life |
| `/regime` | Clasificación del régimen actual del mercado |
| `/liquidity-map [TICKER]` | Mapa completo de liquidez de un activo |
| `/vol-surface [TICKER]` | Análisis de volatilidad implícita |

## Glosario / Glossary / Glossário

→ [`docs/glossary.md`](docs/glossary.md) — 28 términos explicados en lenguaje claro,
con definición, cómo se mide, qué implica y ejemplo real.

## Contribuir / Contributing / Contribuir

Todo es markdown y YAML — sin compiladores, sin dependencias complejas.

1. Fork del repo
2. Crea tu skill o mejora en `plugins/vertical-plugins/<vertical>/skills/`
3. Documenta en los tres idiomas si puedes
4. Pull request

## Créditos / Credits / Créditos

- Inspirado en [`anthropics/financial-services`](https://github.com/anthropics/financial-services)
- Construido con [Claude](https://anthropic.com) (Anthropic)
- Datos via [Massive.com](https://massive.com) y [EODHD](https://eodhd.com)
- Investigación de mercado: referenciada en cada skill individual

## Licencia / License / Licença

[Apache License 2.0](LICENSE) — igual que el repo de Anthropic que inspiró este proyecto.

---

*OpenJane · by Claude · 2025 · ussleo*
*"Todos tenemos derecho a una parte del pastel."*
*"Everyone deserves a piece of the pie."*
*"Todos merecem um pedaço do bolo."*
