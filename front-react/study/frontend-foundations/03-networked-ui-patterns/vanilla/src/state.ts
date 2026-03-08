import type { DirectoryCategory, DirectoryQuery, ExplorerUrlState } from "./types";

export const DEFAULT_QUERY: DirectoryQuery = {
  search: "",
  category: "all",
};

export function parseUrlState(search: string): Partial<ExplorerUrlState> {
  const params = new URLSearchParams(search);
  const parsed: Partial<ExplorerUrlState> = {};
  const category = params.get("category");
  const query = params.get("search");
  const item = params.get("item");

  if (query) {
    parsed.search = query;
  }

  if (category === "all" || category === "runbook" || category === "policy" || category === "guide") {
    parsed.category = category as DirectoryCategory;
  }

  if (item) {
    parsed.item = item;
  }

  return parsed;
}

export function serializeUrlState(state: ExplorerUrlState): string {
  const params = new URLSearchParams();

  if (state.search.trim()) {
    params.set("search", state.search.trim());
  }

  if (state.category !== "all") {
    params.set("category", state.category);
  }

  if (state.item) {
    params.set("item", state.item);
  }

  const value = params.toString();
  return value ? `?${value}` : "";
}

export function createRequestTracker() {
  let token = 0;

  return {
    next() {
      token += 1;
      return token;
    },
    isLatest(nextToken: number) {
      return nextToken === token;
    },
  };
}
