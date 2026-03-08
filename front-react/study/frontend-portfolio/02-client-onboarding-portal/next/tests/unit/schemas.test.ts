import { describe, expect, it } from "vitest";
import { inviteInputSchema, signInSchema, workspaceProfileSchema } from "@/lib/schemas";

describe("schemas", () => {
  it("validates sign-in and workspace profile input", () => {
    expect(() =>
      signInSchema.parse({
        email: "owner@latticecloud.dev",
        password: "launch-ready",
      }),
    ).not.toThrow();

    expect(() =>
      workspaceProfileSchema.parse({
        workspaceName: "Lattice Cloud",
        industry: "Developer tooling",
        region: "Seoul",
        teamSize: "11-50",
        complianceEmail: "compliance@latticecloud.dev",
      }),
    ).not.toThrow();
  });

  it("rejects malformed invite emails", () => {
    expect(() =>
      inviteInputSchema.parse({
        email: "not-an-email",
        role: "Collaborator",
      }),
    ).toThrow();
  });
});
