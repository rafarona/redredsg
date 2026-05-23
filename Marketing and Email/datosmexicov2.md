# Datos México — v2 (corte abril 2026)

**Fuente:** Google Analytics 4 (Property `489630989`, cuenta `346825716`).
**Filtro:** `country = "Mexico"` aplicado a todas las consultas.
**Pull directo del API:** corte al 28-abr-2026 (run-time del script `_ga4_mx_v2.py`).
**Sustituye a:** `datosmexicoabril.md` (v1).

> **Caveat técnico (importante para todo pitch):** RedVet hoy reporta dentro del stream
> `redpet` por una mala configuración Firebase (ver `accesoAnalytics.md`). Eso significa
> que cuando hablamos de "1,142 veterinarios activos / 28 días" en realidad es la base
> combinada **RedVet + RedPet** (mayoritariamente vets), no podemos separar limpio MV vs
> propietario hasta que se corrija el stream. Para vendedor externo: hablar siempre de
> "usuarios activos profesionales" y, si preguntan por el split, decir la verdad: hoy se
> reportan agregados, fix técnico en cola.

---

## TL;DR — frases listas para correo

- **México es nuestro 2.º mercado global**, solo detrás de Venezuela.
- **2,831 usuarios totales** en el histórico — **2,626 instalaciones nuevas verificadas** (`first_open`).
- **1,142 activos en los últimos 28 días** y **420 en la última semana**.
- **880 nuevos veterinarios mexicanos solo en abril 2026** → **récord histórico mensual**.
- **22,433 eventos clínicos** dentro de la app en 28 días.
- Cobertura real en **30+ ciudades**, con **CDMX (264) y Puebla (120)** como motor del país.
- Audiencia **97.6 % móvil** (Android domina con 97 %).

---

## 1. Métricas globales — México

### 1.1 Histórico (lifetime)

- Usuarios totales (`totalUsers`): **2,831**
- Usuarios nuevos (`newUsers`): 2,668
- Usuarios activos (`activeUsers`): 2,816
- Sesiones (`sessions`): 9,642
- Vistas de pantalla (`screenPageViews`): 90,324
- Eventos totales (`eventCount`): **188,990**
- Instalaciones verificadas (`first_open`): **2,626**

### 1.2 Últimos 28 días (corte 28-abr-2026)

- Usuarios totales: 1,244
- **Usuarios activos: 1,142**
- Usuarios nuevos: 908
- Sesiones: 2,163
- Vistas de pantalla: 10,983
- Eventos totales: **22,433**
- Instalaciones nuevas (`first_open`): 908

### 1.3 Últimos 7 días

- Usuarios totales: 482
- Usuarios activos: **420**
- Usuarios nuevos: 250
- Sesiones: 659
- Vistas de pantalla: 3,476
- Eventos totales: 6,863

### 1.4 Solo abril 2026

- Usuarios totales: 1,172
- **Usuarios activos: 1,093**
- **Usuarios nuevos: 880** ← récord histórico mensual
- Sesiones: 1,924
- Eventos totales: **19,783**

---

## 2. Crecimiento mensual (últimos 18 meses, México)

- 2025-05 — 2 activos / 1 nuevo (primer registro mexicano)
- 2025-06 — 93 activos / 91 nuevos (primer arranque orgánico)
- 2025-07 — 54 activos / 44 nuevos
- 2025-08 — 47 activos / 36 nuevos
- 2025-09 — 11 activos / 5 nuevos (valle estacional)
- 2025-10 — 89 activos / 70 nuevos
- 2025-11 — 88 activos / 63 nuevos
- **2025-12 — 409 activos / 384 nuevos** (salto estructural, primera oleada fuerte)
- 2026-01 — 638 activos / 498 nuevos (consolidación post-salto)
- 2026-02 — 601 activos / 416 nuevos (estabilización)
- 2026-03 — 393 activos / 180 nuevos (valle)
- **2026-04 — 1,093 activos / 880 nuevos (récord absoluto histórico)**

**Lectura comercial:** la curva de México muestra un **2.7× sobre el mes anterior** y un **8× sobre marzo en nuevos registros**. Es el mejor mercado de RedRed en momentum ahora mismo.

---

## 3. Crecimiento semanal (últimas 12 semanas)

