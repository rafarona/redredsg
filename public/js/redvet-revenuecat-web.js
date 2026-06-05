(function () {
  "use strict";

  var AD_FREE_ENTITLEMENT = "ad_free";
  var AI_ENTITLEMENT = "ai_access";
  var purchasesInstance = null;
  var configuredUserId = null;
  var configuredApiKey = null;
  var purchasesJsPromise = null;
  var purchasesJsModule = null;
  var cachedOfferingPrices = null;
  var PURCHASES_JS_URL =
    "https://cdn.jsdelivr.net/npm/@revenuecat/purchases-js@1.41.1/dist/Purchases.umd.js";
  var PURCHASES_JS_SCRIPT_ID = "rr-revenuecat-purchases-js";

  function isPurchasesWebSdk(candidate) {
    return !!(
      candidate &&
      typeof candidate.configure === "function" &&
      typeof candidate.isConfigured === "function"
    );
  }

  function resolvePurchasesClass(root) {
    if (!root) return null;
    if (isPurchasesWebSdk(root)) return root;
    if (root.Purchases && isPurchasesWebSdk(root.Purchases)) {
      return root.Purchases;
    }
    return null;
  }

  function resolveLoadedPurchasesSdk() {
    if (window.__rrPurchasesWebSdk && isPurchasesWebSdk(window.__rrPurchasesWebSdk)) {
      return window.__rrPurchasesWebSdk;
    }
    var resolved = resolvePurchasesClass(window.Purchases);
    if (resolved) {
      window.__rrPurchasesWebSdk = resolved;
      return resolved;
    }
    return null;
  }

  function getConfig() {
    return window.__rrRevenueCatWebConfig || {};
  }

  function getPlans() {
    var cfg = getConfig();
    if (Array.isArray(cfg.plans) && cfg.plans.length) {
      return cfg.plans;
    }
    return [
      { id: "premium", checkoutParam: "premium", packageKey: "$rc_monthly" },
      { id: "ai", checkoutParam: "ai", packageKey: "ai_monthly" },
    ];
  }

  function isConfigured() {
    var cfg = getConfig();
    return !!(cfg.enabled && cfg.apiKey);
  }

  function loadPurchasesJs() {
    var cached = purchasesJsModule || resolveLoadedPurchasesSdk();
    if (cached) {
      purchasesJsModule = cached;
      return Promise.resolve(cached);
    }
    if (purchasesJsPromise) {
      return purchasesJsPromise;
    }

    purchasesJsPromise = new Promise(function (resolve, reject) {
      function finishLoad() {
        var sdk = resolveLoadedPurchasesSdk();
        if (!sdk) {
          purchasesJsPromise = null;
          reject(
            new Error(
              "No se pudo inicializar RevenueCat Web Billing. Recarga la página e inténtalo de nuevo.",
            ),
          );
          return;
        }
        purchasesJsModule = sdk;
        purchasesJsPromise = null;
        resolve(sdk);
      }

      var existingScript = document.getElementById(PURCHASES_JS_SCRIPT_ID);
      if (existingScript) {
        if (existingScript.getAttribute("data-rr-loaded") === "true") {
          finishLoad();
          return;
        }
        existingScript.addEventListener("load", finishLoad, { once: true });
        existingScript.addEventListener(
          "error",
          function () {
            purchasesJsPromise = null;
            reject(new Error("No se pudo cargar @revenuecat/purchases-js"));
          },
          { once: true },
        );
        return;
      }

      // No usar window.Purchases como atajo: purchases_flutter en web también lo define
      // pero no expone configure() del SDK web.
      var script = document.createElement("script");
      script.id = PURCHASES_JS_SCRIPT_ID;
      script.src = PURCHASES_JS_URL;
      script.async = true;
      script.onload = function () {
        script.setAttribute("data-rr-loaded", "true");
        finishLoad();
      };
      script.onerror = function () {
        purchasesJsPromise = null;
        reject(new Error("No se pudo cargar @revenuecat/purchases-js"));
      };
      document.head.appendChild(script);
    });

    return purchasesJsPromise;
  }

  function resolveEntitlements(customerInfo) {
    var active =
      (customerInfo && customerInfo.entitlements && customerInfo.entitlements.active) ||
      {};
    var isAiEnabled = !!active[AI_ENTITLEMENT];
    var isAdFree = !!active[AD_FREE_ENTITLEMENT] || isAiEnabled;
    var managementURL = (
      (customerInfo && (customerInfo.managementURL || customerInfo.managementUrl)) ||
      ""
    ).trim();
    var activeSubscriptions =
      (customerInfo && customerInfo.activeSubscriptions) || [];
    var hasActiveEntitlements = Object.keys(active).length > 0;
    var hasWebSubscription =
      hasActiveEntitlements ||
      (Array.isArray(activeSubscriptions) && activeSubscriptions.length > 0) ||
      !!managementURL;
    return {
      isAdFree: isAdFree,
      isAiEnabled: isAiEnabled,
      hasWebSubscription: hasWebSubscription,
    };
  }

  function formatPackagePrice(pkg) {
    if (!pkg) return null;
    var product = pkg.webBillingProduct || pkg.product || null;
    if (!product) return null;
    if (product.priceString) return product.priceString;
    if (product.currentPrice && product.currentPrice.formattedPrice) {
      return product.currentPrice.formattedPrice;
    }
    if (typeof product.price === "number" && product.currency) {
      try {
        return new Intl.NumberFormat(undefined, {
          style: "currency",
          currency: product.currency,
        }).format(product.price);
      } catch (_) {
        return String(product.price);
      }
    }
    return null;
  }

  async function syncSubscriptionToFirestore(uid, isAdFree, isAiEnabled) {
    if (!window.firebase || !firebase.firestore) return;
    var db = firebase.firestore();
    var entitlementIds = [];
    if (isAdFree) entitlementIds.push(AD_FREE_ENTITLEMENT);
    if (isAiEnabled) entitlementIds.push(AI_ENTITLEMENT);
    var payload = {
      isAdFree: isAdFree,
      isAiEnabled: isAiEnabled,
      entitlementId: AD_FREE_ENTITLEMENT,
      entitlementIds: entitlementIds,
      platform: "web",
      source: "revenuecat",
      subscriptionUpdatedAt: firebase.firestore.FieldValue.serverTimestamp(),
    };
    await db.collection("users").doc(uid).set(payload, { merge: true });
    await db.collection("clinics").doc(uid).set(payload, { merge: true });
  }

  function resolveAppUserId(explicitAppUserId) {
    if (explicitAppUserId) return explicitAppUserId;
    if (typeof window.__rrGetAppUserId === "function") {
      var flutterUid = window.__rrGetAppUserId();
      if (flutterUid) return flutterUid;
    }
    if (window.firebase && firebase.auth) {
      var shellUser = firebase.auth().currentUser;
      if (shellUser && shellUser.uid) return shellUser.uid;
    }
    return null;
  }

  async function ensurePurchases(appUserId) {
    if (!isConfigured()) {
      throw new Error("RevenueCat Web no está configurado todavía.");
    }
    var resolvedUserId = resolveAppUserId(appUserId);
    if (!resolvedUserId) {
      throw new Error("Debes iniciar sesión antes de suscribirte.");
    }
    var Purchases = await loadPurchasesJs();
    var apiKey = getConfig().apiKey;
    if (
      Purchases.isConfigured &&
      Purchases.isConfigured() &&
      configuredApiKey === apiKey
    ) {
      purchasesInstance = Purchases.getSharedInstance();
      if (purchasesInstance.getAppUserId() !== resolvedUserId) {
        await purchasesInstance.changeUser(resolvedUserId);
      }
      configuredUserId = resolvedUserId;
      return purchasesInstance;
    }
    purchasesInstance = Purchases.configure({
      apiKey: apiKey,
      appUserId: resolvedUserId,
    });
    configuredUserId = resolvedUserId;
    configuredApiKey = apiKey;
    return purchasesInstance;
  }

  function findPlanDefinition(planKey) {
    var plans = getPlans();
    for (var i = 0; i < plans.length; i++) {
      var plan = plans[i];
      if (
        plan.id === planKey ||
        plan.checkoutParam === planKey ||
        plan.packageKey === planKey
      ) {
        return plan;
      }
    }
    return null;
  }

  function resolveCurrentOffering(offerings) {
    if (!offerings) return null;
    var cfg = getConfig();
    var targetId = cfg.offeringId || "default";
    var current = offerings.current || null;
    var all = offerings.all || {};
    var targeted = all[targetId] || null;

    if (
      targeted &&
      targeted.availablePackages &&
      targeted.availablePackages.length
    ) {
      return targeted;
    }
    if (
      current &&
      current.availablePackages &&
      current.availablePackages.length
    ) {
      return current;
    }
    if (targeted) return targeted;
    return current;
  }

  function findPackageByPlanKey(offerings, planKey) {
    var plan = findPlanDefinition(planKey);
    var lookup = (plan && plan.packageKey) || planKey;
    var packages = [];
    var offering = resolveCurrentOffering(offerings);
    if (offering && offering.availablePackages) {
      packages = offering.availablePackages;
    }
    for (var i = 0; i < packages.length; i++) {
      var pkg = packages[i];
      if (pkg.identifier === lookup || pkg.lookupKey === lookup) {
        return pkg;
      }
    }
    for (var j = 0; j < packages.length; j++) {
      var candidate = packages[j];
      var productId =
        (candidate.webBillingProduct && candidate.webBillingProduct.identifier) ||
        (candidate.product && candidate.product.identifier) ||
        "";
      if (productId.indexOf("redvet_ai") >= 0 && planKey === "ai") return candidate;
      if (productId.indexOf("premium") >= 0 && planKey === "premium") return candidate;
    }
    return null;
  }

  async function loadOfferingPrices(appUserId) {
    if (!isConfigured()) return null;
    var purchases = await ensurePurchases(appUserId);
    var offerings = await purchases.getOfferings();
    var prices = {};
    getPlans().forEach(function (plan) {
      var pkg = findPackageByPlanKey(offerings, plan.id);
      prices[plan.id] = formatPackagePrice(pkg);
    });
    cachedOfferingPrices = prices;
    return prices;
  }

  async function refreshLocalSubscriptionState(appUserId) {
    var purchases = await ensurePurchases(appUserId);
    var customerInfo = await purchases.getCustomerInfo();
    var state = resolveEntitlements(customerInfo);
    if (typeof window.__rrApplyAdFreeFromApp === "function") {
      window.__rrApplyAdFreeFromApp(state.isAdFree);
    }
    return state;
  }

  function describeWebPackage(pkg) {
    if (!pkg) return null;
    var product = pkg.webBillingProduct || pkg.product || null;
    return {
      packageId: pkg.identifier || pkg.lookupKey || null,
      productId: product && product.identifier,
      productName: product && product.name,
      price: formatPackagePrice(pkg),
      freeTrialPhase: product && product.freeTrialPhase,
      introPricePhase: product && product.introPricePhase,
      discountPhase: product && product.discountPhase,
    };
  }

  window.__rrDebugWebOffering = async function (explicitAppUserId) {
    var appUserId = resolveAppUserId(explicitAppUserId);
    if (!appUserId) {
      throw new Error("Inicia sesión para inspeccionar offerings web.");
    }
    var purchases = await ensurePurchases(appUserId);
    var cfg = getConfig();
    var offerings = await purchases.getOfferings();
    var offering = resolveCurrentOffering(offerings);
    var packages = (offering && offering.availablePackages) || [];
    var shellUser = window.firebase && firebase.auth ? firebase.auth().currentUser : null;
    var report = {
      appUserId: appUserId,
      shellFirebaseUid: shellUser ? shellUser.uid : null,
      flutterAuthUid:
        typeof window.__rrGetAppUserId === "function"
          ? window.__rrGetAppUserId()
          : null,
      environmentResolved: cfg.environmentResolved || null,
      offeringIdRequested: cfg.offeringId || null,
      offeringId: offering && offering.identifier,
      apiKeyPrefix: cfg.apiKey ? String(cfg.apiKey).slice(0, 8) : null,
      offeringIdsAvailable: Object.keys(offerings.all || {}),
      packages: packages.map(describeWebPackage),
      aiPackage: describeWebPackage(findPackageByPlanKey(offerings, "ai")),
      premiumPackage: describeWebPackage(findPackageByPlanKey(offerings, "premium")),
    };
    console.table(report.packages);
    console.log("[RedVet RC Web] offering debug:", report);
    return report;
  };

  window.__rrIsRevenueCatWebEnabled = function () {
    return isConfigured();
  };

  window.__rrListWebSubscriptionPlans = function () {
    return getPlans().map(function (plan) {
      return Object.assign({}, plan, {
        price: (cachedOfferingPrices && cachedOfferingPrices[plan.id]) || null,
      });
    });
  };

  window.__rrRefreshWebSubscription = async function (appUserId) {
    if (!isConfigured()) return null;
    try {
      await loadOfferingPrices(appUserId);
    } catch (e) {
      console.warn("[RedVet RC Web] no se pudieron cargar precios:", e);
    }
    return refreshLocalSubscriptionState(appUserId);
  };

  window.__rrStartWebCheckout = async function (planKey, explicitAppUserId) {
    var appUserId = resolveAppUserId(explicitAppUserId);
    if (!appUserId) {
      throw new Error("Inicia sesión en RedVet para continuar con la suscripción.");
    }
    var purchases = await ensurePurchases(appUserId);
    var offerings = await purchases.getOfferings();
    var selectedPackage = findPackageByPlanKey(offerings, planKey || "premium");
    if (!selectedPackage) {
      throw new Error(
        "No hay planes web disponibles. Falta configurar Web Billing en RevenueCat.",
      );
    }
    console.info("[RedVet RC Web] checkout package:", describeWebPackage(selectedPackage));
    var result = await purchases.purchase({ rcPackage: selectedPackage });
    var state = resolveEntitlements(result.customerInfo);
    if (typeof window.__rrApplyAdFreeFromApp === "function") {
      window.__rrApplyAdFreeFromApp(state.isAdFree);
    }
    return state;
  };

  window.__rrOpenWebCustomerPortal = async function (explicitAppUserId) {
    var cfg = getConfig();
    if (cfg.customerPortalUrl) {
      window.open(cfg.customerPortalUrl, "_blank", "noopener");
      return;
    }
    var appUserId = resolveAppUserId(explicitAppUserId);
    if (!appUserId) {
      throw new Error("Inicia sesión para gestionar tu suscripción.");
    }
    var purchases = await ensurePurchases(appUserId);
    var customerInfo = await purchases.getCustomerInfo();
    var url =
      (customerInfo.managementURL || customerInfo.managementUrl || "").trim();
    if (!url) {
      throw new Error("Portal de gestión no disponible todavía.");
    }
    window.open(url, "_blank", "noopener");
  };

  window.__rrHandlePendingWebCheckout = async function () {
    if (!isConfigured()) return;
    var params = new URLSearchParams(window.location.search);
    var plan = params.get("rrCheckout");
    if (!plan) return;
    var appUserId = resolveAppUserId();
    if (!appUserId) return;
    try {
      await window.__rrStartWebCheckout(plan, appUserId);
    } catch (e) {
      console.warn("[RedVet RC Web] checkout pendiente falló:", e);
    } finally {
      params.delete("rrCheckout");
      var nextQuery = params.toString();
      var nextUrl =
        window.location.pathname +
        (nextQuery ? "?" + nextQuery : "") +
        window.location.hash;
      window.history.replaceState({}, "", nextUrl);
    }
  };
})();
