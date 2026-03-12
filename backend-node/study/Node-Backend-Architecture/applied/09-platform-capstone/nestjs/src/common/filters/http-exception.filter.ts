import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from "@nestjs/common";
import { Response } from "express";

@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = "Internal server error";
    let details: unknown = undefined;

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const body = exception.getResponse();
      if (typeof body === "string") {
        message = body;
      } else if (typeof body === "object" && body !== null) {
        const obj = body as Record<string, unknown>;
        message = (obj.message as string) || (obj.error as string) || message;
        if (Array.isArray(obj.message)) {
          details = obj.message;
          message = "검증 실패";
        }
      }
    }

    response.status(status).json({
      success: false,
      error: { status, message, ...(details ? { details } : {}) },
    });
  }
}
