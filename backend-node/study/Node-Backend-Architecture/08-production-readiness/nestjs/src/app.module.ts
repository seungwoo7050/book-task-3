import { Module } from "@nestjs/common";
import { APP_INTERCEPTOR } from "@nestjs/core";

import { HealthController } from "./health.controller";
import { loadRuntimeConfig } from "./runtime/runtime-config";
import { RuntimeConfigService } from "./runtime/runtime-config.service";
import { RUNTIME_CONFIG } from "./runtime/runtime.constants";
import { StructuredLoggingInterceptor } from "./runtime/structured-logging.interceptor";

@Module({
  controllers: [HealthController],
  providers: [
    {
      provide: RUNTIME_CONFIG,
      useFactory: () => loadRuntimeConfig(process.env),
    },
    RuntimeConfigService,
    {
      provide: APP_INTERCEPTOR,
      inject: [RuntimeConfigService],
      useFactory: (runtimeConfig: RuntimeConfigService) => {
        return new StructuredLoggingInterceptor(runtimeConfig);
      },
    },
  ],
})
export class AppModule {}
