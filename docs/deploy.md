# Deploy hosting RedRedSG

## Context
When running `firebase deploy --only hosting:redredsg` inside the Cursor tool
environment, the Firebase CLI may end with:

- `Error: EPERM: operation not permitted, open '~/.config/configstore/firebase-tools.json.*'`
- `Error: An unexpected error has occurred.`

Even if the deploy succeeds, this error can appear because the sandbox blocks
writing to the CLI config store in the user's home directory.

## Solution
Run the deploy outside the sandbox so the CLI can write to its config store.
In this environment, that means requesting full permissions for the command.

Example (outside sandbox):

```
firebase deploy --only hosting:redredsg
```

## Notes
- The deploy can still succeed even if the error appears, but it is noisy.
- After running outside the sandbox, the error does not appear.

## Local run (important for Google login)

For this project, run local hosting on `localhost:8080`:

```
firebase serve --only hosting:redredsg --port 8080
```

Open the app from:

- `http://localhost:8080/redtpv-app/#/login`
- `http://localhost:8080/redvet-app/#/login`

### Why this matters

Google OAuth is strict with origin/redirect matching. If you run the app from a
different host/port (for example `127.0.0.1:5003`), Google sign-in can fail
with:

- `Error 400: redirect_uri_mismatch`

To keep login working locally, use the same origin that was configured before:

- `http://localhost:8080`

## Integrate a new RedVet web build

When integrating a new build from `redvetrf/build/web` into
`public/redvet-app`, keep the custom shell and ad integration from this
repository.

### Source and target

- Source build: `/Users/rafaelrodrigueznadal/flutter/redvetrf/build/web`
- Target folder: `public/redvet-app`

### Safe integration steps

1. Sync the generated Flutter artifacts, but do not overwrite `index.html`.

```
rsync -av --exclude "index.html" \
  "/Users/rafaelrodrigueznadal/flutter/redvetrf/build/web/" \
  "/Users/rafaelrodrigueznadal/flutter/redredsg/public/redvet-app/"
```

2. Keep `public/redvet-app/index.html` with the custom page shell, ad slots and
   Firebase ad-free logic. If needed, restore it from the known custom shell and
   then update only the service worker version.

3. Update `serviceWorkerVersion` in `public/redvet-app/index.html` to match the
   new build (from source build `index.html` or `flutter_bootstrap.js`).

### What must be preserved in `public/redvet-app/index.html`

- App host: `#rr-flutter-host`
- Ads container/slots: `#rr-ad-right`, `#rr-ad-slot-main`, `#rr-ad-slot-side`
- Ad loader and policy functions:
  - `loadAdScript`
  - `showAdsColumn`
  - `hideAdsColumn`
  - `resolveIsAdFreeForUser`
  - `applyAdFreePolicy`

If `index.html` is replaced by the vanilla Flutter one, page layout and ad
integration will break.

### Quick validation after integration

1. Run local hosting:

```
firebase serve --only hosting:redredsg --port 8080
```

2. Open and validate:
- `http://localhost:8080/redvet-app/#/login`
- Non-authenticated user: ads column visible on desktop.
- Authenticated ad-free user: ads column hidden.
