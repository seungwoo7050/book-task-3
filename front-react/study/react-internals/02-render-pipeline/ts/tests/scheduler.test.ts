import { createElement } from "@front-react/vdom-foundations";
import { beforeEach, describe, expect, it } from "vitest";

import { flushSync, render, resetScheduler, workLoop } from "../src/scheduler";

describe("scheduler", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    resetScheduler();
  });

  it("does not mutate the DOM during the render phase", () => {
    const container = document.createElement("div");

    render(createElement("section", { title: "alpha" }, "Ready"), container);

    expect(container.childNodes).toHaveLength(0);
  });

  it("commits the tree when flushSync completes all work", () => {
    const container = document.createElement("div");

    render(
      createElement(
        "section",
        { title: "alpha" },
        createElement("p", null, "Ready"),
      ),
      container,
    );

    flushSync();

    expect(container.querySelector("section")?.getAttribute("title")).toBe("alpha");
    expect(container.textContent).toContain("Ready");
  });

  it("supports interrupted work before commit", () => {
    const container = document.createElement("div");

    render(
      createElement(
        "section",
        null,
        createElement("p", null, "Step 1"),
        createElement("p", null, "Step 2"),
      ),
      container,
    );

    let firstPass = true;
    workLoop({
      timeRemaining() {
        if (firstPass) {
          firstPass = false;
          return 1;
        }
        return 0;
      },
    });

    expect(container.childNodes).toHaveLength(0);

    flushSync();

    expect(container.textContent).toContain("Step 1");
    expect(container.textContent).toContain("Step 2");
  });
});
