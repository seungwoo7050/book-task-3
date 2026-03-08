import { createRequestTracker, DEFAULT_QUERY, parseUrlState, serializeUrlState } from "./state";
import { explorerService } from "./service";
import type {
  AsyncState,
  DirectoryItem,
  DirectoryQuery,
  ExplorerService,
  ExplorerUrlState,
} from "./types";

interface ExplorerState {
  query: DirectoryQuery;
  selectedId: string | null;
  listState: AsyncState;
  detailState: AsyncState;
  items: DirectoryItem[];
  currentItem: DirectoryItem | null;
  errorMessage: string | null;
  detailErrorMessage: string | null;
  simulateFailureNext: boolean;
}

function buildUrlState(state: ExplorerState): ExplorerUrlState {
  return {
    ...state.query,
    item: state.selectedId,
  };
}

function syncUrl(state: ExplorerState) {
  const next = serializeUrlState(buildUrlState(state));
  window.history.replaceState({}, "", `${window.location.pathname}${next}`);
}

function getMarkup(state: ExplorerState): string {
  return `
    <div class="explorer-shell">
      <header class="explorer-header">
        <div>
          <p class="eyebrow">Foundations 03</p>
          <h1>Networked UI patterns explorer</h1>
          <p class="lede">A mock directory that shows loading, empty, error, retry, abort, and query-param navigation without a real backend.</p>
        </div>
        <button type="button" data-action="simulate-failure">
          ${state.simulateFailureNext ? "Failure armed for next request" : "Simulate next request failure"}
        </button>
      </header>

      <main class="explorer-layout">
        <section class="panel" aria-labelledby="directory-heading">
          <div class="panel-header">
            <h2 id="directory-heading">Directory</h2>
            <p id="list-status" role="status" aria-live="polite">
              ${
                state.listState === "loading"
                  ? "Loading directory results."
                  : state.listState === "error"
                    ? state.errorMessage
                    : state.listState === "empty"
                      ? "No directory entries match the current query."
                      : `${state.items.length} result${state.items.length === 1 ? "" : "s"} ready.`
              }
            </p>
          </div>

          <form class="controls" aria-label="Explorer controls">
            <label>
              Search
              <input id="searchInput" name="search" type="search" value="${state.query.search}" placeholder="Search title, summary, or owner" />
            </label>

            <label>
              Category
              <select id="categoryFilter" name="category">
                <option value="all" ${state.query.category === "all" ? "selected" : ""}>All categories</option>
                <option value="runbook" ${state.query.category === "runbook" ? "selected" : ""}>Runbooks</option>
                <option value="policy" ${state.query.category === "policy" ? "selected" : ""}>Policies</option>
                <option value="guide" ${state.query.category === "guide" ? "selected" : ""}>Guides</option>
              </select>
            </label>
          </form>

          ${
            state.listState === "loading"
              ? `<div class="list-state" data-testid="list-loading">Loading directory…</div>`
              : state.listState === "error"
                ? `<div class="list-state error-state">
                    <p>${state.errorMessage}</p>
                    <button type="button" data-action="retry-list">Retry directory request</button>
                  </div>`
                : state.listState === "empty"
                  ? `<div class="list-state">No matching results. Try a different search or category.</div>`
                  : `<ul class="result-list">
                      ${state.items
                        .map(
                          (item) => `
                            <li>
                              <button
                                type="button"
                                class="result-button ${item.id === state.selectedId ? "is-active" : ""}"
                                data-action="open-item"
                                data-id="${item.id}"
                              >
                                <span class="result-title">${item.title}</span>
                                <span class="result-meta">${item.category} · ${item.owner}</span>
                                <span class="result-summary">${item.summary}</span>
                              </button>
                            </li>
                          `,
                        )
                        .join("")}
                    </ul>`
          }
        </section>

        <aside class="panel detail-panel" aria-labelledby="detail-heading">
          <div class="panel-header">
            <h2 id="detail-heading">Detail</h2>
            <p id="detail-status" role="status" aria-live="polite">
              ${
                state.detailState === "loading"
                  ? "Loading document detail."
                  : state.detailState === "error"
                    ? state.detailErrorMessage
                    : state.currentItem
                      ? `Viewing ${state.currentItem.title}.`
                      : "Select an item to inspect its detail."
              }
            </p>
          </div>

          ${
            state.detailState === "loading"
              ? `<div class="detail-state" data-testid="detail-loading">Loading detail…</div>`
              : state.detailState === "error"
                ? `<div class="detail-state error-state">
                    <p>${state.detailErrorMessage}</p>
                    <button type="button" data-action="retry-detail">Retry detail request</button>
                  </div>`
                : state.currentItem
                  ? `<article class="detail-article">
                      <p class="detail-eyebrow">${state.currentItem.category} · ${state.currentItem.owner}</p>
                      <h3>${state.currentItem.title}</h3>
                      <p>${state.currentItem.summary}</p>
                      <div class="detail-body">${state.currentItem.body}</div>
                    </article>`
                  : `<p class="detail-state">Select an item to inspect its detail.</p>`
          }
        </aside>
      </main>
    </div>
  `;
}

