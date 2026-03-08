import { describe, expect, it } from "vitest";
import {
  defaultWorkspaceProfile,
  readWorkspaceProfile,
  resetPortalState,
  writeWorkspaceProfile,
} from "@/lib/storage";

describe("storage", () => {
  it("restores a saved workspace profile draft", () => {
    resetPortalState();
    writeWorkspaceProfile({
      ...defaultWorkspaceProfile,
      workspaceName: "Lattice Cloud",
      industry: "Developer tooling",
      region: "Seoul",
      teamSize: "11-50",
      complianceEmail: "compliance@latticecloud.dev",
    });

    expect(readWorkspaceProfile().workspaceName).toBe("Lattice Cloud");
  });
});
