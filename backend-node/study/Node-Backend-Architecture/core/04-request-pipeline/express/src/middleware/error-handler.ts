import { Request, Response, NextFunction } from "express";
import { AppError } from "../errors/app-error";
import { ValidationError } from "../errors/validation-error";

export function errorHandler(
  err: Error,
  _req: Request,
  res: Response,
  _next: NextFunction,
): void {
  if (err instanceof ValidationError) {
    res.status(err.statusCode).json({
      success: false,
      error: {
        message: err.message,
        statusCode: err.statusCode,
        details: err.details,
      },
    });
    return;
  }

  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      success: false,
      error: {
        message: err.message,
        statusCode: err.statusCode,
      },
    });
    return;
  }

  // 잘못된 JSON에서 express.json()이 던진 SyntaxError
  if (err instanceof SyntaxError && "body" in err) {
    res.status(400).json({
      success: false,
      error: {
        message: "Invalid JSON",
        statusCode: 400,
      },
    });
    return;
  }

  console.error("[Unhandled Error]", err);
  res.status(500).json({
    success: false,
    error: {
      message: "Internal Server Error",
      statusCode: 500,
    },
  });
}
