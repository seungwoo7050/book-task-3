import { beforeEach, describe, expect, it, vi } from "vitest";

import { createElement, render, resetRuntime, useEffect, useState } from "../src";

describe("useEffect", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    resetRuntime();
  });

  it("runs effects after commit and cleans them up before the next effect", () => {
    const container = document.createElement("div");
    const calls: string[] = [];

    function EffectCounter() {
      const [count, setCount] = useState(0);

      useEffect(() => {
        calls.push(`setup:${count}`);
        return () => {
          calls.push(`cleanup:${count}`);
        };
      }, [count]);

      return createElement(
        "button",
        {
          onClick: () => setCount((value) => value + 1),
        },
        `Count: ${count}`,
      );
    }

    render(createElement(EffectCounter, null), container);
    expect(calls).toEqual(["setup:0"]);

    container.querySelector("button")?.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(calls).toEqual(["setup:0", "cleanup:0", "setup:1"]);
  });

  it("runs cleanup when a component unmounts", () => {
    const container = document.createElement("div");
    const cleanup = vi.fn();

    function Leaf() {
      useEffect(() => cleanup, []);
      return createElement("p", null, "Leaf");
    }

    render(createElement(Leaf, null), container);
    render(createElement("section", null, "Gone"), container);

    expect(cleanup).toHaveBeenCalledTimes(1);
  });
});
