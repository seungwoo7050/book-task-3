import { createElement } from "@front-react/vdom-foundations";
import { beforeEach, describe, expect, it } from "vitest";

import { applyPatches } from "../src/patch";

describe("applyPatches", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
  });

  it("creates and removes DOM nodes according to patches", () => {
    const parent = document.createElement("div");

    applyPatches(parent, [
      {
        type: "CREATE",
        newNode: createElement("span", { title: "first" }, "Hello"),
        index: 0,
      },
    ]);

    expect(parent.querySelector("span")?.textContent).toBe("Hello");

    applyPatches(parent, [
      {
        type: "REMOVE",
        index: 0,
      },
    ]);

    expect(parent.childNodes).toHaveLength(0);
  });
});
