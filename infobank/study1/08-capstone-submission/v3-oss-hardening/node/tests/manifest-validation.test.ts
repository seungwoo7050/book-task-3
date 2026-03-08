import { mcpManifestSchema } from "@study1-v3/shared";
import { describe, expect, it } from "vitest";

describe("manifest validation", () => {
  it("rejects incomplete manifests", () => {
    const parsed = mcpManifestSchema.safeParse({
      id: "bad",
      slug: "bad",
      name: "Bad",
      version: "1.0.0"
    });

    expect(parsed.success).toBe(false);
  });
});
