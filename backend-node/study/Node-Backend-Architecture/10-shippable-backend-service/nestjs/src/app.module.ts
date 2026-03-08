import { MiddlewareConsumer, Module, NestModule } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { EventEmitterModule } from "@nestjs/event-emitter";
import { AuthModule } from "./auth/auth.module";
import { BooksModule } from "./books/books.module";
import { EventsModule } from "./events/events.module";
import { RuntimeModule } from "./runtime/runtime.module";
import { RuntimeConfigService } from "./runtime/runtime-config.service";
import { createTypeOrmModuleOptions } from "./database/database-options";
import { HealthController } from "./health.controller";
import { StructuredLoggingInterceptor } from "./runtime/structured-logging.interceptor";
import { RequestIdMiddleware } from "./common/middleware/request-id.middleware";

@Module({
  imports: [
    RuntimeModule,
    TypeOrmModule.forRootAsync({
      imports: [RuntimeModule],
      inject: [RuntimeConfigService],
      useFactory: (runtimeConfig: RuntimeConfigService) =>
        createTypeOrmModuleOptions(runtimeConfig.snapshot),
    }),
    EventEmitterModule.forRoot(),
    AuthModule,
    BooksModule,
    EventsModule,
  ],
  controllers: [HealthController],
  providers: [StructuredLoggingInterceptor],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer.apply(RequestIdMiddleware).forRoutes("*");
  }
}
