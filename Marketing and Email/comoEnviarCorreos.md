# Como Enviar Correos con Gmail MCP

Este documento resume la configuracion realizada para poder enviar correos desde la cuenta `info@redredsg.com` usando un servidor MCP de Gmail desde Cursor.

## Objetivo

Poder enviar correos desde `info@redredsg.com` con:

- nombre visible del remitente: `Ing. Rafael Rodriguez Nadal`
- firma visual de Gmail
- contenido en espanol
- envio automatizado desde Cursor

## Solucion elegida

Se utilizo el servidor MCP:

- `@shinzolabs/gmail-mcp`

Motivo:

- permite autenticar contra Gmail
- permite leer, redactar y enviar correos
- es suficiente para el objetivo sin montar todo Google Workspace

## Archivos y rutas usadas

Configuracion MCP de Cursor:

- `~/.cursor/mcp.json`

Directorio local de credenciales Gmail MCP:

- `~/.gmail-mcp/`

Launcher estable del MCP de Gmail:

- `~/.gmail-mcp/start-gmail-mcp.sh`

Archivo OAuth de Google:

- `~/.gmail-mcp/gcp-oauth.keys.json`

Credenciales del usuario autenticado:

- `~/.gmail-mcp/credentials.json`

Firma HTML reutilizable para correos:

- `firmaCorreoRedRedSG.html`

Importante:

- este archivo debe conservar la `firma visual real` que ya fue validada
- incluye nombre, imagen, correo, web y WhatsApp
- no sustituirla por una version simplificada, porque entonces el correo vuelve a llegar "sin pie"

Script local de envio raw con firma:

- `enviarCorreoRawConFirma.py`

## Configuracion realizada

En `~/.cursor/mcp.json` se dejo el servidor `gmail` apuntando a:

- comando: `/Users/rafaelrodrigueznadal/.gmail-mcp/start-gmail-mcp.sh`

Ese launcher hace tres cosas:

- fija `MCP_CONFIG_DIR=/Users/rafaelrodrigueznadal/.gmail-mcp`
- desactiva telemetria
- usa `PORT=0` para que el sistema asigne un puerto libre automaticamente

Ademas limpia procesos viejos de `@shinzolabs/gmail-mcp` antes de arrancar, para evitar el error `EADDRINUSE`.

## Configuracion en Google Cloud

Se creo un proyecto separado para Gmail MCP:

- `RedRedMCPGmail`

Pasos hechos:

1. Crear pantalla de consentimiento OAuth.
2. Crear cliente OAuth de tipo `App de escritorio`.
3. Descargar el JSON del cliente.
4. Guardarlo como `~/.gmail-mcp/gcp-oauth.keys.json`.
5. Habilitar `Gmail API`.
6. Autorizar la cuenta `info@redredsg.com`.

## Configuracion en Gmail

En Gmail web, dentro de `Configuracion` > `Cuentas` > `Enviar mensaje como`, se dejo configurado:

- nombre visible: `Ing. Rafael Rodriguez Nadal`
- firma de correo activa en la cuenta

## Problemas encontrados

### 1. El MCP fallaba al iniciar

Causa:

- el servidor queria escuchar en un puerto fijo
- si quedaba un proceso viejo colgado, Cursor no podia volver a levantarlo

Solucion:

- crear un launcher propio
- limpiar procesos viejos antes de arrancar
- usar `PORT=0` para puerto automatico
- mantener `AUTH_SERVER_PORT=3012` solo para el flujo de autorizacion

### 2. Gmail API no estaba habilitada

Aunque el OAuth estaba correcto, Gmail devolvia error hasta habilitar explicitamente `Gmail API` en el proyecto.

### 3. El remitente salia como `info`

Aunque el alias `sendAs` ya tenia `displayName`, el envio simple del MCP no respetaba correctamente el nombre mostrado.

### 4. La firma no se agregaba

Esto es comportamiento normal de Gmail API:

- la firma existe en Gmail
- pero la API no la inserta automaticamente en los correos enviados
- por eso hubo que extraer y restaurar la `firma visual real` dentro de `firmaCorreoRedRedSG.html`

### 5. Los follow-ups pueden salir "simples"

Si el correo se manda con HTML basico pero sin insertar manualmente la firma, el mensaje llega sin el pie visual aunque el remitente sea correcto.

Por eso el flujo correcto no es solo "mandar HTML", sino:

- construir HTML del cuerpo
- concatenar la firma HTML
- enviar el mensaje como `raw`

## Conclusion tecnica importante

Para correos reales no conviene usar el modo simple de envio del MCP.

El metodo correcto es enviar el correo en formato `raw` RFC 2822, definiendo explicitamente:

- header `From`
- asunto
- cuerpo HTML
- firma HTML
- `Content-Language: es`

## Metodo que funciono bien

La cuarta prueba salio correctamente usando:

- `From: "Ing. Rafael Rodriguez Nadal" <info@redredsg.com>`
- cuerpo HTML
- firma insertada manualmente
- cabecera de idioma en espanol

Con ese metodo:

- el remitente ya aparece como `Ing. Rafael Rodriguez Nadal`
- la firma ya aparece en el correo
- el mensaje ya no se detecta como ingles

## Recomendacion operativa

Para enviar correos a patrocinadores:

1. Tomar el asunto y cuerpo desde `Búsqueda de Contactos Empresas Veterinarias México.md`.
2. Convertir el correo a HTML.
3. Anadir la firma HTML desde `firmaCorreoRedRedSG.html`.
4. Enviar en formato `raw`.

## Metodo reutilizable desde ahora

Quedo preparado un flujo local para no repetir el error del pie/firma:

1. Guardar el cuerpo del correo como archivo HTML.
2. Ejecutar:

```bash
python3 "enviarCorreoRawConFirma.py" \
  --to "destinatario@empresa.com" \
  --subject "Asunto del correo" \
  --html-file "cuerpo.html" \
  --text "Version texto plano opcional"
```

Este script:

- lee las credenciales desde `~/.gmail-mcp/`
- refresca el token automaticamente
- inserta la firma HTML fija
- envia por Gmail API en formato `raw`
- conserva `From: "Ing. Rafael Rodriguez Nadal" <info@redredsg.com>`
- envia con `Content-Language: es`
- usa la `firma visual real restaurada`, no una firma simplificada

## Regla practica

Si el correo es importante o comercial:

- no usar envio simple del MCP
- no asumir que Gmail insertara la firma
- usar siempre `raw` + HTML + firma visual real restaurada

## Flujo recomendado antes de envios masivos

1. Crear borrador o prueba.
2. Verificar remitente, firma e idioma.
3. Enviar uno real.
4. Continuar uno por uno.

## Estado actual

Quedo operativo el envio desde:

- `info@redredsg.com`

Y quedo validado que el metodo fiable es el envio `raw` con firma y remitente explicitos.
