# Frontend

This is the minimal Angular baseline for Proyecto Integrador: it renders a neutral startup heading and has no inventory, order, login, API, or other business functionality yet. Docker Compose supplies both local development and the same containerized checks used by CI.

## Quick start from a fork

You need Git, Docker Engine, and Docker Compose v2. Node, npm, and Python are not host prerequisites for normal development.

1. Fork this repository, then clone **your fork** and add the shared repository as `upstream`:

   ```bash
   git clone https://github.com/<your-account>/frontend.git
   cd frontend
   git remote add upstream https://github.com/statick88/frontend.git
   git fetch upstream
   ```

2. Create a worktree and branch, then enter it:

   ```bash
   git worktree add ../frontend-my-change -b my-change upstream/main
   cd ../frontend-my-change
   ```

3. Disable implicit `.env` loading and start development. This literal command is enough after cloning:

   ```bash
   export COMPOSE_DISABLE_ENV_FILE=1
   docker compose up -d --build
   ```

4. Confirm readiness and open http://127.0.0.1:4200/:

   ```bash
   docker compose ps frontend
   docker compose logs --no-color --tail 80 frontend
   ```

The development container runs `ng serve` with polling. Only `src/` and `public/` are read-only bind mounts, so saved source changes reload without rebuilding the image. Rebuild after changing dependencies or container/configuration files:

```bash
docker compose up -d --build
```

## Worktrees and ports

Compose uses the directory basename as its default project name, so differently named worktrees are isolated. You can also set an explicit project name with `docker compose -p frontend-my-change ...`. To run worktrees at the same time, choose a free loopback port:

```bash
FRONTEND_PORT=14200 docker compose -p frontend-my-change up -d --build
```

The container port remains `4200`; this example is available at http://127.0.0.1:14200/. Stop only the project you started:

```bash
docker compose -p frontend-my-change down --remove-orphans
```

## Checks

Run the complete, immutable check container before opening a PR:

```bash
COMPOSE_DISABLE_ENV_FILE=1 docker compose -f compose.yaml run --build --rm --no-deps frontend-check
```

`frontend-check` runs linting, TypeScript checks, Angular unit tests, and a production build. It has no source mounts. The image uses `node:22.23.5-bookworm-slim`, npm `11.19.1`, and the committed lockfile.

## Pull requests and CI

Push your branch to your fork, open a PR against upstream `main`, and link its issue in [Proyecto Integrador project 9](https://github.com/users/statick88/projects/9). Fork contributors need permission to open PRs; private-fork access is governed by the upstream repository's settings.

The workflow is defined for pull requests, pushes to `main`, and manual dispatch. It validates Compose, runs the complete check container, boots the frontend with a bounded wait, checks the HTTP Angular app-shell marker, captures bounded logs on runtime failure, and always stops its own Compose project. CI is not active remotely until this workflow is published. Required merge checks and branch rules remain separate repository settings. As the sole maintainer, you do not need to obtain independent review to use this local workflow.
