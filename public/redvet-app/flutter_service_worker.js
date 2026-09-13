'use strict';

// Legacy: usuarios que aún tenían registrado el SW antiguo de Flutter.
// Solo se desregistra; NO recargamos pestañas (evita volver a Home en mitad del trabajo).
self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      try {
        await self.registration.unregister();
      } catch (e) {
        console.warn('[RedVet] Failed to unregister legacy service worker:', e);
      }
    })(),
  );
});
