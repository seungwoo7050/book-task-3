import { beforeEach, describe, expect, it } from "vitest";

import { createElement, render, resetRuntime, useState } from "../src";

describe("useState", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    resetRuntime();
  });

  it("re-renders when state updates from an event handler", () => {
    const container = document.createElement("div");

    function Counter() {
      const [count, setCount] = useState(0);

      return createElement(
        "button",
        {
          onClick: () => setCount((value) => value + 1),
        },
        `Count: ${count}`,
      );
    }

    render(createElement(Counter, null), container);

    const button = container.querySelector("button");
    button?.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(container.textContent).toContain("Count: 1");
  });

  it("throws when the hook count changes between renders", () => {
    const container = document.createElement("div");

    function ToggleHooks(props: { enabled: boolean }) {
      useState("always");
      if (props.enabled) {
        useState("conditional");
      }
      return createElement("div", null, props.enabled ? "On" : "Off");
    }

    render(createElement(ToggleHooks, { enabled: true }), container);

    expect(() => {
      render(createElement(ToggleHooks, { enabled: false }), container);
    }).toThrow(/Hook order changed/);
  });
});
