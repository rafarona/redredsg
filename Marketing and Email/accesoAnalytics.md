# Acceso programático a Firebase / Google Analytics 4

Guía interna del proyecto **RedRed / redpetvet25** para consultar métricas de
Firebase Analytics (GA4) desde scripts, sin depender de la consola y sin
renovar tokens manuales.

---

## 1. Contexto

Firebase Analytics publica los eventos de **RedVet**, **RedPet** y **RedTPV** en
una propiedad GA4 que comparte cuenta con el proyecto Firebase.

| Recurso | Valor |
|---|---|
| Proyecto Firebase | `redpetvet25` (nº `482372343054`) |
| Propiedad GA4 | `489630989` |
| Cuenta GA4 | `346825716` |
| Web measurement ID | `G-2T9X8NP3JQ` |
| Streams Android | `11229356790`, `11830158303`, `11412248515` |
| Streams iOS | `11229353632`, `11828273229`, `11412267911` |
| Stream Web | `12064669456` |

> ⚠️ **ADVERTENCIA DE CONFIGURACIÓN — no romper headers, leer antes de interpretar datos**
>
> **RedVet no está reportando a su propio stream.** Hoy los eventos de RedVet
> llegan mezclados dentro del stream que GA4 etiqueta como `redpet`. Es decir:
>
> - `streamName = "redpet"` → **RedPet + RedVet combinados** (no solo propietarios).
> - `streamName = "RedTPV SG"` → RedTPV.
> - **No existe actualmente un stream limpio solo de RedVet.**
>
> Implicaciones:
> - Cualquier split "propietarios vs MVs" derivado de GA4 es **no confiable**.
> - Para presentaciones/comerciales hablar de "usuarios activos" y "descargas"
>   a nivel app genérico, no por rol.
> - Reportes por ciudad, país, eventos, sesiones, etc. **siguen siendo
>   correctos** (el usuario existe, solo está mal etiquetado).
>
> Fix pendiente (lado Flutter): corregir la configuración de Firebase en el
> build de RedVet para que sus eventos vayan al stream que le corresponde
> (Android `11412248515`, iOS `11412267911`). Hasta entonces los números
> deben citarse genéricos.

