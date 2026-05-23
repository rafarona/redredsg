## Guía rápida: conectar y actualizar el sitio de RedRed SG

### Contexto
- **Hosting**: Firebase Hosting
- **Proyecto**: `redpetvet25`
- **Target de Hosting**: `redredsg`
- **Directorio público**: `public/`
- **Sitio en producción**: [redredsg.com](https://redredsg.com/)

### Requisitos
- Tener instalada la Firebase CLI:
```bash
firebase --version
```
- Acceso al proyecto `redpetvet25` en Firebase.

### Estructura relevante del repo
- `firebase.json` → configuración de Hosting (usa `public/`).
- `.firebaserc` → targets ya configurados: `hosting:redredsg` en el proyecto `redpetvet25`.
- `public/index.html` → contenido principal de la web.
- `public/images/` → imágenes públicas (icons, logos, etc.).
- `public/redvet-app/` → app Flutter Web de RedVet servida dentro del mismo Hosting.

### Pasos para desplegar cambios
1) Entrar al proyecto
```bash
cd /Users/rafaelrodrigueznadal/flutter/redredsg
```

2) Autenticarse (si no lo estás)
```bash
firebase login --no-localhost
```

3) Seleccionar el proyecto correcto
```bash
firebase use redpetvet25
```

4) Desplegar solo Hosting al sitio `redredsg`
```bash
firebase deploy --only hosting:redredsg --non-interactive
```

5) Verificar en producción
- Abre [redredsg.com](https://redredsg.com/) (o `https://redredsg.web.app`) y fuerza recarga:
  - macOS: `Cmd + Shift + R`
  - Windows/Linux: `Ctrl + F5`

### Cómo editar contenido
- HTML/CSS: editar `public/index.html`.
- Imágenes: colocar/actualizar archivos en `public/images/` y referenciarlos desde el HTML.

### Cache busting (muy recomendado para imágenes)
Firebase Hosting puede servir recursos desde caché del navegador/CDN. Para ver cambios inmediatamente:
- Renombra el archivo y actualiza su referencia en el HTML. Ejemplo:
  - De: `images/redtpv.png`
  - A: `images/redtpv-v2.png` (y actualizar el `src` en `index.html`).
- Alternativa: añadir query string de versión en el `src`, p. ej. `?v=20251013`.

### Previsualización local (opcional)
Para revisar todo el sitio (incluyendo `redvet-app` y `redtpv-app`) usa Firebase Hosting local:
```bash
firebase serve --only hosting:redredsg --port 8080
```
Luego visita `http://localhost:8080`.

### Integrar una nueva versión de RedVet en la web
**Objetivo**: actualizar `public/redvet-app` con un build nuevo de Flutter sin romper la capa web personalizada (publicidad lateral, layout y lógica `ad-free`).

**Origen típico del build**:
- `/Users/rafaelrodrigueznadal/flutter/redvetrf/build/web`

**Importante**: el `index.html` de `public/redvet-app/` es **editable a mano** y **no debe sobrescribirse** con el del build de Flutter. Contiene el layout, la columna de publicidad y la lógica de suscripción en JS.

#### Procedimiento recomendado
1) Compilar RedVet (si aún no tienes build reciente):
```bash
cd /Users/rafaelrodrigueznadal/flutter/redvetrf
flutter build web --release
```

2) Entrar al proyecto del sitio:
```bash
cd /Users/rafaelrodrigueznadal/flutter/redredsg
```

3) Sincronizar el build nuevo, **sin sobrescribir `index.html`**:
```bash
rsync -av --exclude "index.html" \
  "/Users/rafaelrodrigueznadal/flutter/redvetrf/build/web/" \
  "/Users/rafaelrodrigueznadal/flutter/redredsg/public/redvet-app/"
```

4) Actualizar `serviceWorkerVersion` en `public/redvet-app/index.html` con el valor del build nuevo.
- Puedes leerlo desde:
  - `redvetrf/build/web/index.html` (línea `var serviceWorkerVersion = '"...'"`)
  - o `redvetrf/build/web/flutter_bootstrap.js` (`serviceWorkerVersion: "..."`)

5) Verificar que `public/redvet-app/index.html` mantiene la personalización:
- `base href="/redvet-app/"`
- Layout: `#rr-app-container`, `#rr-flutter-host`, `#rr-ad-right`
- Banner de publicidad lateral: `.rr-ad-banner` (video RedVet IA, **no** scripts externos tipo HighPerformanceFormat)
- Umbral de ancho: `RR_ADS_MIN_WIDTH = 700` (por debajo de 700px la columna se oculta con CSS `display: none !important`)
- Funciones JS de ads/ad-free: `showAdsColumn`, `hideAdsColumn`, `resolveIsAdFreeForUser`, `applyAdFreePolicy`, `window.__rrApplyAdFreeFromApp`
- Puente desde Flutter: la build debe incluir `__rrApplyAdFreeFromApp` en `main.dart.js` (vía `subscription_web_shell_bridge_web.dart`)

