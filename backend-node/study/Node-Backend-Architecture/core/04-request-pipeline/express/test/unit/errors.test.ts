import { describe, it, expect, beforeEach } from "vitest";
import { AppError, NotFoundError, ValidationError } from "../../src/errors";

describe("Error Classes", () => {
  describe("AppError", () => {
    it("should have correct statusCode and message", () => {
      const err = new AppError(418, "I am a teapot");
      expect(err.statusCode).toBe(418);
      expect(err.message).toBe("I am a teapot");
      expect(err.name).toBe("AppError");
      expect(err).toBeInstanceOf(Error);
    });
  });

  describe("NotFoundError", () => {
    it("should default to 404 with a default message", () => {
      const err = new NotFoundError();
      expect(err.statusCode).toBe(404);
      expect(err.message).toBe("Resource not found");
      expect(err).toBeInstanceOf(AppError);
    });

    it("should accept custom message", () => {
      const err = new NotFoundError("Book not found");
      expect(err.message).toBe("Book not found");
    });
  });

  describe("ValidationError", () => {
    it("should have 400 status and details", () => {
      const err = new ValidationError("검증 실패", [
        { field: "title", message: "Required" },
      ]);
      expect(err.statusCode).toBe(400);
      expect(err.details).toHaveLength(1);
      expect(err.details[0].field).toBe("title");
      expect(err).toBeInstanceOf(AppError);
    });
  });
});
