import { describe, expect, it } from "vitest";
import { canSubmitOnboarding, coerceStep } from "@/lib/guards";
import { defaultChecklist, defaultWorkspaceProfile } from "@/lib/storage";

describe("coerceStep", () => {
  it("falls back to workspace for unknown values", () => {
    expect(coerceStep("unknown")).toBe("workspace");
    expect(coerceStep("review")).toBe("review");
  });
});

describe("canSubmitOnboarding", () => {
  it("requires profile, invite, and completed checklist items", () => {
    const profile = {
      ...defaultWorkspaceProfile,
      workspaceName: "Lattice Cloud",
      industry: "Developer tooling",
      region: "Seoul",
      teamSize: "11-50",
      complianceEmail: "compliance@latticecloud.dev",
    };
    const invites = [
      {
        id: "invite-1",
        email: "ops@latticecloud.dev",
        role: "Admin" as const,
        status: "pending" as const,
      },
    ];
    const incompleteChecklist = defaultChecklist;
    const completeChecklist = defaultChecklist.map((item) => ({
      ...item,
      completed: true,
    }));

    expect(canSubmitOnboarding(profile, invites, incompleteChecklist)).toBe(false);
    expect(canSubmitOnboarding(profile, invites, completeChecklist)).toBe(true);
  });
});
