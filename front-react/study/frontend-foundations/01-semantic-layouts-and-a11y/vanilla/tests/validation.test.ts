import { describe, expect, it } from "vitest";
import { hasValidationErrors, validateSettings } from "../src/validation";

describe("validateSettings", () => {
  it("returns errors for a short workspace name and invalid email", () => {
    const errors = validateSettings({
      workspaceName: "ab",
      supportEmail: "ops-at-example",
      timezone: "Asia/Seoul",
    });

    expect(errors.workspaceName).toContain("at least 3 characters");
    expect(errors.supportEmail).toContain("valid support email");
    expect(hasValidationErrors(errors)).toBe(true);
  });

  it("accepts valid values", () => {
    const errors = validateSettings({
      workspaceName: "Ops North",
      supportEmail: "ops@example.com",
      timezone: "Asia/Seoul",
    });

    expect(errors).toEqual({});
    expect(hasValidationErrors(errors)).toBe(false);
  });
});
