FROM node:22-alpine AS build

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml tsconfig.json tsconfig.base.json tsconfig.build.json ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY src ./src
RUN pnpm run build

FROM node:22-alpine AS runtime

WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN corepack enable && pnpm install --prod --frozen-lockfile
COPY --from=build /app/dist ./dist

ENV NODE_ENV=production
CMD ["sh", "-c", "pnpm run db:migrate:compiled && pnpm run db:seed:compiled && node dist/main.js"]
