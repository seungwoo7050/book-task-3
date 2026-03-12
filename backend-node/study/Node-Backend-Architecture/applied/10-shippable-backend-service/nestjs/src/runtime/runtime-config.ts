export type LogLevel = "debug" | "info" | "warn" | "error";

export type RuntimeConfig = {
  appName: string;
  environment: string;
  port: number;
  logLevel: LogLevel;
  jwtSecret: string;
  databaseUrl: string;
  redisUrl: string;
  loginThrottleMaxAttempts: number;
  loginThrottleWindowSeconds: number;
  booksCacheTtlSeconds: number;
};

const ALLOWED_LOG_LEVELS = new Set<LogLevel>(["debug", "info", "warn", "error"]);

function parsePositiveInteger(name: string, value: string | undefined, fallback: number): number {
  const rawValue = value ?? String(fallback);
  const parsed = Number(rawValue);

  if (!Number.isInteger(parsed) || parsed <= 0) {
    throw new Error(`${name} must be a positive integer. Received: ${rawValue}`);
  }

  return parsed;
}

function parseLogLevel(value: string | undefined): LogLevel {
  const rawLogLevel = value ?? "info";
  if (!ALLOWED_LOG_LEVELS.has(rawLogLevel as LogLevel)) {
    throw new Error(`LOG_LEVEL must be one of debug, info, warn, error. Received: ${rawLogLevel}`);
  }

  return rawLogLevel as LogLevel;
}

export function loadRuntimeConfig(env: NodeJS.ProcessEnv = process.env): RuntimeConfig {
  const appName = env.APP_NAME?.trim() || "shippable-backend-service";
  const jwtSecret = env.JWT_SECRET?.trim();
  const databaseUrl = env.DATABASE_URL?.trim();
  const redisUrl = env.REDIS_URL?.trim();

  if (!jwtSecret) {
    throw new Error("JWT_SECRET is required");
  }

  if (!databaseUrl) {
    throw new Error("DATABASE_URL is required");
  }

  if (!redisUrl) {
    throw new Error("REDIS_URL is required");
  }

  return {
    appName,
    environment: env.NODE_ENV?.trim() || "development",
    port: parsePositiveInteger("PORT", env.PORT, 3000),
    logLevel: parseLogLevel(env.LOG_LEVEL),
    jwtSecret,
    databaseUrl,
    redisUrl,
    loginThrottleMaxAttempts: parsePositiveInteger(
      "LOGIN_THROTTLE_MAX_ATTEMPTS",
      env.LOGIN_THROTTLE_MAX_ATTEMPTS,
      5,
    ),
    loginThrottleWindowSeconds: parsePositiveInteger(
      "LOGIN_THROTTLE_WINDOW_SECONDS",
      env.LOGIN_THROTTLE_WINDOW_SECONDS,
      60,
    ),
    booksCacheTtlSeconds: parsePositiveInteger(
      "BOOKS_CACHE_TTL_SECONDS",
      env.BOOKS_CACHE_TTL_SECONDS,
      30,
    ),
  };
}
