import {
  applyQuery,
  createInitialBoardState,
  reconcileSelection,
  savePersistedState,
  serializeQuery,
  updateItemTitle,
} from "./state";
import type { BoardItem, BoardQuery, BoardState } from "./types";

function syncUrl(query: BoardQuery): void {
  const nextSearch = serializeQuery(query);
  const nextUrl = `${window.location.pathname}${nextSearch}`;
  window.history.replaceState({}, "", nextUrl);
}

function getSelectedItem(state: BoardState): BoardItem | undefined {
  return state.items.find((item) => item.id === state.selection.selectedId);
}

function getMarkup(state: BoardState): string {
  const visibleItems = applyQuery(state.items, state.query);
  const selectedItem = getSelectedItem(state);

  return `
    <div class="board-shell">
      <header class="board-header">
        <div>
          <p class="eyebrow">Foundations 02</p>
          <h1>DOM state and event delegation board</h1>
          <p class="lede">Search, filter, sort, select, and edit a small task board while syncing URL and local persistence.</p>
        </div>
        <p class="status-badge">${visibleItems.length} visible item${visibleItems.length === 1 ? "" : "s"}</p>
      </header>

      <main class="board-layout">
        <section class="board-panel" aria-labelledby="controls-heading">
          <div class="panel-header">
            <h2 id="controls-heading">Queue controls</h2>
            <p>Query state is encoded in the URL. Item edits and selection persist locally.</p>
          </div>

          <form class="controls" aria-label="Board controls">
            <label>
              Search
              <input id="searchInput" name="search" type="search" value="${state.query.search}" placeholder="Search title, workspace, or owner" />
            </label>

            <label>
              Status
              <select id="statusFilter" name="status">
                <option value="all" ${state.query.status === "all" ? "selected" : ""}>All statuses</option>
                <option value="open" ${state.query.status === "open" ? "selected" : ""}>Open</option>
                <option value="blocked" ${state.query.status === "blocked" ? "selected" : ""}>Blocked</option>
                <option value="done" ${state.query.status === "done" ? "selected" : ""}>Done</option>
              </select>
            </label>

            <label>
              Sort
              <select id="sortFilter" name="sort">
                <option value="priority-desc" ${state.query.sort === "priority-desc" ? "selected" : ""}>Priority high to low</option>
                <option value="priority-asc" ${state.query.sort === "priority-asc" ? "selected" : ""}>Priority low to high</option>
                <option value="title-asc" ${state.query.sort === "title-asc" ? "selected" : ""}>Title A-Z</option>
              </select>
            </label>
          </form>

          <table class="board-table">
            <thead>
              <tr>
                <th scope="col">Task</th>
                <th scope="col">Workspace</th>
                <th scope="col">Owner</th>
                <th scope="col">Status</th>
                <th scope="col">Priority</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody id="boardRows">
              ${
                visibleItems.length === 0
                  ? `<tr><td colspan="6" class="empty-row">No tasks match the current query.</td></tr>`
                  : visibleItems
                      .map((item) => {
                        const isSelected = item.id === state.selection.selectedId;
                        const isEditing = item.id === state.selection.editingId;

                        return `
                          <tr data-row-id="${item.id}" class="${isSelected ? "is-selected" : ""}">
                            <td>
                              ${
                                isEditing
                                  ? `<label class="sr-only" for="edit-${item.id}">Edit title for ${item.title}</label>
                                     <input id="edit-${item.id}" class="edit-input" name="draftTitle" data-edit-id="${item.id}" value="${item.title}" />`
                                  : `<strong>${item.title}</strong>`
                              }
                            </td>
                            <td>${item.workspace}</td>
                            <td>${item.owner}</td>
                            <td><span class="status-chip status-${item.status}">${item.status}</span></td>
                            <td>${item.priority}</td>
                            <td class="action-cell">
                              <button type="button" data-action="select" data-id="${item.id}" aria-pressed="${isSelected}">
                                ${isSelected ? "Selected" : "Select"}
                              </button>
                              ${
                                isEditing
                                  ? `<button type="button" data-action="save" data-id="${item.id}">Save</button>
                                     <button type="button" data-action="cancel" data-id="${item.id}">Cancel</button>`
                                  : `<button type="button" data-action="edit" data-id="${item.id}">Edit</button>`
                              }
                            </td>
                          </tr>
                        `;
                      })
                      .join("")
              }
            </tbody>
          </table>
        </section>

        <aside class="board-panel detail-panel" aria-labelledby="detail-heading">
          <div class="panel-header">
            <h2 id="detail-heading">Selection detail</h2>
            <p id="board-status" role="status" aria-live="polite">${state.notice}</p>
          </div>

          ${
            selectedItem
              ? `<dl class="detail-grid">
                  <div><dt>Task</dt><dd>${selectedItem.title}</dd></div>
                  <div><dt>Workspace</dt><dd>${selectedItem.workspace}</dd></div>
                  <div><dt>Owner</dt><dd>${selectedItem.owner}</dd></div>
                  <div><dt>Status</dt><dd>${selectedItem.status}</dd></div>
                  <div><dt>Priority</dt><dd>${selectedItem.priority}</dd></div>
                </dl>`
              : `<p class="empty-detail">Select a row to inspect its detail.</p>`
          }
        </aside>
      </main>
    </div>
  `;
}

