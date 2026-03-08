import { Global, Module } from "@nestjs/common";

import { RUNTIME_CONFIG } from "./runtime.constants";
import { loadRuntimeConfig } from "./runtime-config";
import { RuntimeConfigService } from "./runtime-config.service";
import { RedisService } from "./redis.service";

@Global()
@Module({
  providers: [
    {
      provide: RUNTIME_CONFIG,
      useFactory: () => loadRuntimeConfig(process.env),
    },
    RuntimeConfigService,
    RedisService,
  ],
  exports: [RuntimeConfigService, RedisService],
})
export class RuntimeModule {}
