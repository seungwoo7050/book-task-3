import { NestFactory } from "@nestjs/core";

import { AppModule } from "./app.module";
import { RuntimeConfigService } from "./runtime/runtime-config.service";

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule);
  const config = app.get(RuntimeConfigService).snapshot;

  await app.listen(config.port);
}

bootstrap();
