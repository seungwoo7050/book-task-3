import { beforeEach, describe, expect, it } from "vitest";

import { createElement, render, resetRuntime } from "../src";

describe("delegated events", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    resetRuntime();
  });

  it("bubbles delegated events through the runtime tree", () => {
    const container = document.createElement("div");
    const calls: string[] = [];

    function App() {
      return createElement(
        "section",
        {
          onClick: () => calls.push("section"),
        },
        createElement(
          "button",
          {
            onClick: () => calls.push("button"),
          },
          "Fire",
        ),
      );
    }

    render(createElement(App, null), container);
    container.querySelector("button")?.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(calls).toEqual(["button", "section"]);
  });

  it("supports stopPropagation on delegated events", () => {
    const container = document.createElement("div");
    const calls: string[] = [];

    function App() {
      return createElement(
        "section",
        {
          onClick: () => calls.push("section"),
        },
        createElement(
          "button",
          {
            onClick: (event: { stopPropagation(): void }) => {
              calls.push("button");
              event.stopPropagation();
            },
          },
          "Fire",
        ),
      );
    }

    render(createElement(App, null), container);
    container.querySelector("button")?.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(calls).toEqual(["button"]);
  });
});
