import { DIRECTORY_ITEMS } from "./data";
import type { DirectoryItem, DirectoryQuery, ExplorerService } from "./types";

function wait(ms: number, signal: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    const timer = window.setTimeout(() => {
      signal.removeEventListener("abort", onAbort);
      resolve();
    }, ms);

    const onAbort = () => {
      window.clearTimeout(timer);
      reject(new DOMException("The operation was aborted.", "AbortError"));
    };

    signal.addEventListener("abort", onAbort, { once: true });
  });
}

function filterItems(items: DirectoryItem[], query: DirectoryQuery): DirectoryItem[] {
  const search = query.search.trim().toLowerCase();

  return items
    .filter((item) => {
      const categoryMatch = query.category === "all" || item.category === query.category;
      const searchMatch =
        search.length === 0 ||
        item.title.toLowerCase().includes(search) ||
        item.summary.toLowerCase().includes(search) ||
        item.owner.toLowerCase().includes(search);

      return categoryMatch && searchMatch;
    })
    .sort((left, right) => left.title.localeCompare(right.title));
}

export const explorerService: ExplorerService = {
  async listDirectory(query, signal) {
    await wait(140 + query.search.length * 25, signal);

    if (query.simulateFailure) {
      throw new Error("Simulated directory failure.");
    }

    return filterItems(DIRECTORY_ITEMS, query);
  },

  async getDirectoryItem(id, signal) {
    await wait(90, signal);

    const item = DIRECTORY_ITEMS.find((entry) => entry.id === id);
    if (!item) {
      throw new Error(`Directory item ${id} was not found.`);
    }

    return item;
  },
};