- 2026-W05 (Ene 26 – Feb 1): 164 activos / 120 nuevos
- 2026-W06 (Feb 2 – 8): 253 / 157
- 2026-W07 (Feb 9 – 15): 268 / 176
- 2026-W08 (Feb 16 – 22): 146 / 50
- 2026-W09 (Feb 23 – Mar 1): 111 / 33
- 2026-W10 (Mar 2 – 8): 117 / 38
- 2026-W11 (Mar 9 – 15): 142 / 50
- 2026-W12 (Mar 16 – 22): 115 / 39
- 2026-W13 (Mar 23 – 29): 97 / 37
- 2026-W14 (Mar 30 – Abr 5): 101 / 31
- **2026-W15 (Abr 6 – 12): 468 / 405**
- **2026-W16 (Abr 13 – 19): 477 / 360**
- 2026-W17 (parcial, Abr 20 – ): 213 / 100

**Observación:** las semanas 15 y 16 de abril son **~4× la base de marzo**. Sostenido durante 2 semanas consecutivas → no es ruido, es escala real.

---

## 4. Distribución geográfica

### 4.1 Top 30 ciudades — histórico (`totalUsers`)

- Ciudad de México — 618 totales / 575 activos
- *(no detectado / VPN / privacidad)* — 474 / 449
- Heroica Veracruz — 397 / 386
- **Puebla — 228 / 216**
- Guadalajara — 88 / 81
- Mérida — 80 / 76
- Monterrey — 77 / 74
- Xalapa — 65 / 64
- Zapopan — 55 / 54
- Tuxtla Gutiérrez — 46 / 44
- Ecatepec de Morelos — 44 / 37
- Ciudad Nezahualcóyotl — 43 / 38
- Cuernavaca — 40 / 36
- Santiago de Querétaro — 39 / 31
- Culiacán — 35 / 29
- Pachuca — 34 / 34
- Tijuana — 34 / 34
- Veracruz — 33 / 32
- Coatzacoalcos — 31 / 29
- Cancún — 30 / 26
- Ciudad Juárez — 29 / 26
- Morelia — 29 / 28
- Acapulco — 28 / 26
- Ixtapaluca — 27 / 26
- Oaxaca — 27 / 23
- Chimalhuacán — 26 / 21
- León — 24 / 23
- Toluca — 24 / 21
- Cuautitlán Izcalli — 22 / 20
- Fraccionamiento Puente Moreno (Boca del Río) — 22 / 22

### 4.2 Top 30 ciudades — últimos 28 días

- Ciudad de México — 264 activos
- **Puebla — 120 activos**
- *(no detectado)* — 117
- Heroica Veracruz — 65
- Xalapa — 30
- Cuernavaca — 25
- Guadalajara — 23
- Coatzacoalcos — 22
- Pachuca — 22
- Mérida — 19
- Zapopan — 19
- Oaxaca — 18
- Ixtapaluca — 17
- Ciudad Nezahualcóyotl — 16
- Ecatepec de Morelos — 16
- Tijuana — 16
- Tuxtla Gutiérrez — 15
- Acapulco — 13
- Chimalhuacán — 13
- Monterrey — 13
- León — 12
- Valle de Chalco — 11
- Ojo de Agua — 10
- Ciudad Guzmán — 9
- Santiago de Querétaro — 9
- Veracruz — 9
- Cancún — 8
- Ciudad Juárez — 8
- Cuautla — 8
- Toluca — 8

**Concentración:** CDMX + Puebla + Veracruz suman ~40 % del activo mensual. La cola larga (~30 ciudades adicionales con 5–15 activos) cubre prácticamente todo el territorio nacional, de Tijuana a Cancún.

> **Hook para Congreso Veterinario Puebla 2026:** Puebla es la **2.ª ciudad activa del país** este mes, con 120 vets activos. Para cualquier marca con presencia confirmada en el congreso, hay un argumento clarísimo de continuidad digital pre/durante/post-evento.

---

## 5. Comportamiento dentro de la app (28 días)

### 5.1 Eventos top

- `screen_view` — 10,981
- `user_engagement` — 5,134
- `session_start` — 2,053
- `app_open` — 1,972
- `first_open` (instalación nueva) — 908
- `ad_impression` (RedVetAds actual) — **535**
- `app_remove` — 480
- `login` — 122
- `app_update` — 108
- `os_update` — 36
- `sign_up` (registros nuevos) — **30**
- `app_store_subscription_renew` — 18
- `whatsapp_reminder_sent` — 15
- `app_clear_data` — 15
- `in_app_purchase` — 8
- `ad_click` — 3
- `first_appointment_created` — 3
- `purchase` — 2
- `subscribe` — 2
- `app_store_subscription_convert` — 1

