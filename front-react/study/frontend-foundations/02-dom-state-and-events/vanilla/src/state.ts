import { DEFAULT_ITEMS } from "./data";
import type {
  BoardItem,
  BoardQuery,
  BoardSort,
  BoardState,
  PersistedBoardState,
} from "./types";

export const STORAGE_KEY = "front-react:foundations:board";

export const DEFAULT_QUERY: BoardQuery = {
  search: "",
  status: "all",
  sort: "priority-desc",
};

function cloneItems(items: BoardItem[]): BoardItem[] {
  return items.map((item) => ({ ...item }));
}

export function parseQuery(search: string): Partial<BoardQuery> {
  const params = new URLSearchParams(search);
  const parsed: Partial<BoardQuery> = {};
  const status = params.get("status");
  const sort = params.get("sort");
  const query = params.get("search");

  if (query) {
    parsed.search = query;
  }

  if (status === "all" || status === "open" || status === "blocked" || status === "done") {
    parsed.status = status;
  }

  if (sort === "priority-desc" || sort === "priority-asc" || sort === "title-asc") {
    parsed.sort = sort as BoardSort;
  }

  return parsed;
}

export function serializeQuery(query: BoardQuery): string {
  const params = new URLSearchParams();

  if (query.search.trim()) {
    params.set("search", query.search.trim());
  }

  if (query.status !== "all") {
    params.set("status", query.status);
  }

  if (query.sort !== DEFAULT_QUERY.sort) {
    params.set("sort", query.sort);
  }

  const value = params.toString();
  return value ? `?${value}` : "";
}

export function loadPersistedState(storage: Storage): PersistedBoardState | null {
  const raw = storage.getItem(STORAGE_KEY);

  if (!raw) {
    return null;
  }

  try {
    const parsed = JSON.parse(raw) as PersistedBoardState;
    if (!Array.isArray(parsed.items)) {
      return null;
    }

    return parsed;
  } catch {
    return null;
  }
}

export function savePersistedState(storage: Storage, state: BoardState): void {
  const payload: PersistedBoardState = {
    items: cloneItems(state.items),
    query: { ...state.query },
    selectedId: state.selection.selectedId,
  };

  storage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

export function applyQuery(items: BoardItem[], query: BoardQuery): BoardItem[] {
  const search = query.search.trim().toLowerCase();

  const filtered = items.filter((item) => {
    const searchMatch =
      search.length === 0 ||
      item.title.toLowerCase().includes(search) ||
      item.workspace.toLowerCase().includes(search) ||
      item.owner.toLowerCase().includes(search);

    const statusMatch = query.status === "all" || item.status === query.status;

    return searchMatch && statusMatch;
  });

  return filtered.sort((left, right) => {
    if (query.sort === "priority-desc") {
      return right.priority - left.priority;
    }

    if (query.sort === "priority-asc") {
      return left.priority - right.priority;
    }

    return left.title.localeCompare(right.title);
  });
}

export function reconcileSelection(state: BoardState): BoardState {
  const visibleItems = applyQuery(state.items, state.query);
  const hasSelectedItem =
    state.selection.selectedId !== null &&
    visibleItems.some((item) => item.id === state.selection.selectedId);

  const hasEditingItem =
    state.selection.editingId !== null &&
    visibleItems.some((item) => item.id === state.selection.editingId);

  return {
    ...state,
    selection: {
      selectedId: hasSelectedItem ? state.selection.selectedId : visibleItems[0]?.id ?? null,
      editingId: hasEditingItem ? state.selection.editingId : null,
    },
  };
}

export function createInitialBoardState(
  locationSearch: string,
  storage: Storage,
): BoardState {
  const persisted = loadPersistedState(storage);
  const query = {
    ...DEFAULT_QUERY,
    ...(persisted?.query ?? {}),
    ...parseQuery(locationSearch),
  };

  const items = cloneItems(persisted?.items ?? DEFAULT_ITEMS);
  const selectedId = persisted?.selectedId ?? items[0]?.id ?? null;

  return reconcileSelection({
    items,
    query,
    selection: {
      selectedId,
      editingId: null,
    },
    notice: "State synced from URL and local storage.",
  });
}

export function updateItemTitle(items: BoardItem[], itemId: string, title: string): BoardItem[] {
  return items.map((item) =>
    item.id === itemId
      ? {
          ...item,
          title: title.trim(),
        }
      : item,
  );
}
