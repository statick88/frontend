FROM node:22.23.5-bookworm-slim AS npm

RUN npm install --global npm@11.19.1 && test "$(npm --version)" = "11.19.1"

FROM npm AS deps

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM deps AS check

COPY angular.json tsconfig.json tsconfig.app.json tsconfig.spec.json eslint.config.js ./
COPY src ./src
COPY public ./public
ENV CI=true
ENV NG_BUILD_MAX_WORKERS=2
CMD ["sh", "-c", "npm run lint && npm run typecheck && npm run test:ci && npm run build"]

FROM deps AS development

COPY angular.json tsconfig.json tsconfig.app.json tsconfig.spec.json eslint.config.js ./
COPY src ./src
COPY public ./public
EXPOSE 4200
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--port", "4200", "--poll", "1000"]
