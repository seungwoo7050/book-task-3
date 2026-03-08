import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
  BadRequestException,
} from "@nestjs/common";
import { Response } from "express";

@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message: string | string[] = "Internal Server Error";
    let details: unknown = undefined;

    if (exception instanceof BadRequestException) {
      status = exception.getStatus();
      const exResponse = exception.getResponse();
      if (typeof exResponse === "object" && exResponse !== null) {
        const obj = exResponse as Record<string, unknown>;
        message = (obj.message as string | string[]) ?? exception.message;
        if (Array.isArray(message)) {
          details = message;
          message = "Validation failed";
        }
      } else {
        message = exception.message;
      }
    } else if (exception instanceof HttpException) {
      status = exception.getStatus();
      message = exception.message;
    }

    const errorBody: Record<string, unknown> = {
      statusCode: status,
      message,
    };

    if (details) {
      errorBody.details = details;
    }

    response.status(status).json({
      success: false,
      error: errorBody,
    });
  }
}
