import { describe, expect, it, vi } from "vitest";

import {
  fetchInventorySnapshot,
  formatBookCard,
  normalizeTags,
  toNormalizedBook,
} from "../src/catalog";
import { runCli } from "../src/cli";

describe("catalog helpers", () => {
  it("normalizes and deduplicates tags", () => {
    expect(normalizeTags([" Node ", "architecture", "node", "Type Script"])).toEqual([
      "architecture",
      "node",
      "type-script",
    ]);
  });

  it("builds a normalized book", () => {
    expect(
      toNormalizedBook({
        title: " Node Patterns ",
        author: " Alice ",
        publishedYear: 2024,
        tags: ["Node", "Architecture", "node"],
      }),
    ).toEqual({
      slug: "node-patterns-2024",
      title: "Node Patterns",
      author: "Alice",
      publishedYear: 2024,
      tags: ["architecture", "node"],
      summary: "Alice wrote Node Patterns in 2024.",
    });
  });

  it("captures per-item inventory failures without failing the whole batch", async () => {
    const fetchStock = vi.fn(async (slug: string) => {
      if (slug === "broken-book") {
        throw new Error("service unavailable");
      }

      return slug.length;
    });

    await expect(fetchInventorySnapshot(["clean-book", "broken-book"], { fetchStock })).resolves.toEqual([
      { slug: "clean-book", inStock: 10 },
      { slug: "broken-book", inStock: null, error: "service unavailable" },
    ]);
  });

  it("formats a human-readable card", () => {
    const card = formatBookCard(
      {
        slug: "node-patterns-2024",
        title: "Node Patterns",
        author: "Alice",
        publishedYear: 2024,
        tags: ["architecture", "node"],
        summary: "Backend patterns",
      },
      { slug: "node-patterns-2024", inStock: 4 },
    );

    expect(card).toContain("Node Patterns (2024)");
    expect(card).toContain("Inventory: 4");
  });
});

describe("cli", () => {
  it("prints a formatted card for valid input", () => {
    const stdout = { write: vi.fn() };
    const stderr = { write: vi.fn() };

    const exitCode = runCli(
      ["--title", "Node Patterns", "--author", "Alice", "--year", "2024", "--tags", "Node,Architecture"],
      stdout,
      stderr,
    );

    expect(exitCode).toBe(0);
    expect(stdout.write).toHaveBeenCalledOnce();
    expect(stderr.write).not.toHaveBeenCalled();
  });

  it("returns a non-zero exit code for invalid input", () => {
    const stdout = { write: vi.fn() };
    const stderr = { write: vi.fn() };

    const exitCode = runCli(["--title", "Only Title"], stdout, stderr);

    expect(exitCode).toBe(1);
    expect(stderr.write).toHaveBeenCalledWith("Required flags: --title --author --year --tags\n");
  });
});
