import { Controller, Get, Inject, ServiceUnavailableException } from "@nestjs/common";
import { DataSource } from "typeorm";

import { RedisService } from "./runtime/redis.service";

@Controller("health")
export class HealthController {
  constructor(
    @Inject(DataSource)
    private readonly dataSource: DataSource,
    @Inject(RedisService)
    private readonly redisService: RedisService,
  ) {}

  @Get("live")
  getLiveness() {
    return { status: "ok" };
  }

  @Get("ready")
  async getReadiness() {
    let databaseReady = false;
    try {
      await this.dataSource.query("SELECT 1");
      databaseReady = true;
    } catch {
      databaseReady = false;
    }

    const redisReady = await this.redisService.isReady();

    if (!databaseReady || !redisReady) {
      throw new ServiceUnavailableException({
        status: "degraded",
        databaseReady,
        redisReady,
      });
    }

    return {
      status: "ready",
      databaseReady: true,
      redisReady: true,
    };
  }
}
