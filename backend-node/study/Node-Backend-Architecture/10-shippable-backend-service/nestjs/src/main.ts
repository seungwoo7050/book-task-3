import "dotenv/config";

import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";
import { configureApp } from "./app.bootstrap";
import { RuntimeConfigService } from "./runtime/runtime-config.service";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await configureApp(app, { listen: true });
  const runtimeConfig = app.get(RuntimeConfigService);
  console.log(`Server running on http://localhost:${runtimeConfig.port}`);
}

bootstrap();
