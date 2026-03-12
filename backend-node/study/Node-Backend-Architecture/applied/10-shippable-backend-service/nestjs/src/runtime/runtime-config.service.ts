import { Inject, Injectable } from "@nestjs/common";

import { RUNTIME_CONFIG } from "./runtime.constants";
import { type RuntimeConfig } from "./runtime-config";

@Injectable()
export class RuntimeConfigService {
  constructor(
    @Inject(RUNTIME_CONFIG)
    private readonly config: RuntimeConfig,
  ) {}

  get snapshot(): RuntimeConfig {
    return this.config;
  }

  get appName(): string {
    return this.config.appName;
  }

  get environment(): string {
    return this.config.environment;
  }

  get port(): number {
    return this.config.port;
  }

  get logLevel(): RuntimeConfig["logLevel"] {
    return this.config.logLevel;
  }

  get jwtSecret(): string {
    return this.config.jwtSecret;
  }

  get databaseUrl(): string {
    return this.config.databaseUrl;
  }

  get redisUrl(): string {
    return this.config.redisUrl;
  }

  get loginThrottleMaxAttempts(): number {
    return this.config.loginThrottleMaxAttempts;
  }

  get loginThrottleWindowSeconds(): number {
    return this.config.loginThrottleWindowSeconds;
  }

  get booksCacheTtlSeconds(): number {
    return this.config.booksCacheTtlSeconds;
  }
}
