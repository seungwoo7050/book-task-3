import { beforeEach, describe, expect, it } from "vitest";

import { createElement, render, resetRuntime, useEffect, useState } from "../src";

describe("runtime integration", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    resetRuntime();
  });

  it("keeps event updates and effect timing in one runtime flow", () => {
    const container = document.createElement("div");
    const lifecycle: string[] = [];

    function App() {
      const [status, setStatus] = useState("idle");

      useEffect(() => {
        lifecycle.push(`effect:${status}`);
      }, [status]);

      return createElement(
        "main",
        null,
        createElement("p", { title: "status" }, `Status: ${status}`),
        createElement(
          "button",
          {
            onClick: () => setStatus("ready"),
          },
          "Advance",
        ),
      );
    }

    render(createElement(App, null), container);
    expect(lifecycle).toEqual(["effect:idle"]);
    expect(container.querySelector("[title='status']")?.textContent).toBe("Status: idle");

    container.querySelector("button")?.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(container.querySelector("[title='status']")?.textContent).toBe("Status: ready");
    expect(lifecycle).toEqual(["effect:idle", "effect:ready"]);
  });
});
