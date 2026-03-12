import { randomUUID } from "node:crypto";

import { Injectable, type NestMiddleware } from "@nestjs/common";
import type { NextFunction, Request, Response } from "express";

type RequestWithId = Request & {
  requestId?: string;
};

@Injectable()
export class RequestIdMiddleware implements NestMiddleware {
  use(request: RequestWithId, response: Response, next: NextFunction): void {
    const requestId = request.header("x-request-id")?.trim() || randomUUID();

    request.requestId = requestId;
    response.setHeader("x-request-id", requestId);
    next();
  }
}
