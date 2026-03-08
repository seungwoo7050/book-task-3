import { beforeEach, describe, expect, it, vi } from "vitest";

import { mountRuntimeDemo, resetRuntimeDemo } from "../src/app";

describe("runtime demo app", () => {
  beforeEach(() => {
    document.body.innerHTML = '<div id="app"></div>';
    resetRuntimeDemo();
    vi.useFakeTimers();
  });

  it("filters results after the debounce window and updates metrics", async () => {
    const container = document.querySelector<HTMLElement>("#app");
    if (!container) {
      throw new Error("Missing app root for test.");
    }

    mountRuntimeDemo(container);

    const input = container.querySelector<HTMLInputElement>("#runtime-search");
    if (!input) {
      throw new Error("Missing search input.");
    }

    input.value = "metrics";
    input.dispatchEvent(new Event("input", { bubbles: true }));

    expect(container.textContent).toContain("Showing 4 of 10 matches");

    await vi.advanceTimersByTimeAsync(260);

    expect(container.textContent).toContain("Showing 2 of 2 matches");
    expect(container.querySelector("#metric-query")?.textContent).toBe("metrics");
  });

  it("loads the next page of results and updates visible metrics", () => {
    const container = document.querySelector<HTMLElement>("#app");
    if (!container) {
      throw new Error("Missing app root for test.");
    }

    mountRuntimeDemo(container);

    const button = container.querySelector<HTMLButtonElement>(".load-more");
    if (!button) {
      throw new Error("Missing load more button.");
    }

    button.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(container.textContent).toContain("Showing 8 of 10 matches");
    expect(container.querySelector("#metric-visible")?.textContent).toBe("8");
  });

  it("keeps render metrics visible after multiple interactions", async () => {
    const container = document.querySelector<HTMLElement>("#app");
    if (!container) {
      throw new Error("Missing app root for test.");
    }

    mountRuntimeDemo(container);

    const input = container.querySelector<HTMLInputElement>("#runtime-search");
    const button = container.querySelector<HTMLButtonElement>(".load-more");
    if (!input || !button) {
      throw new Error("Missing demo controls.");
    }

    button.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    input.value = "interaction";
    input.dispatchEvent(new Event("input", { bubbles: true }));
    await vi.advanceTimersByTimeAsync(260);

    const renderCount = Number(container.querySelector("#metric-renders")?.textContent ?? "0");
    expect(renderCount).toBeGreaterThan(1);
    expect(container.querySelector("#metric-commit-ms")?.textContent).toContain("ms");
  });
});