export function mountDirectoryExplorer(
  container: HTMLElement,
  service: ExplorerService = explorerService,
): void {
  const parsed = parseUrlState(window.location.search);
  const listTracker = createRequestTracker();
  const detailTracker = createRequestTracker();
  let listController: AbortController | null = null;
  let detailController: AbortController | null = null;

  let state: ExplorerState = {
    query: {
      ...DEFAULT_QUERY,
      ...parsed,
    },
    selectedId: parsed.item ?? null,
    listState: "idle",
    detailState: "idle",
    items: [],
    currentItem: null,
    errorMessage: null,
    detailErrorMessage: null,
    simulateFailureNext: false,
  };

  const render = (focusSelector?: string) => {
    container.innerHTML = getMarkup(state);
    syncUrl(state);

    if (focusSelector) {
      container.querySelector<HTMLElement>(focusSelector)?.focus();
    }
  };

  const loadDetail = async (itemId: string, focusSelector?: string) => {
    detailController?.abort();
    detailController = new AbortController();
    const token = detailTracker.next();

    state = {
      ...state,
      selectedId: itemId,
      detailState: "loading",
      detailErrorMessage: null,
    };
    render(focusSelector);

    try {
      const item = await service.getDirectoryItem(itemId, detailController.signal);
      if (!detailTracker.isLatest(token)) {
        return;
      }

      state = {
        ...state,
        currentItem: item,
        detailState: "success",
      };
      render(focusSelector);
    } catch (error) {
      if ((error as Error).name === "AbortError" || !detailTracker.isLatest(token)) {
        return;
      }

      state = {
        ...state,
        detailState: "error",
        detailErrorMessage:
          error instanceof Error ? error.message : "Detail request failed.",
      };
      render(focusSelector);
    }
  };

  const loadList = async (focusSelector?: string) => {
    listController?.abort();
    listController = new AbortController();
    const token = listTracker.next();
    const shouldFail = state.simulateFailureNext;

    state = {
      ...state,
      listState: "loading",
      errorMessage: null,
      simulateFailureNext: false,
    };
    render(focusSelector);

    try {
      const items = await service.listDirectory(
        {
          ...state.query,
          simulateFailure: shouldFail,
        },
        listController.signal,
      );

      if (!listTracker.isLatest(token)) {
        return;
      }

      const selectedId = items.some((item) => item.id === state.selectedId)
        ? state.selectedId
        : items[0]?.id ?? null;

      state = {
        ...state,
        items,
        selectedId,
        listState: items.length === 0 ? "empty" : "success",
        currentItem: selectedId && state.currentItem?.id === selectedId ? state.currentItem : null,
      };
      render(focusSelector);

      if (selectedId) {
        await loadDetail(selectedId, focusSelector);
      } else {
        state = {
          ...state,
          currentItem: null,
          detailState: "empty",
          detailErrorMessage: null,
        };
        render(focusSelector);
      }
    } catch (error) {
      if ((error as Error).name === "AbortError" || !listTracker.isLatest(token)) {
        return;
      }

      state = {
        ...state,
        listState: "error",
        errorMessage:
          error instanceof Error ? error.message : "Directory request failed.",
        items: [],
        currentItem: null,
        detailState: "empty",
        detailErrorMessage: null,
      };
      render(focusSelector);
    }
  };

  container.addEventListener("input", (event) => {
    const target = event.target as HTMLInputElement | null;
    if (!target) {
      return;
    }

    if (target.name === "search") {
      state = {
        ...state,
        query: {
          ...state.query,
          search: target.value,
        },
      };
      void loadList("#searchInput");
    }
  });

  container.addEventListener("change", (event) => {
    const target = event.target as HTMLSelectElement | null;
    if (!target) {
      return;
    }

    if (target.name === "category") {
      state = {
        ...state,
        query: {
          ...state.query,
          category: target.value as DirectoryQuery["category"],
        },
      };
      void loadList("#categoryFilter");
    }
  });

  container.addEventListener("click", (event) => {
    const target = (event.target as HTMLElement | null)?.closest<HTMLElement>("[data-action]");
    if (!target) {
      return;
    }

    const action = target.dataset.action;
    const itemId = target.dataset.id;

    if (action === "simulate-failure") {
      state = {
        ...state,
        simulateFailureNext: !state.simulateFailureNext,
      };
      render('[data-action="simulate-failure"]');
      return;
    }

    if (action === "retry-list") {
      void loadList('[data-action="retry-list"]');
      return;
    }

    if (action === "retry-detail" && state.selectedId) {
      void loadDetail(state.selectedId, '[data-action="retry-detail"]');
      return;
    }

    if (action === "open-item" && itemId) {
      void loadDetail(itemId, `[data-id="${itemId}"]`);
    }
  });

  void loadList("#searchInput");
}
