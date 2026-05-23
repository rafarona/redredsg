# Seguimiento de rebotes abril 2026

## Resumen ejecutivo

Hay dos tipos de incidencias:

1. `Rebote por autenticación DMARC`
Estos casos no implican necesariamente que el correo esté mal. El servidor del destinatario rechazó el mensaje por autenticación del remitente.

2. `Correo inexistente o no operativo`
Estos casos sí requieren sustituir el destinatario o cambiar de canal.

## Reintentar cuando se corrija DMARC

- `Zoetis`
  - Correos: `zoetismexico@zoetis.com`, `servicioalclientePAH@zoetis.com`
  - Estado: rebotó por `550 5.7.1 Unauthenticated email rejected due to a DMARC failure`
  - Acción: reintentar después de corregir autenticación del dominio

- `IDEXX`
  - Correo: `comercial-latam@idexx.com`
  - Estado: rebotó por `550 5.7.1 Unauthenticated email rejected due to a DMARC failure`
  - Acción: reintentar después de corregir autenticación del dominio

- `Endoshop`
  - Correo previo: `inigo@endoshop.mx`
  - Estado: bloqueado por `500 5.7.5 DMARC Policy of the domain doesn't allow to accept mail for dmarc failures`
  - Acción: reintentar solo si se confirma el correo o usar antes teléfono/formulario

## Sustituir y reenviar

- `Diamond Pet Foods`
  - Correo que falló: `urvet@diamondpet.com.mx`
  - Motivo: `550 No Such User Here`
  - Usar ahora: `contacto@diamondpet.com.mx`
  - Alternativo: `oscarv@diamondpet.com.mx`

- `Chinoin`
  - Correo que falló: `gervet@chinoin.com.mx`
  - Motivo: `550 5.1.1 User unknown`
  - Usar ahora: `ventas@chinoin.com`
  - Alternativo: `rhernandez@chinoin.com.mx`

- `AMMVEPE`
  - Correo que falló: `informes@ammvepe.com.mx`
  - Motivo: `550 mailbox unavailable or not local`
  - Usar ahora: `membresias@ammvepe.com.mx`
  - Alternativo: `informes@ammvepe.com.mx`

## Usar formulario o llamada

- `Elanco`
  - Correo que falló: `contacto@elanco.com`
  - Motivo: `550 5.4.1 Recipient address rejected: Access denied`
  - Canal recomendado: formulario oficial y teléfono `52 3338195534` o `800 000 7387`

- `Purina`
  - Correo que falló: `diana.guerra@purina.nestle.com`
  - Motivo: `550 5.4.1 Recipient address rejected: Access denied`
  - Canal recomendado: formulario oficial Purina México y teléfono `800-614-53-15`
  - Nota: no encontré evidencia pública suficiente para confirmar un correo directo vigente para Diana Guerra

## Entregados o con respuesta

- `Royal Canin`
  - Estado: autorespuesta recibida
  - Interpretación: el correo sí entró

## Prioridad recomendada

1. Corregir autenticación `SPF/DKIM/DMARC` de `info@redredsg.com`
2. Reenviar `Zoetis` e `IDEXX`
3. Reenviar `Diamond`, `Chinoin` y `AMMVEPE` con las direcciones sustituidas
4. Contactar `Elanco`, `Purina` y `Endoshop` por formulario o teléfono

## Follow-ups programados automáticamente

- `Laboratorios Referencia (RD) — Dianny De La Cruz`
  - Correo: `diannyc@labreferencia.com`
  - Motivo: respondió con autorespuesta de vacaciones hasta el 30 de abril
  - Acción: reply dentro del hilo original (`threadId 19dabbde2e6e5cd2`) con
    recordatorio breve y oferta de llamada de 15 min
  - Disparo programado: **lunes 4 de mayo 2026, 10:00 AM CDMX** vía `launchd`
  - Script: `Marketing and Email/_scheduled/sendFollowUpDianny.py`
  - Agent: `~/Library/LaunchAgents/com.redredsg.followup-dianny.plist`
    (Label: `com.redredsg.followup-dianny`)
  - Requisito: el Mac debe estar encendido y con sesión iniciada a esa hora.
    Si estuviera apagado, `launchd` dispara en el próximo arranque.
  - Idempotencia: la guarda de fecha dentro del script y el marker
    `dianny.sent` impiden reenvíos; tras enviar, el agent se auto-descarga.
  - Log: `Marketing and Email/_scheduled/dianny.log`
  - Para cancelarlo manualmente antes del disparo:
    `launchctl bootout gui/$(id -u)/com.redredsg.followup-dianny`
    y borrar el plist.

