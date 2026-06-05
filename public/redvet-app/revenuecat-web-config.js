// Catálogo web alineado con offering "default" de RevenueCat (iOS/Android).
// Plan 1 → package $rc_monthly → entitlement ad_free (premium_monthly_web)
// Plan 2 → package ai_monthly → entitlement ai_access (redvet_ai_web, trial 3 días)
//
// Modos:
// - environment: "auto"     → sandbox en localhost, producción en redredsg.com
// - environment: "sandbox"  → fuerza sandbox (rcb_sb_...)
// - environment: "production" → fuerza producción (rcb_...)
//
// Obtener keys: RevenueCat → redredsg → RedVet Web (sandbox) / RedVet Web Production
window.__rrRevenueCatWebConfig = {
  enabled: true,
  environment: "auto",
  apiKeys: {
    sandbox: "rcb_sb_CatTucyEcLBWwyPPLMliJBAyI",
    // Public API Key de PRODUCCIÓN (rcb_..., sin _sb_). Obligatoria en redredsg.com.
    production: "rcb_djeICDwBVyNgeoQxBKHNuBOcJsYR",
  },
  // Offering por entorno: sandbox usa productos RedVet Web; producción usa web_production.
  offeringIds: {
    sandbox: "default",
    production: "web_production",
  },
  offeringId: "default",
  plans: [
    {
      id: "premium",
      checkoutParam: "premium",
      packageKey: "$rc_monthly",
      entitlement: "ad_free",
      mobileProductIds: {
        ios: "premium_monthly",
        android: "premium_monthly:monthly",
      },
      title: "Plan RedVet Premium sin publicidad",
      badge: null,
      priceFallback: "Mensual",
      cta: "Suscribirme sin anuncios",
      features: [
        "Sin publicidad",
        "Más espacio en pantalla",
      ],
      legal:
        "Suscripción auto renovable mensual. Se renueva automáticamente salvo cancelación.",
    },
    {
      id: "ai",
      checkoutParam: "ai",
      packageKey: "ai_monthly",
      entitlement: "ai_access",
      mobileProductIds: {
        ios: "redvet_ai",
        android: "redvet_ai:monthly",
      },
      title: "Plan RedVet IA sin publicidad",
      badge: "3 días gratis",
      priceFallback: "Mensual",
      cta: "Probar RedVet IA",
      features: [
        "3 días gratis*",
        "Diagnósticos diferenciales IA",
        "Tratamientos con IA",
        "Interpretación de análisis IA",
        "Sin publicidad",
      ],
      legal:
        "Suscripción auto renovable mensual. Incluye acceso a RedVet IA sin publicidad.",
      trialNote: "*Aplican restricciones.",
    },
  ],
  customerPortalUrl: "",
};

(function rrResolveRevenueCatEnvironment() {
  var cfg = window.__rrRevenueCatWebConfig;
  if (!cfg || !cfg.enabled) return;

  var keys = cfg.apiKeys || {};
  var host = (window.location && window.location.hostname) || "";
  var isLocal = host === "localhost" || host === "127.0.0.1";
  var forced = String(cfg.environment || "auto").toLowerCase();
  var mode =
    forced === "sandbox" || forced === "production"
      ? forced
      : isLocal
        ? "sandbox"
        : "production";

  var selectedKey = keys[mode] || cfg.apiKey || "";
  var offeringIds = cfg.offeringIds || {};
  cfg.apiKey = selectedKey;
  cfg.environmentResolved = mode;
  cfg.isSandbox = mode === "sandbox";
  cfg.offeringId =
    offeringIds[mode] || cfg.offeringId || offeringIds.sandbox || "default";

  if (!selectedKey) {
    console.error(
      "[RedVet RC Web] Falta apiKeys." +
        mode +
        ". Configura la Public API Key en revenuecat-web-config.js",
    );
  } else if (mode === "production") {
    console.info("[RedVet RC Web] Modo producción activo en", host || "web");
  } else {
    console.info("[RedVet RC Web] Modo sandbox activo en", host || "web");
  }
})();
