import * as matchers from "@testing-library/jest-dom/matchers";
import { cleanup } from "@testing-library/react";
import { afterEach, beforeEach, expect, vi } from "vitest";
import {
  resetIssues,
  resetRuntimeConfig,
  updateRuntimeConfig,
} from "@/lib/storage";

class ResizeObserverMock {
  observe() {}
  unobserve() {}
  disconnect() {}
}

expect.extend(matchers);

beforeEach(() => {
  window.localStorage.clear();
  resetIssues();
  resetRuntimeConfig();
  updateRuntimeConfig({
    latencyMs: 0,
    failureRate: 0,
    failNextRequest: false,
    mode: "stable",
  });

  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });

  Object.defineProperty(window, "ResizeObserver", {
    writable: true,
    value: ResizeObserverMock,
  });

  window.HTMLElement.prototype.scrollIntoView = vi.fn();
  window.HTMLElement.prototype.hasPointerCapture = vi.fn(() => false);
  window.HTMLElement.prototype.setPointerCapture = vi.fn();
  window.HTMLElement.prototype.releasePointerCapture = vi.fn();
});

afterEach(() => {
  cleanup();
});
