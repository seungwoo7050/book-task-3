import { cleanup } from "@testing-library/react";
import { afterEach, vi } from "vitest";

type MockRoute = {
  body: unknown;
  method?: string;
  path: string;
  status?: number;
};

function normalizeUrl(input: RequestInfo | URL): string {
  if (typeof input === "string") {
    return input;
  }
  if (input instanceof URL) {
    return input.toString();
  }
  return input.url;
}

export function mockFetchRoutes(routes: MockRoute[]) {
  const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = normalizeUrl(input);
    const path = url.replace(/^https?:\/\/[^/]+/, "");
    const method = (init?.method ?? "GET").toUpperCase();
    const match = routes.find((route) => (route.method ?? "GET").toUpperCase() === method && route.path === path);
    if (!match) {
      return new Response(JSON.stringify({ detail: `No mock for ${method} ${path}` }), {
        status: 404,
        headers: { "Content-Type": "application/json" },
      });
    }
    return new Response(JSON.stringify(match.body), {
      status: match.status ?? 200,
      headers: { "Content-Type": "application/json" },
    });
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});