6) Probar en local:
```bash
firebase serve --only hosting:redredsg --port 8080
```
- Abrir: `http://localhost:8080/redvet-app/#/login`
- Probar con ventana **> 700px** de ancho
- Comportamiento esperado:
  - **Sin sesión** → publicidad lateral visible
  - **Usuario no suscrito** → publicidad lateral visible
  - **Usuario suscrito** (`isAdFree: true`) → publicidad lateral oculta

7) Si todo está correcto, desplegar:
```bash
firebase deploy --only hosting:redredsg
```

### Publicidad lateral en `redvet-app` (RedVet)

RedVet web usa **dos capas** que deben estar alineadas:

1. **Shell HTML** (`public/redvet-app/index.html`): pinta la columna `#rr-ad-right` y decide mostrar/ocultar según suscripción.
2. **App Flutter** (`SubscriptionService` en `redvetrf`): resuelve el estado de suscripción desde Firestore y, en web, llama a `window.__rrApplyAdFreeFromApp(isAdFree)` para sincronizar el shell.

#### Comportamiento esperado

| Usuario | Publicidad lateral |
|---|---|
| Sin login | Visible |
| No suscrito | Visible |
| Suscrito | Oculta |

#### Campo que define “suscriptor” (sin publicidad)

En Flutter el getter es:

```dart
bool get isAdFree => _manualOverrideAdFree || _isAdFree;
```

En web, `_isAdFree` se resuelve desde Firestore con esta prioridad:

| Prioridad | Fuente |
|---|---|
| 1 | `users/{uid}.isAdFreeManualOverride === true` → siempre sin ads (modo prueba) |
| 2 | `clinics/{clinicId}.isAdFree` (si el campo existe como `boolean`) |
| 3 | Si no hay campo en clínica → `users/{uid}.isAdFree` |
| 4 | Si tampoco existe en user → `false` (mostrar ads) |

**Candidatos de clínica** (igual que Flutter): `[uid, ...associatedClinicIds]`.

**No usar** `users/{uid}.clinicId` como candidato extra en el shell: Flutter no lo incluye y puede ocultar la publicidad por error si apunta a otra clínica con `isAdFree: true`.

`isAiEnabled` es un campo aparte en Firestore; en web **no** entra en el getter `isAdFree` para la columna lateral.

#### Puente Flutter → shell

En `redvetrf/lib/services/subscription_service.dart`:
- `notifyListeners()` en web llama a `syncWebShellAdVisibility(isAdFree)`.
- Implementación web: `subscription_web_shell_bridge_web.dart` → `window.__rrApplyAdFreeFromApp(isAdFree)`.

Si integras un build **sin** ese puente (build antigua), el shell decide solo con su lectura de Firestore y puede desincronizarse respecto a la app.

#### Diagnóstico en el navegador

Con sesión iniciada, abrir consola (F12) en `http://localhost:8080/redvet-app/` y ejecutar:

```javascript
await __rrDebugAdPolicy()
```

Revisar:
- `shellResolvedIsAdFree` → si es `true` pero el usuario no es suscriptor, revisar Firestore (`users/{uid}` y `clinics/{uid}`)
- `users.isAdFreeManualOverride` → si es `true`, es modo prueba y oculta ads
- `windowInnerWidth` → debe ser **> 700** para ver la columna

#### Problemas frecuentes

- **No aparece la publicidad**: ventana ≤700px; Firestore con `isAdFree: true` obsoleto; `isAdFreeManualOverride: true`; shell leyendo `clinicId` distinto de Flutter (corregido en el shell actual).
- **Aparece 1 segundo y desaparece**: `onAuthStateChanged` en web puede dispararse varias veces al cargar; el estado final debe basarse en Firestore + puente Flutter.
- **Suscrito y sigue viendo ads**: build sin puente JS; caché local desactualizada; Firestore sin `isAdFree: true` en `users` o `clinics/{uid}`.

### Solución de problemas
- Error: `Deploy target redredsg not configured for project redredsg`.
  - Asegúrate de usar el proyecto correcto: `firebase use redpetvet25`.
  - Si hiciera falta re-vincular el target (normalmente ya está listo en `.firebaserc`):
    ```bash
    firebase target:apply hosting redredsg redredsg
    ```

### Notas
- Los cambios viven en `public/`. La landing es estática, pero `redvet-app`/`redtpv-app` son builds de Flutter Web.
- Dominio principal: [redredsg.com](https://redredsg.com/). La sección de apps está en `#aplicaciones`.


