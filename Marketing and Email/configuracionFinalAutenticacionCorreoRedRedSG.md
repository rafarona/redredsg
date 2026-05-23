# Configuracion final de autenticacion de correo de `redredsg.com`

## Estado final verificado

Ahora mismo `redredsg.com` ya quedó correctamente configurado:

1. `SPF`:
   - `v=spf1 include:_spf.firebasemail.com ~all`

2. `DKIM`:
   - publicado en `google._domainkey.redredsg.com`

3. `DMARC`:
   - `v=DMARC1; p=reject; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;`

Resultado:

- ya no hay doble SPF
- Google Workspace firma con DKIM
- DMARC quedó otra vez en modo estricto correcto (`p=reject`)

## Diagnostico inicial

El dominio `redredsg.com` tenía inicialmente estos problemas:

1. Hay `2` registros SPF publicados al mismo tiempo:
   - `v=spf1 include:dc-aa8e722993._spfm.redredsg.com ~all`
   - `v=spf1 include:_spf.firebasemail.com ~all`

2. El include `dc-aa8e722993._spfm.redredsg.com` resuelve a:
   - `v=spf1 include:_spf.google.com ~all`

3. No existe registro DKIM público para Google Workspace en:
   - `google._domainkey.redredsg.com`

4. DMARC está en modo estricto:
   - `v=DMARC1; p=reject; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;`

## Que significa esto

- Tener `2` registros SPF invalida SPF.
- Sin DKIM alineado de Google Workspace, muchos destinatarios corporativos rechazan el mensaje.
- Como DMARC está en `p=reject`, esos fallos no solo bajan reputación: directamente bloquean la entrega.

Eso explica los rebotes tipo:

- `550 5.7.1 Unauthenticated email rejected due to a DMARC failure`
- `500 5.7.5 DMARC Policy of the domain doesn't allow to accept mail for dmarc failures`

## Lo que hubo que cambiar

### 1. En GoDaddy: dejar un solo SPF

Debes eliminar los `2` TXT SPF actuales y dejar solo `1`.

Valor recomendado para tu caso:

```txt
v=spf1 include:_spf.firebasemail.com ~all
```

Este valor sirve si sigues usando:

- Google Workspace / Gmail
- Firebase email / SendGrid

No dejes dos registros `v=spf1`.

## 2. En Google Admin: activar DKIM para `redredsg.com`

Ruta:

`Google Admin` -> `Apps` -> `Google Workspace` -> `Gmail` -> `Authenticate email`

Pasos:

1. Selecciona el dominio `redredsg.com`.
2. Genera una clave nueva.
3. Usa selector `google`.
4. Usa longitud `2048 bits`.
5. Google te dará un TXT para publicar en DNS.

Normalmente será algo con este host:

```txt
google._domainkey
```

Y un valor largo que empieza parecido a:

```txt
v=DKIM1; k=rsa; p=...
```

Ese valor exacto lo genera Google. No lo inventes manualmente.

## 3. En GoDaddy: publicar el TXT DKIM

En la zona DNS de `redredsg.com`, agrega el TXT que te dio Google:

- `Host`: `google._domainkey`
- `Type`: `TXT`
- `Value`: el que te entregue Google Admin
- `TTL`: el normal por defecto de GoDaddy

## 4. En Google Admin: iniciar autenticacion DKIM

Cuando el TXT ya exista en DNS:

1. vuelve a `Authenticate email`
2. pulsa `Start authentication`

## 5. En GoDaddy: bajar temporalmente DMARC

Mientras corriges SPF y DKIM, conviene cambiar temporalmente DMARC de `reject` a `none`.

Reemplaza el TXT actual de `_dmarc` por este:

```txt
v=DMARC1; p=none; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;
```

Con eso:

- dejas de provocar rechazos inmediatos
- sigues recibiendo reportes DMARC

Cuando todo funcione, puedes subirlo otra vez a `quarantine` o `reject`.

## 6. Estado final recomendado

Una vez validado SPF, DKIM y la entrega real de correos, el valor final correcto para `_dmarc` es:

```txt
v=DMARC1; p=reject; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;
```

## Orden recomendado

1. Cambiar SPF y dejar uno solo.
2. Cambiar DMARC temporalmente a `p=none`.
3. Generar DKIM en Google Admin.
4. Publicar el TXT DKIM en GoDaddy.
5. Activar DKIM en Google Admin.
6. Esperar propagacion.
7. Hacer prueba real de envio.
8. Subir DMARC a `p=quarantine`.
9. Confirmar que no hay comportamientos raros.
10. Subir DMARC a `p=reject`.

## Como verificar que ya quedo bien

Para verificar que quedó bien, hay que revisar estos `3` puntos:

1. `SPF`
   - debe existir un solo `v=spf1`

2. `DKIM`
   - debe resolver `google._domainkey.redredsg.com`

3. `DMARC`
   - debe existir `_dmarc.redredsg.com`

Y después hacemos una prueba de envio a:

- tu Gmail personal
- un dominio corporativo estricto

## Cierre

Este proceso ya quedó completado y verificado:

- `SPF` correcto
- `DKIM` correcto
- `DMARC` final en `p=reject`

Adicionalmente, se confirmó por prueba real que los fallos masivos anteriores eran de autenticación y que, una vez corregidos SPF/DKIM/DMARC, el dominio volvió a enviar correctamente.

## Nota importante

Aunque arreglemos SPF/DKIM/DMARC, todavía conviene corregir en el generador de correos el encabezado `Subject` para que los acentos no salgan mal codificados en algunos destinatarios.

Eso es secundario frente al problema de autenticacion, pero después de arreglar DNS conviene hacerlo.
