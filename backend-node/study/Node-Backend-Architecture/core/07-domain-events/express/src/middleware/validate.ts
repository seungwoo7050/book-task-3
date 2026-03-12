import { Request, Response, NextFunction } from "express";
import { ZodSchema, ZodError } from "zod";
import { ValidationError } from "../errors";

export function validate(schema: ZodSchema) {
  return (req: Request, _res: Response, next: NextFunction): void => {
    try { req.body = schema.parse(req.body); next(); }
    catch (err) {
      if (err instanceof ZodError) {
        next(new ValidationError("검증 실패", err.errors.map((e) => ({ field: e.path.join("."), message: e.message }))));
        return;
      }
      next(err);
    }
  };
}
