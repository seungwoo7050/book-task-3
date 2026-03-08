import { Inject, Injectable, Logger, OnModuleDestroy, OnModuleInit } from "@nestjs/common";
import { createClient, type RedisClientType } from "redis";

import { RuntimeConfigService } from "./runtime-config.service";

@Injectable()
export class RedisService implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(RedisService.name);
  private readonly client: RedisClientType;

  constructor(
    @Inject(RuntimeConfigService)
    private readonly runtimeConfig: RuntimeConfigService,
  ) {
    this.client = createClient({
      url: this.runtimeConfig.redisUrl,
      socket: {
        reconnectStrategy: (retries) => Math.min(retries * 100, 1000),
      },
    });

    this.client.on("error", (error) => {
      this.logger.warn(`Redis connection error: ${String(error)}`);
    });
  }

  async onModuleInit(): Promise<void> {
    await this.ensureConnected();
  }

  async onModuleDestroy(): Promise<void> {
    if (this.client.isOpen) {
      await this.client.quit();
    }
  }

  async isReady(): Promise<boolean> {
    if (!(await this.ensureConnected())) {
      return false;
    }

    try {
      return (await this.client.ping()) === "PONG";
    } catch {
      return false;
    }
  }

  async getJson<T>(key: string): Promise<T | null> {
    if (!(await this.ensureConnected())) {
      return null;
    }

    const value = await this.client.get(key);
    return value ? (JSON.parse(value) as T) : null;
  }

  async get(key: string): Promise<string | null> {
    if (!(await this.ensureConnected())) {
      return null;
    }

    return this.client.get(key);
  }

  async setJson(key: string, value: unknown, ttlSeconds: number): Promise<void> {
    if (!(await this.ensureConnected())) {
      return;
    }

    await this.client.set(key, JSON.stringify(value), {
      EX: ttlSeconds,
    });
  }

  async delete(key: string): Promise<void> {
    if (!(await this.ensureConnected())) {
      return;
    }

    await this.client.del(key);
  }

  async deleteMany(keys: string[]): Promise<void> {
    if (keys.length === 0 || !(await this.ensureConnected())) {
      return;
    }

    await this.client.del(keys);
  }

  async incrementWithExpiry(key: string, ttlSeconds: number): Promise<number> {
    if (!(await this.ensureConnected())) {
      return 0;
    }

    const attempts = await this.client.incr(key);
    if (attempts === 1) {
      await this.client.expire(key, ttlSeconds);
    }

    return attempts;
  }

  async clear(key: string): Promise<void> {
    await this.delete(key);
  }

  private async ensureConnected(): Promise<boolean> {
    if (this.client.isOpen) {
      return true;
    }

    try {
      await this.client.connect();
      return true;
    } catch {
      return false;
    }
  }
}