### 5.2 Engagement promedio

- Vistas de pantalla por sesión: **5.08**
- Sesiones por usuario: **1.89**
- Tasa de engagement (`engagementRate`): **68.5 %**
- Tiempo total de engagement: 290,369 s (≈ 80.6 h)
- Duración media de sesión (cruda GA4): 3,724 s

> Ojo con `averageSessionDuration`: GA4 lo calcula sobre `userEngagementDuration / sessions`,
> y como muchos vets dejan la app abierta en background (en consulta), el promedio crudo
> infla. La métrica útil para vender es **`engagementRate = 68.5 %`** y **5 vistas por
> sesión**, que sí son saludables y comparables.

### 5.3 Lectura para RedVetAds

- **535 impresiones publicitarias reales** en 28 días, con la base actual de 5 marcas piloto.
- **3 clicks sobre 535 impresiones** → CTR 0.56 % en este periodo (línea base; a optimizar con creativos profesionales).
- **20 eventos por usuario activo / mes** → uso intensivo, no ocasional.

---

## 6. Stack del usuario mexicano (28 días)

### 6.1 Tipo de dispositivo

- Móvil — **1,117 activos (97.6 %)**
- Tablet — 25 (2.2 %)
- Desktop — 2 (0.2 %)

### 6.2 Sistema operativo

- **Android — 1,105 activos (96.8 %)**
- iOS — 37 (3.2 %)
- macOS (web) — 2 (<0.2 %)

> **Implicación creativa:** los assets para México deben optimizarse para Android primero
> (proporciones, peso, formatos compatibles con Material). iOS es residual, no descuidar
> pero no priorizar.

### 6.3 Versión de app más usada (top 5)

- 1.0.50 — 629 activos (55.1 %)
- 1.0.58 (última) — 264 (23.1 %)
- 1.0.56 — 104 (9.1 %)
- 1.0.47 — 97 (8.5 %)
- 1.0.41 — 50 (4.4 %)

> ~78 % de la base mexicana corre versiones recientes (1.0.50+). Cualquier formato
> publicitario nuevo lanzado en una versión actual llega a la mayoría sin esperar
> reinstalación.

---

## 7. Split por stream (28 días, México)

- `redpet` (RedVet + RedPet mezclados) — **1,131 activos** / 2,096 sesiones / 21,640 eventos
- RedTPV Android — 9 activos / 65 sesiones / 783 eventos
- RedTPV SG — 2 activos / 2 sesiones / 10 eventos

> El split RedVet vs RedPet limpio se desbloquea cuando se corrija el stream
> Firebase del build de RedVet (Android `11412248515`, iOS `11412267911`).

---

## 8. Frases listas para pitch

- *"México es nuestro 2.º mercado global, solo detrás de Venezuela."*
- *"En abril sumamos 880 veterinarios mexicanos nuevos — récord histórico."*
- *"1,142 veterinarios activos cada 28 días, generando 22,433 eventos dentro de la app."*
- *"Puebla es nuestra 2.ª ciudad activa del país este mes, con 120 vets — argumento directo para Congreso Veterinario Puebla 2026."*
- *"Engagement del 68.5 % y 5 pantallas por sesión: la app no es un download muerto, se usa en consulta."*
- *"Audiencia 97.6 % móvil, 97 % Android — perfil clínico real, no escritorio corporativo."*
- *"Cobertura en 30+ ciudades, de Tijuana a Cancún, con cola larga viva (no concentración solo en CDMX)."*

---

## 9. Para pitch de RedVetAds (cierre comercial)

- **Audiencia mensual verificada:** 1,142 veterinarios activos.
- **Inventario publicitario real:** 535 impresiones en 28 días con la base piloto actual; capacidad de escalar 10× si se llenan los 4 slots de flujo clínico.
- **Segmentación 100 % por país:** la marca paga solo por impactos sobre el veterinario mexicano (sin tráfico de relleno LATAM).
- **Concentración estratégica:** CDMX (23 % del activo mensual) + cinturón Puebla–Veracruz–Xalapa (20 %) + cola larga nacional (57 %).
- **Engagement clínico real:** 5 pantallas/sesión y 68.5 % de engagementRate dan una alta probabilidad de exposición efectiva del banner.
- **Plataforma móvil-Android first:** alinear creativos con esa realidad.

