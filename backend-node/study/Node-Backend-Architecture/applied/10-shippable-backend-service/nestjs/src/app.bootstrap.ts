import { type INestApplication, ValidationPipe } from "@nestjs/common";
import { DocumentBuilder, SwaggerModule } from "@nestjs/swagger";

import { HttpExceptionFilter } from "./common/filters/http-exception.filter";
import { TransformInterceptor } from "./common/interceptors/transform.interceptor";
import { StructuredLoggingInterceptor } from "./runtime/structured-logging.interceptor";
import { RuntimeConfigService } from "./runtime/runtime-config.service";

export async function configureApp(
  app: INestApplication,
  options: { listen?: boolean } = {},
): Promise<void> {
  const runtimeConfig = app.get(RuntimeConfigService);

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );
  app.useGlobalFilters(new HttpExceptionFilter());
  app.useGlobalInterceptors(app.get(StructuredLoggingInterceptor), new TransformInterceptor());

  const swaggerConfig = new DocumentBuilder()
    .setTitle("Shippable Backend Service")
    .setDescription("Portfolio-ready NestJS service for junior backend applications")
    .setVersion("1.0.0")
    .addBearerAuth()
    .build();
  const swaggerDocument = SwaggerModule.createDocument(app, swaggerConfig);
  SwaggerModule.setup("docs", app, swaggerDocument);

  if (options.listen === false) {
    await app.init();
    return;
  }

  await app.listen(runtimeConfig.port);
}
