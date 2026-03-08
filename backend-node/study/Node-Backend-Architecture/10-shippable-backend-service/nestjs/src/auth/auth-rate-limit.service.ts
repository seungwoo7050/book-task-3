import { HttpException, HttpStatus, Inject, Injectable } from "@nestjs/common";

import { RedisService } from "../runtime/redis.service";
import { RuntimeConfigService } from "../runtime/runtime-config.service";

@Injectable()
export class AuthRateLimitService {
  constructor(
    @Inject(RedisService)
    private readonly redisService: RedisService,
    @Inject(RuntimeConfigService)
    private readonly runtimeConfig: RuntimeConfigService,
  ) {}

  async ensureLoginAllowed(clientId: string): Promise<void> {
    const attempts = await this.redisService.getJson<number>(this.getKey(clientId));

    if (attempts !== null && attempts >= this.runtimeConfig.loginThrottleMaxAttempts) {
      throw new HttpException("Too many login attempts", HttpStatus.TOO_MANY_REQUESTS);
    }
  }

  async recordFailedAttempt(clientId: string): Promise<number> {
    return this.redisService.incrementWithExpiry(
      this.getKey(clientId),
      this.runtimeConfig.loginThrottleWindowSeconds,
    );
  }

  async clearAttempts(clientId: string): Promise<void> {
    await this.redisService.clear(this.getKey(clientId));
  }

  isBlockedAttemptCount(attemptCount: number): boolean {
    return attemptCount >= this.runtimeConfig.loginThrottleMaxAttempts;
  }

  private getKey(clientId: string): string {
    return `auth:login:${clientId}`;
  }
}