La API usada para consultar es
[Google Analytics Data API v1beta](https://developers.google.com/analytics/devguides/reporting/data/v1).

---

## 2. Credencial de servicio (hecho)

Se creó una service account dedicada (solo lectura) en IAM del proyecto
`redpetvet25`:

- **Email**: `redred-analytics-reader@redpetvet25.iam.gserviceaccount.com`
- **Rol en GA4**: `Viewer` (Lector) sobre la propiedad `489630989`
- **Rol en GCP**: ninguno (GA4 no requiere permisos IAM)

La clave privada vive en la máquina local en:

```
~/.redred-ga4-sa.json        (permisos 600)
```

> ⚠️ Este archivo es equivalente a una contraseña. **No** subirlo a git ni
> compartirlo. Si se compromete, revocar la clave desde
> [IAM → Service Accounts → redred-analytics-reader → Keys](https://console.cloud.google.com/iam-admin/serviceaccounts?project=redpetvet25).

### Cómo regenerar la credencial (si se pierde)

1. https://console.cloud.google.com/iam-admin/serviceaccounts?project=redpetvet25
2. Click en `redred-analytics-reader@redpetvet25.iam.gserviceaccount.com`.
3. Pestaña **Keys** → "Add Key → Create new key → JSON".
4. `mv ~/Downloads/redpetvet25-*.json ~/.redred-ga4-sa.json`
5. `chmod 600 ~/.redred-ga4-sa.json`

Si se creó una SA nueva, además hay que darle acceso en Google Analytics:

1. https://analytics.google.com/ → engranaje ⚙️ (Administrador).
2. Columna **Propiedad** → **Gestión del acceso de la propiedad**.
3. "+" → Agregar usuarios → email de la SA, rol **Lector**, sin notificar.

---

## 3. Cómo autenticarse desde un script (Python, sin librerías externas)

GA4 Data API acepta JWTs firmados por la SA. No hace falta `google-auth`; con
`cryptography` (preinstalada por el sistema) alcanza.

```python
import base64, json, pathlib, time, urllib.parse, urllib.request
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

SA_PATH = pathlib.Path.home() / ".redred-ga4-sa.json"
PROPERTY_ID = "489630989"
SCOPE = "https://www.googleapis.com/auth/analytics.readonly"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def sa_access_token() -> str:
    sa = json.loads(SA_PATH.read_text())
    now = int(time.time())
    header = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claims = b64url(json.dumps({
        "iss": sa["client_email"],
        "scope": SCOPE,
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now,
        "exp": now + 3600,
    }).encode())
    signing_input = f"{header}.{claims}".encode()
    key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    signature = key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    assertion = f"{header}.{claims}.{b64url(signature)}"

    body = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": assertion,
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())["access_token"]


def run_report(body: dict) -> dict:
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {sa_access_token()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())
```

---

## 4. Queries de ejemplo

### 4.1 Usuarios activos por país (últimos 28 días)

```python
run_report({
    "dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "country"}],
    "metrics": [{"name": "activeUsers"}, {"name": "newUsers"}],
    "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
    "limit": 20,
})
```

### 4.2 Filtro por país específico (p. ej. Argentina)

```python
run_report({
    "dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "country"}, {"name": "city"}],
    "metrics": [
        {"name": "activeUsers"},
        {"name": "newUsers"},
        {"name": "sessions"},
        {"name": "screenPageViews"},
        {"name": "eventCount"},
    ],
    "dimensionFilter": {
        "filter": {
            "fieldName": "country",
            "stringFilter": {"value": "Argentina"},
        }
    },
    "orderBys": [{"metric": {"metricName": "activeUsers"}, "desc": True}],
    "limit": 25,
})
```

### 4.3 Descargas / instalaciones (evento `first_open`)

```python
run_report({
    "dateRanges": [{"startDate": "180daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "country"}],
    "metrics": [{"name": "eventCount"}],
    "dimensionFilter": {
        "andGroup": {"expressions": [
            {"filter": {"fieldName": "eventName", "stringFilter": {"value": "first_open"}}},
        ]}
    },
    "orderBys": [{"metric": {"metricName": "eventCount"}, "desc": True}],
})
```

### 4.4 Split por app (RedVet / RedPet / RedTPV)

El GA4 no sabe de las tres marcas por nombre: cada app envía los eventos con
`app_id` (bundle). Para separarlas se usa la dimensión `streamName` o
`appVersion` y se cruza con la tabla de arriba:

```python
run_report({
    "dateRanges": [{"startDate": "28daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "streamName"}, {"name": "country"}],
    "metrics": [{"name": "activeUsers"}, {"name": "newUsers"}],
    "dimensionFilter": {
        "filter": {"fieldName": "country", "stringFilter": {"value": "Argentina"}}
    },
})
```

Para traducir `streamName` → marca consultar la tabla de streams en la
sección 1.

---

## 5. Desde la consola (sin código)

- **GA4**: https://analytics.google.com/ → propiedad `redpetvet25`.
  - Reportes → **Engagement → Eventos** (ver `first_open`, `session_start`,
    etc.).
  - Reportes → **Tecnología** / **Demografía** → País / Ciudad.
  - **Explorar** → reporte libre con cualquier dimensión/métrica.
- **Firebase Console**: https://console.firebase.google.com/project/redpetvet25/analytics
  - Vista resumida y compartida con el equipo.
- **DebugView** (eventos en tiempo real): Firebase → Analytics → DebugView.
- **BigQuery export** (opcional, histórico crudo): Firebase → Integrations →
  BigQuery.

---

## 6. Límites y buenas prácticas

- La Data API aplica **Quotas** por propiedad y por día (tokens/10k per day).
  Cada `runReport` consume `tokensPerHour` dependiendo de la complejidad.
  Para uso de marketing/reportes manuales no hay problema.
- Datos de GA4 tienen un lag de ~24-48h para reportes de audiencia. Eventos
  en tiempo real (DebugView / `Realtime`) sí son inmediatos.
- `first_open` **no es** exactamente "descargas", es "primera apertura". Para
  descargas literales consultar **Google Play Console** / **App Store
  Connect** (no están expuestas vía GA4).
- La SA no puede modificar nada — rol Viewer. Si en algún momento se
  necesita enviar eventos o editar audiencias, crear otra SA con rol superior.

---

## 7. Checklist rápido si algo falla

| Error | Causa probable | Fix |
|---|---|---|
| `403 PERMISSION_DENIED` al llamar Data API | La SA no está añadida como Viewer en la propiedad | Sección 2 → paso final |
| `401 Unauthorized` al intercambiar JWT | Reloj desincronizado o `private_key` corrupta | `date` en la Mac, regenerar JSON |
| `404 Property not found` | Property ID equivocado | Revisar sección 1 |
| Quotas excedidas | Consultas muy pesadas o loop mal hecho | Agregar `limit`, dateRanges más cortos |

---

## 8. Archivos relacionados en el repo

- `~/.redred-ga4-sa.json` · clave privada (no versionada).
- `Marketing and Email/bulkSendCorreos.py` · envío masivo, usa Gmail API.
- `Marketing and Email/enviarCorreoRawConFirma.py` · envío puntual.
- `Marketing and Email/accesoAnalytics.md` · **este archivo**.

---

_Última actualización: 2026-04-21 · mantenedor: Ing. Rafael Rodríguez Nadal_
