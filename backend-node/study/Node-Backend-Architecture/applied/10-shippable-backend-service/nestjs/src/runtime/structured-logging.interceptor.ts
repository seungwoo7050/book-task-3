import {
  type CallHandler,
  type ExecutionContext,
  Inject,
  Injectable,
  type NestInterceptor,
} from "@nestjs/common";
import { Observable, tap } from "rxjs";

import { RuntimeConfigService } from "./runtime-config.service";

type HttpRequestLike = {
  method: string;
  headers: Record<string, string | string[] | undefined>;
  originalUrl?: string;
  url?: string;
  requestId?: string;
};

type HttpResponseLike = {
  setHeader(name: string, value: string): void;
  statusCode: number;
};

@Injectable()
export class StructuredLoggingInterceptor implements NestInterceptor {
  constructor(
    @Inject(RuntimeConfigService)
    private readonly runtimeConfig: RuntimeConfigService,
  ) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<unknown> {
    if (context.getType() !== "http") {
      return next.handle();
    }

    const request = context.switchToHttp().getRequest<HttpRequestLike>();
    const response = context.switchToHttp().getResponse<HttpResponseLike>();
    const requestIdHeader = request.headers["x-request-id"];
    const requestId = Array.isArray(requestIdHeader)
      ? requestIdHeader[0] ?? request.requestId ?? "unknown-request-id"
      : requestIdHeader ?? request.requestId ?? "generated-request-id";
    const startedAt = Date.now();

    response.setHeader("x-request-id", requestId);

    return next.handle().pipe(
      tap({
        next: () => {
          this.logRequest("ok", request, response, requestId, startedAt);
        },
        error: () => {
          this.logRequest("error", request, response, requestId, startedAt);
        },
      }),
    );
  }

  private logRequest(
    outcome: "ok" | "error",
    request: HttpRequestLike,
    response: HttpResponseLike,
    requestId: string,
    startedAt: number,
  ): void {
    const config = this.runtimeConfig.snapshot;
    const payload = {
      level: config.logLevel,
      appName: config.appName,
      environment: config.environment,
      requestId,
      method: request.method,
      path: request.originalUrl ?? request.url ?? "/",
      statusCode: response.statusCode,
      durationMs: Date.now() - startedAt,
      outcome,
    };

    process.stdout.write(`${JSON.stringify(payload)}\n`);
  }
}
