import { describe, it, expect, beforeEach } from "vitest";
import { validate } from "../../src/middleware/validate";
import { CreateBookSchema } from "../../src/schemas/book.schema";
import { Request, Response, NextFunction } from "express";
import { ValidationError } from "../../src/errors";

function mockReq(body: unknown): Request {
  return { body } as Request;
}

function mockRes(): Response {
  return {} as Response;
}

describe("validate middleware", () => {
  const middleware = validate(CreateBookSchema);

  it("should call next() with valid body", () => {
    const req = mockReq({
      title: "Test",
      author: "Author",
      publishedYear: 2024,
      genre: "Fiction",
      price: 19.99,
    });
    const res = mockRes();
    let called = false;
    const next: NextFunction = () => {
      called = true;
    };

    middleware(req, res, next);
    expect(called).toBe(true);
  });

  it("should call next with ValidationError for invalid body", () => {
    const req = mockReq({ title: "" }); // missing required fields
    const res = mockRes();
    let passedError: unknown;
    const next: NextFunction = (err?: unknown) => {
      passedError = err;
    };

    middleware(req, res, next);
    expect(passedError).toBeInstanceOf(ValidationError);
    expect((passedError as ValidationError).details.length).toBeGreaterThan(0);
  });

  it("should include field paths in validation details", () => {
    const req = mockReq({ title: "T", author: "A", publishedYear: "not a number", genre: "G", price: -5 });
    const res = mockRes();
    let passedError: unknown;
    const next: NextFunction = (err?: unknown) => {
      passedError = err;
    };

    middleware(req, res, next);
    const err = passedError as ValidationError;
    const fields = err.details.map((d) => d.field);
    expect(fields).toContain("publishedYear");
    expect(fields).toContain("price");
  });
});
