import { beforeEach, describe, expect, it } from "vitest";
import {
  STORAGE_KEY,
  createInitialBoardState,
  loadPersistedState,
  parseQuery,
  reconcileSelection,
  savePersistedState,
  serializeQuery,
} from "../src/state";

describe("query helpers", () => {
  it("parses known query values", () => {
    expect(parseQuery("?search=ops&status=blocked&sort=title-asc")).toEqual({
      search: "ops",
      status: "blocked",
      sort: "title-asc",
    });
  });

  it("serializes only meaningful values", () => {
    expect(
      serializeQuery({
        search: "ops",
        status: "open",
        sort: "priority-desc",
      }),
    ).toBe("?search=ops&status=open");
  });
});

describe("persistence", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("stores and restores board state", () => {
    const state = createInitialBoardState("", localStorage);
    savePersistedState(localStorage, state);

    expect(loadPersistedState(localStorage)?.query).toEqual(state.query);
    expect(loadPersistedState(localStorage)?.items).toHaveLength(state.items.length);
  });

  it("prefers URL query over persisted query and resets hidden selection", () => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        items: [
          {
            id: "task-1",
            title: "Only open task",
            workspace: "Ops",
            owner: "Jin",
            status: "open",
            priority: 4,
          },
        ],
        query: {
          search: "",
          status: "open",
          sort: "priority-desc",
        },
        selectedId: "task-1",
      }),
    );

    const state = createInitialBoardState("?status=done", localStorage);
    const reconciled = reconcileSelection(state);

    expect(reconciled.query.status).toBe("done");
    expect(reconciled.selection.selectedId).toBeNull();
  });
});