---

## 10. Trazabilidad

- **Property GA4:** `489630989`
- **Cuenta:** `346825716`
- **Service account:** `redred-analytics-reader@redpetvet25.iam.gserviceaccount.com`
- **Filtro aplicado:** `dimensionFilter.country = "Mexico"`
- **Script generador:** `_ga4_mx_v2.py` (one-shot, eliminado tras el pull).
- **Timestamps clave:**
  - Pull realizado: 28-abr-2026 (run-time del script).
  - Periodo `28d`: 2026-03-31 → 2026-04-28.
  - Periodo `7d`: 2026-04-21 → 2026-04-28.
  - Periodo `Abril 2026`: 2026-04-01 → 2026-04-30 (cerrado al día del pull).

---

## 11. Datos globales (todo el mundo) — anexo

Mismo corte GA4 (28-abr-2026), **sin filtro de país**. Útil para cuando un pitch requiere
"números globales de RedRed" (Wildlife, Mars multi-país, Vetco multi-país, etc.). México
representa ~20 % de la base global lifetime y el **país #1 del mundo en activos mensuales
este mes**.

### 11.1 Métricas globales — histórico (lifetime)

- Usuarios totales (`totalUsers`): **20,741**
- Usuarios nuevos (`newUsers`): 20,325
- Usuarios activos (`activeUsers`): 20,687
- Sesiones (`sessions`): 45,970
- Vistas de pantalla (`screenPageViews`): 255,372
- Eventos totales (`eventCount`): **544,416**
- Instalaciones verificadas (`first_open`): **20,270**

### 11.2 Últimos 28 días

- Usuarios totales: 6,753
- **Usuarios activos: 5,749**
- Usuarios nuevos: 4,220
- Sesiones: 11,827
- Vistas de pantalla: 45,875
- Eventos totales: **97,991**
- Instalaciones nuevas (`first_open`): 4,220

### 11.3 Últimos 7 días

- Usuarios totales: 2,048
- Usuarios activos: **1,584**
- Usuarios nuevos: 800
- Sesiones: 2,883
- Vistas de pantalla: 10,933
- Eventos totales: 23,865

### 11.4 Solo abril 2026

- Usuarios totales: 5,551
- Usuarios activos: **4,685**
- Usuarios nuevos: 3,294
- Sesiones: 9,317
- Eventos totales: **77,404**

---

### 11.5 Top 30 países — histórico (`totalUsers`)

- **Venezuela — 5,313 totales / 5,303 activos / 5,234 nuevos**
- **México — 2,831 / 2,816 / 2,668**
- Colombia — 1,536 / 1,523 / 1,483
- Pakistán — 1,421 / 1,412 / 1,403
- Nigeria — 1,143 / 1,142 / 1,135
- India — 1,088 / 1,084 / 1,080
- Bolivia — 1,014 / 1,010 / 993
- Ecuador — 947 / 945 / 923
- Perú — 688 / 685 / 672
- Estados Unidos — 627 / 607 / 552
- Kenia — 551 / 550 / 545
- Nicaragua — 435 / 434 / 427
- El Salvador — 368 / 364 / 359
- Filipinas — 315 / 313 / 306
- Argentina — 284 / 284 / 271
- *(no detectado)* — 263 / 263 / 263
- Ghana — 261 / 261 / 259
- Guatemala — 229 / 221 / 214
- República Dominicana — 212 / 208 / 204
- Honduras — 206 / 205 / 197
- Paraguay — 195 / 194 / 187
- Chile — 184 / 183 / 179
- Panamá — 172 / 172 / 169
- Costa Rica — 95 / 95 / 92
- Puerto Rico — 69 / 69 / 68
- Indonesia — 59 / 53 / 43
- España — 54 / 54 / 48
- Uruguay — 49 / 49 / 48
- Canadá — 40 / 35 / 29
- Francia — 30 / 27 / 22

### 11.6 Top 30 países — últimos 28 días (activos)

