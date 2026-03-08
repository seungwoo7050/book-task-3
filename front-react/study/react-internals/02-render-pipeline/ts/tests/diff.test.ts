import { createElement } from "@front-react/vdom-foundations";
import { describe, expect, it } from "vitest";

import { diff, diffChildren, diffProps } from "../src/diff";

describe("diffProps", () => {
  it("returns changed and removed props", () => {
    expect(
      diffProps(
        { className: "old", title: "keep", children: [] },
        { className: "new", children: [] },
      ),
    ).toEqual({
      set: { className: "new" },
      remove: ["title"],
    });
  });
});

describe("diffChildren", () => {
  it("diffs index-based children by position", () => {
    const oldChildren = [createElement("li", null, "One"), createElement("li", null, "Two")];
    const newChildren = [createElement("li", null, "One"), createElement("li", null, "Three")];

    const patches = diffChildren(oldChildren, newChildren);
    expect(patches).toHaveLength(1);
    expect(patches[0].type).toBe("UPDATE");
    expect(patches[0].index).toBe(1);
  });

  it("uses keys to identify create and remove patches", () => {
    const oldChildren = [
      createElement("li", { key: "alpha" }, "One"),
      createElement("li", { key: "beta" }, "Two"),
    ];
    const newChildren = [
      createElement("li", { key: "beta" }, "Two"),
      createElement("li", { key: "gamma" }, "Three"),
    ];

    const patches = diffChildren(oldChildren, newChildren);
    expect(patches.some((patch) => patch.type === "REMOVE")).toBe(true);
    expect(patches.some((patch) => patch.type === "CREATE")).toBe(true);
  });
});

describe("diff", () => {
  it("returns replace for type changes", () => {
    const oldNode = createElement("div", null, "Old");
    const newNode = createElement("section", null, "New");

    expect(diff(oldNode, newNode)).toMatchObject({ type: "REPLACE" });
  });
});
