export type LogLevel = "debug" | "info" | "warn" | "error";

export type RuntimeConfig = {
  appName: string;
  environment: string;
  port: number;
  ready: boolean;
  logLevel: LogLevel;
};

const ALLOWED_LOG_LEVELS = new Set<LogLevel>(["debug", "info", "warn", "error"]);

function parsePort(value: string | undefined): number {
  const rawPort = value ?? "3000";
  const port = Number(rawPort);

  if (!Number.isInteger(port) || port <= 0) {
    throw new Error(`PORT must be a positive integer. Received: ${rawPort}`);
  }

  return port;
}

function parseReady(value: string | undefined): boolean {
  const rawReady = value ?? "true";
  if (rawReady === "true") {
    return true;
  }

  if (rawReady === "false") {
    return false;
  }

  throw new Error(`READY must be either true or false. Received: ${rawReady}`);
}

function parseLogLevel(value: string | undefined): LogLevel {
  const rawLogLevel = value ?? "info";
  if (!ALLOWED_LOG_LEVELS.has(rawLogLevel as LogLevel)) {
    throw new Error(`LOG_LEVEL must be one of debug, info, warn, error. Received: ${rawLogLevel}`);
  }

  return rawLogLevel as LogLevel;
}

export function loadRuntimeConfig(env: NodeJS.ProcessEnv = process.env): RuntimeConfig {
  const appName = env.APP_NAME?.trim() || "production-readiness-app";

  return {
    appName,
    environment: env.NODE_ENV?.trim() || "development",
    port: parsePort(env.PORT),
    ready: parseReady(env.READY),
    logLevel: parseLogLevel(env.LOG_LEVEL),
  };
}