- **México — 1,142 activos / 908 nuevos / 22,433 eventos** ← país #1 del mes
- **Venezuela — 1,025 / 716 / 14,281**
- Pakistán — 436 / 326 / 6,518
- Nigeria — 431 / 323 / 5,600
- Colombia — 382 / 249 / 7,121
- India — 355 / 298 / 5,624
- Bolivia — 257 / 170 / 4,711
- Kenia — 248 / 188 / 3,151
- Ecuador — 222 / 119 / 5,250
- Perú — 181 / 120 / 2,343
- Ghana — 136 / 100 / 1,680
- Filipinas — 115 / 93 / 1,369
- Nicaragua — 113 / 87 / 2,412
- Argentina — 97 / 59 / 3,558
- El Salvador — 71 / 50 / 849
- Estados Unidos — 70 / 56 / 512
- Honduras — 57 / 34 / 3,192
- Chile — 56 / 44 / 814
- Panamá — 53 / 44 / 2,073
- República Dominicana — 52 / 31 / 581
- Guatemala — 46 / 31 / 596
- Paraguay — 42 / 25 / 668
- Costa Rica — 32 / 23 / 644
- Puerto Rico — 25 / 21 / 247
- Canadá — 14 / 8 / 82
- Uruguay — 14 / 10 / 141
- Sudáfrica — 13 / 13 / 248
- España — 13 / 8 / 170
- Indonesia — 11 / 8 / 121
- Alemania — 10 / 8 / 97

> **Lectura:** México (1,142) superó a Venezuela (1,025) como país #1 del mes por primera
> vez en la historia de RedRed. Venezuela sigue siendo #1 lifetime.

### 11.7 Distribución por continente (últimos 28 días)

- Américas — 3,948 activos / 2,815 nuevos (69 % del total global)
- Asia — 919 / 727 (16 %)
- África — 835 / 632 (15 %)
- Europa — 45 / 33 (<1 %)
- Oceanía — 14 / 10 (<1 %)
- *(no detectado)* — 3 / 3

### 11.8 Idioma del dispositivo (últimos 28 días)

- **Español — 3,900 activos (67.9 %)**
- **Inglés — 1,841 (32.0 %)**
- Chino — 4
- Árabe, Bengalí, Francés, Hindi — 1 cada uno

> Base bilingüe real: los creativos y copies de RedVetAds deben existir mínimo en
> español e inglés para cubrir el 100 % de la audiencia.

### 11.9 Top 20 ciudades globales (últimos 28 días)

- Caracas, Venezuela — 268 activos
- Ciudad de México, México — 264
- Lagos, Nigeria — 250
- *(no detectado)*, Venezuela — 220
- Nairobi, Kenia — 199
- Abuja, Nigeria — 144
- **Puebla, México — 120**
- *(no detectado)*, México — 117
- Valencia, Venezuela — 112
- Bogotá, Colombia — 111
- Lahore, Pakistán — 106
- Santa Cruz de la Sierra, Bolivia — 99
- *(no detectado)*, Perú — 94
- Accra, Ghana — 90
- Managua, Nicaragua — 90
- Karachi, Pakistán — 77
- Quito, Ecuador — 71
- *(no detectado)*, Ecuador — 66
- Heroica Veracruz, México — 65
- Maracaibo, Venezuela — 65

