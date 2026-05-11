# OpenJane · Security Model

## Resumen / Summary

OpenJane es una plataforma educativa de demostración. Este documento describe su modelo de seguridad, las amenazas conocidas, las mitigaciones implementadas y cómo reportar vulnerabilidades.

OpenJane is an educational demo platform. This document describes its security model, known threats, implemented mitigations, and how to report vulnerabilities.

---

## Modelo de datos / Data model

**El servidor no almacena nada. / The server stores nothing.**

| Dato | Dónde vive | Cuándo desaparece |
|---|---|---|
| API keys del usuario | Solo en el body del POST request | Al terminar el request |
| Resultados de análisis | Solo en el navegador del usuario | Al recargar o cerrar |
| Rate limiting (IP + timestamps) | RAM del servidor (dict en memoria) | Al reiniciar el servidor |
| Logs de Render.com | Render infrastructure | Según política de Render |

**No hay base de datos. No hay sesiones. No hay cookies de sesión. No hay almacenamiento persistente de ningún tipo.**

---

## Amenazas y mitigaciones / Threats and mitigations

### 1. Inyección de path vía campo `ticker` (Path Injection)

**Amenaza:** Un usuario malicioso podría enviar `../../etc/passwd` o `ICE?injected=true` como ticker, intentando manipular las URLs que el servidor construye para las APIs externas.

**Mitigación:**
```python
TICKER_RE = re.compile(r'^[A-Z0-9.\-]{1,12}$')
```
Todo ticker se valida con esta regex antes de usarse en cualquier URL. Un ticker inválido retorna HTTP 422 inmediatamente, sin llegar a construir ninguna URL externa.

---

### 2. Crossover de API keys entre requests concurrentes (Race Condition)

**Amenaza:** Una implementación naive que use `os.environ["API_KEY"] = key` seguido de `importlib.reload(module)` en FastAPI (que es concurrente/async) puede cruzar las keys de dos usuarios simultáneos: el Request A escribe la key del usuario A en la variable de entorno global, pero antes de que el módulo recargue, el Request B escribe la key del usuario B. El Request A termina usando la key del usuario B.

**Mitigación:** Los clientes HTTP se instancian **por request**, recibiendo la key como parámetro de función. No se usa `os.environ` como canal de comunicación entre el request y los clientes.

```python
# ❌ Patrón inseguro (eliminado):
os.environ["MASSIVE_API_KEY"] = key
importlib.reload(massive_client)

# ✅ Patrón seguro (implementado):
def _massive_get(key: str, endpoint: str, ...) -> dict:
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {key}"}
    )
```

---

### 3. Prompt Injection

**Amenaza:** Un usuario podría intentar inyectar instrucciones en los campos de texto (tickers, keys) para manipular el comportamiento del servidor.

**Mitigación:** El servidor no usa LLMs ni procesa texto libre. Los únicos campos de entrada son:
- `ticker`: validado con regex estricto, solo alfanumérico
- `massive_key` / `eodhd_key`: validados por longitud (8-200 chars), nunca interpolados en strings ejecutables

No hay superficie de prompt injection porque no hay prompt.

---

### 4. API Flooding / DoS

**Amenaza:** Un atacante podría enviar miles de requests para agotar el free tier de las APIs externas del usuario o sobrecargar el servidor.

**Mitigación:** Rate limiting en memoria por IP real:
```python
RATE_WINDOW = 60   # segundos
RATE_LIMIT  = 10   # requests por ventana por IP
```
La IP real se extrae de `X-Forwarded-For` (correcto para Render.com que está detrás de un proxy) con fallback a `request.client.host`.

---

### 5. API Keys expuestas en logs

**Amenaza:** Si el servidor logueara el body de los requests, las API keys del usuario quedarían en los logs de Render.com.

**Mitigación:**
- El servidor no loguea el body de ningún request
- Los mensajes de error están truncados a 200 caracteres y no incluyen keys
- FastAPI no loguea request bodies por defecto

---

### 6. CORS abierto

**Amenaza:** Una API sin restricciones CORS puede ser llamada desde cualquier origen, incluyendo páginas maliciosas que el usuario visite.

**Mitigación:** CORS configurado con orígenes explícitos:
```python
allow_origins=["https://ussleo.github.io", "https://openjane.onrender.com"]
```

---

### 7. Payloads masivos (DoS por tamaño)

**Amenaza:** Enviar un payload JSON de varios MB para consumir memoria o tiempo de procesamiento.

**Mitigación:** Validación de longitud en todos los campos de string:
```python
if not key or len(key) < 8 or len(key) > 200:
    raise ValueError("API key inválida")
```
FastAPI también tiene límites de tamaño de request por defecto.

---

## Lo que el servidor NO puede proteger

### Revocación de API keys
Si un usuario sospecha que sus API keys de Massive.com o EODHD fueron comprometidas, **OpenJane no puede revocarlas**. El usuario debe hacerlo directamente en:
- Massive.com: dashboard → API Keys → Revoke
- EODHD: dashboard → Settings → API Token → Regenerate

### Seguridad del navegador del usuario
Si el dispositivo del usuario está comprometido (keylogger, extensión maliciosa, red insegura sin HTTPS), las keys pueden ser capturadas antes de llegar al servidor. OpenJane usa HTTPS (enforced por Render.com) pero no puede proteger el endpoint del cliente.

### Análisis de tráfico
Un observador de red con acceso a la conexión HTTPS del usuario puede ver los metadatos (IP destino, tamaño del request) pero no el contenido (keys, tickers) gracias a TLS.

---

## Botón de pánico / Panic button

La página `/analyze` incluye un botón de pánico visible que:
1. Borra todas las API keys del formulario del navegador
2. Elimina todos los resultados visibles
3. Limpia `sessionStorage` y `localStorage`
4. Reabre el onboarding de bienvenida

**El botón de pánico opera exclusivamente en el navegador del usuario. No tiene acceso al servidor ni puede revocar keys externas.**

---

## Reporte de vulnerabilidades / Vulnerability reporting

Si encuentras una vulnerabilidad de seguridad en OpenJane:

1. **No abras un Issue público en GitHub** si la vulnerabilidad podría ser explotada antes de ser corregida
2. Describe la vulnerabilidad, los pasos para reproducirla y el impacto potencial
3. Abre un Issue con el label `security` o contacta directamente via GitHub

Nos comprometemos a:
- Confirmar la recepción en 48 horas
- Investigar y responder en 7 días
- Dar crédito al reportero en el fix (si lo desea)

---

## Alcance de la seguridad / Security scope

OpenJane es una **plataforma educativa y de demostración**. No es un sistema financiero de producción, no maneja dinero real, no ejecuta órdenes de mercado y no almacena datos de usuario.

El nivel de seguridad implementado es apropiado para este alcance: protege a los usuarios de las amenazas más comunes (inyección, crossover de keys, flooding) sin necesitar los controles de un sistema financiero regulado (SOC2, PCI-DSS, etc.).

---

*OpenJane · Apache 2.0 · github.com/ussleo/openjane*