export function mountBoard(container: HTMLElement, storage: Storage = window.localStorage): void {
  let state = createInitialBoardState(window.location.search, storage);

  const render = (focusSelector?: string) => {
    state = reconcileSelection(state);
    container.innerHTML = getMarkup(state);
    syncUrl(state.query);
    savePersistedState(storage, state);

    const input = container.querySelector<HTMLInputElement>(
      `[data-edit-id="${state.selection.editingId ?? ""}"]`,
    );
    if (input) {
      input.focus();
      input.select();
      return;
    }

    if (focusSelector) {
      const focusTarget = container.querySelector<HTMLElement>(focusSelector);
      focusTarget?.focus();
    }
  };

  const setQuery = (
    patch: Partial<BoardQuery>,
    notice: string,
    focusSelector?: string,
  ) => {
    state = {
      ...state,
      query: {
        ...state.query,
        ...patch,
      },
      notice,
    };
    render(focusSelector);
  };

  const setSelection = (selectedId: string, notice: string) => {
    state = {
      ...state,
      selection: {
        ...state.selection,
        selectedId,
      },
      notice,
    };
    render(`[data-action="select"][data-id="${selectedId}"]`);
  };

  const setEditing = (editingId: string | null, notice: string) => {
    state = {
      ...state,
      selection: {
        ...state.selection,
        editingId,
        selectedId: editingId ?? state.selection.selectedId,
      },
      notice,
    };
    render(editingId ? undefined : `[data-action="select"][data-id="${state.selection.selectedId ?? ""}"]`);
  };

  container.addEventListener("input", (event) => {
    const target = event.target as HTMLInputElement | null;
    if (!target) {
      return;
    }

    if (target.name === "search") {
      setQuery(
        { search: target.value },
        "Search query synced to URL and storage.",
        "#searchInput",
      );
    }
  });

  container.addEventListener("change", (event) => {
    const target = event.target as HTMLInputElement | HTMLSelectElement | null;
    if (!target) {
      return;
    }

    if (target.name === "status") {
      setQuery(
        { status: target.value as BoardQuery["status"] },
        "Status filter updated.",
        "#statusFilter",
      );
    }

    if (target.name === "sort") {
      setQuery(
        { sort: target.value as BoardQuery["sort"] },
        "Sort order updated.",
        "#sortFilter",
      );
    }
  });

  container.addEventListener("click", (event) => {
    const target = (event.target as HTMLElement | null)?.closest<HTMLButtonElement>("[data-action]");

    if (!target) {
      return;
    }

    const action = target.dataset.action;
    const itemId = target.dataset.id;

    if (!itemId) {
      return;
    }

    if (action === "select") {
      setSelection(itemId, `Selected ${itemId}.`);
      return;
    }

    if (action === "edit") {
      setEditing(itemId, `Editing ${itemId}.`);
      return;
    }

    if (action === "cancel") {
      setEditing(null, `Edit cancelled for ${itemId}.`);
      return;
    }

    if (action === "save") {
      const input = container.querySelector<HTMLInputElement>(`[data-edit-id="${itemId}"]`);
      const nextTitle = input?.value.trim();

      if (!nextTitle) {
        state = {
          ...state,
          notice: `Enter a title before saving ${itemId}.`,
        };
        render(`[data-edit-id="${itemId}"]`);
        return;
      }

      state = {
        ...state,
        items: updateItemTitle(state.items, itemId, nextTitle),
        selection: {
          selectedId: itemId,
          editingId: null,
        },
        notice: `Saved title update for ${itemId}.`,
      };
      render();
    }
  });

  container.addEventListener("keydown", (event) => {
    const target = event.target as HTMLElement | null;

    if (
      event.key === "Enter" &&
      target instanceof HTMLInputElement &&
      target.matches("[data-edit-id]")
    ) {
      event.preventDefault();
      const itemId = target.dataset.editId;
      if (!itemId) {
        return;
      }

      const nextTitle = target.value.trim();
      if (!nextTitle) {
        state = {
          ...state,
          notice: `Enter a title before saving ${itemId}.`,
        };
        render(`[data-edit-id="${itemId}"]`);
        return;
      }

      state = {
        ...state,
        items: updateItemTitle(state.items, itemId, nextTitle),
        selection: {
          selectedId: itemId,
          editingId: null,
        },
        notice: `Saved title update for ${itemId}.`,
      };
      render();
    }
  });

  render();
}