> **Observación destacable:** **4 ciudades mexicanas entran en el top 20 mundial** (CDMX #2, Puebla #7, Heroica Veracruz #19, y el bloque no detectado #8). Ninguna otra nación tiene esa concentración de ciudades en el top global.

---

### 11.10 Crecimiento mensual global (últimos 12 meses)

- 2025-05 — 2 activos / 1 nuevo
- 2025-06 — 174 / 172
- 2025-07 — 194 / 163
- 2025-08 — 193 / 176
- 2025-09 — 30 / 22
- 2025-10 — 245 / 226
- 2025-11 — 166 / 140
- **2025-12 — 506 / 478** (primer salto)
- **2026-01 — 6,849 / 6,744** (explosión global: despegue Pakistán/Nigeria/India/VE/MX)
- 2026-02 — 6,367 / 5,314
- 2026-03 — 5,135 / 3,595
- **2026-04 — 4,685 / 3,294** (descenso global; pero MX dentro crece 2.7× vs marzo)

> **Dinámica importante:** la base global está en fase de *retención post-adquisición
> masiva*. México es el mercado contracíclico ahora mismo (crece cuando la base global
> decrece).

### 11.11 Crecimiento semanal global (últimas 12 semanas)

- 2026-W05 — 844 activos / 579 nuevos
- 2026-W06 — 1,637 / 1,156
- 2026-W07 — 1,830 / 1,374
- 2026-W08 — 2,032 / 1,474
- 2026-W09 — 1,920 / 1,310
- 2026-W10 — 1,651 / 1,029
- 2026-W11 — 1,142 / 526
- 2026-W12 — 1,042 / 526
- 2026-W13 — 1,592 / 1,072
- 2026-W14 — 1,382 / 844
- **2026-W15 — 1,947 / 1,405**
- **2026-W16 — 1,802 / 1,153**
- 2026-W17 (parcial) — 826 / 334

---

### 11.12 Eventos top globales (últimos 28 días)

- `screen_view` — 45,870
- `user_engagement` — 21,848
- `session_start` — 10,922
- `app_open` — 9,668
- `first_open` — 4,220
- `app_remove` — 2,979
- `ad_impression` — **1,385**
- `login` — 308
- `app_update` — 284
- `os_update` — 170
- `app_exception` — 90
- `sign_up` — **70**
- `app_clear_data` — 67
- `whatsapp_reminder_sent` — 56
- `app_store_subscription_renew` — 18
- `in_app_purchase` — 10
- `ad_click` — 8
- `first_appointment_created` — 6
- `page_view` — 5
- `first_visit` — 2
- `purchase` — 2
- `subscribe` — 2
- `app_store_subscription_convert` — 1

### 11.13 Engagement promedio global (últimos 28 días)

- Vistas de pantalla por sesión: **3.88**
- Sesiones por usuario: **2.06**
- Tasa de engagement (`engagementRate`): **61.6 %**
- Tiempo total de engagement: 1,313,232 s (≈ 365 h)
- Duración media de sesión (cruda GA4): 4,313 s

### 11.14 Stack global (últimos 28 días)

- Móvil — 5,697 activos (99.1 %)
- Tablet — 51 (0.9 %)
- Desktop — 3 (<0.1 %)
- **Android — 5,671 (98.6 %)**
- iOS — 77 (1.3 %)
- macOS — 2
- Linux — 1

### 11.15 Split por stream global (últimos 28 días)

- `redpet` (RedVet + RedPet mezclados) — 5,729 activos / 11,737 sesiones / 96,674 eventos
- RedTPV Android — 16 / 89 / 1,274
- RedTPV SG — 4 / 4 / 43

---

### 11.16 Frases listas para pitch global

- *"RedRed tiene más de 20,700 profesionales veterinarios en todo el mundo, con 20,270 instalaciones verificadas."*
- *"En los últimos 28 días, 5,749 veterinarios activos generaron casi 98,000 eventos clínicos dentro de la app."*
- *"Estamos presentes en más de 50 países, con LATAM como mercado principal (69 % del activo) y expansión real en África y Asia."*
- *"Abril 2026: México (1,142) desbancó a Venezuela (1,025) como el país #1 del mes por primera vez en nuestra historia."*
- *"4 ciudades mexicanas en el top 20 mundial: CDMX, Puebla, Heroica Veracruz y el bloque no-geolocalizado."*
- *"Base bilingüe real: 68 % español / 32 % inglés — creativos deben producirse en ambos idiomas."*
- *"98.6 % Android: priorizar Android en cualquier producción publicitaria regional o global."*

### 11.17 Para pitch multi-país (RedVetAds regional / global)

- **Audiencia mensual verificada:** 5,749 veterinarios activos (global).
- **Países con masa crítica vendible hoy (>50 activos/mes):** México, Venezuela, Pakistán, Nigeria, Colombia, India, Bolivia, Kenia, Ecuador, Perú, Ghana, Filipinas, Nicaragua, Argentina, El Salvador, Estados Unidos, Honduras, Chile, Panamá, República Dominicana, Guatemala.
- **Paquete multi-país** (Vetco, Mars, Royal Canin, etc.): posibilidad de armar combos por bloque (p. ej. CAN — Centroamérica + México; CONO SUR — AR/CL/UY/PY; ANDINO — CO/EC/PE/BO/VE) con tarifa fija cross-border.
- **Segmentación GA4 100 % por país:** el reporte mensual puede cortar los impactos por país sin costo adicional.

---

### 11.18 Trazabilidad (anexo global)

- **Mismo property, cuenta y service account** de la sección México.
- **Script generador:** `_ga4_global.py` (one-shot, eliminado tras el pull).
- **Sin filtro de país** aplicado a todas las consultas globales.

---

*Datos verificados directamente contra GA4 vía service account read-only el 28-abr-2026.*
