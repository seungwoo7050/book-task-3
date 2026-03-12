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
}
