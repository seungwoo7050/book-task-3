import {
  Controller,
  Get,
  Inject,
  ServiceUnavailableException,
} from "@nestjs/common";

import { RuntimeConfigService } from "./runtime/runtime-config.service";

@Controller()
export class HealthController {
  constructor(
    @Inject(RuntimeConfigService)
    private readonly runtimeConfig: RuntimeConfigService,
  ) {}

  @Get("health")
  getHealth() {
    const config = this.runtimeConfig.snapshot;

    return {
      status: "ok",
      appName: config.appName,
      environment: config.environment,
      timestamp: new Date().toISOString(),
    };
  }

  @Get("ready")
  getReady() {
    const config = this.runtimeConfig.snapshot;

    if (!config.ready) {
      throw new ServiceUnavailableException({
        status: "not-ready",
        appName: config.appName,
        reason: "Set READY=true after dependencies are available.",
      });
    }

    return {
      status: "ready",
      appName: config.appName,
      environment: config.environment,
    };
  }
}
