# Frontend

Minimal Angular baseline for the Proyecto Integrador frontend. It contains only a neutral startup heading and its rendering test; no business functionality is included.

## Requirements

- Docker Engine with Docker Compose

## Container commands

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose -f compose.yaml run --build --rm --no-deps frontend-check
COMPOSE_DISABLE_ENV_FILE=1 docker compose -f compose.yaml up frontend
```

The development service is available only at `127.0.0.1:4200` and starts Angular with `npm start -- --host 0.0.0.0 --port 4200`.

The Docker build uses `node:22.23.5-bookworm-slim` and installs the fixed npm version `11.19.1` before consuming `package-lock.json`. A clean container lock generation and a clean `npm ci` were confirmed with that version. This documents the confirmed environment result only; it does not establish the cause of the earlier npm 10 error.

## Checks

The `frontend-check` Compose service runs linting, TypeScript checks, Angular unit tests, and a production build. Checks run when the container starts, rather than only during image construction. CI sets `CI=true` and `NG_BUILD_MAX_WORKERS=2` to bound worker use.

## Continuous integration

The GitHub Actions workflow runs on pull requests, pushes to `main`, and manual dispatches. It invokes the same Compose check service without host npm installation. Requiring its status check to block merges must be configured separately in repository branch-protection or ruleset settings.
