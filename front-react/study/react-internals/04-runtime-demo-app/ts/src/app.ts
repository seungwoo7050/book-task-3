import {
  createElement,
  render,
  resetRuntime,
  useEffect,
  useState,
  type SetStateAction,
} from "@front-react/hooks-and-events";

import { DEMO_ITEMS, type DemoItem } from "./data";

const PAGE_SIZE = 4;
const DEBOUNCE_MS = 250;

interface DemoMetrics {
  renderCount: number;
  lastCommitMs: number;
  visibleCount: number;
  matchCount: number;
  activeQuery: string;
}

function useDebouncedValue<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      setDebounced(value);
    }, delayMs);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [value, delayMs]);

  return debounced;
}

function updateMetrics(
  setMetrics: (action: SetStateAction<DemoMetrics>) => void,
  startedAt: number,
  visibleCount: number,
  matchCount: number,
  activeQuery: string,
): void {
  const elapsed = Number((performance.now() - startedAt).toFixed(2));
  setMetrics((previous) => ({
    renderCount: previous.renderCount + 1,
    lastCommitMs: elapsed,
    visibleCount,
    matchCount,
    activeQuery,
  }));
}

function DemoApp() {
  const renderStartedAt = performance.now();
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebouncedValue(query, DEBOUNCE_MS);
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const [metrics, setMetrics] = useState<DemoMetrics>({
    renderCount: 0,
    lastCommitMs: 0,
    visibleCount: PAGE_SIZE,
    matchCount: DEMO_ITEMS.length,
    activeQuery: "all",
  });

  const normalizedQuery = debouncedQuery.trim().toLowerCase();
  const filteredItems = DEMO_ITEMS.filter((item) => {
    if (!normalizedQuery) {
      return true;
    }

    const haystack = `${item.title} ${item.category} ${item.excerpt}`.toLowerCase();
    return haystack.includes(normalizedQuery);
  });
  const visibleItems = filteredItems.slice(0, visibleCount);
  const hasMore = visibleItems.length < filteredItems.length;

  useEffect(() => {
    setVisibleCount(PAGE_SIZE);
  }, [normalizedQuery]);

  useEffect(() => {
    updateMetrics(
      setMetrics,
      renderStartedAt,
      visibleItems.length,
      filteredItems.length,
      normalizedQuery || "all",
    );
  }, [normalizedQuery, visibleItems.length, filteredItems.length]);

  return createElement(
    "main",
    { className: "demo-shell" },
    createElement(
      "header",
      { className: "demo-hero" },
      createElement("p", { className: "eyebrow" }, "Runtime Demo"),
      createElement("h1", null, "Shared runtime consumer app"),
      createElement(
        "p",
        { className: "hero-copy" },
        "Debounced search, paginated results, and render metrics on top of the hooks-and-events runtime.",
      ),
    ),
    createElement(
      "section",
      { className: "demo-controls" },
      createElement(
        "label",
        { className: "field", htmlFor: "runtime-search" },
        createElement("span", { className: "field-label" }, "Search demo items"),
        createElement("input", {
          id: "runtime-search",
          value: query,
          placeholder: "Try metrics, effects, or interaction",
          onInput: (event: { currentTarget: HTMLInputElement | null }) =>
            setQuery(event.currentTarget?.value ?? ""),
        }),
      ),
      createElement(
        "div",
        { className: "demo-status", "aria-live": "polite" },
        `Showing ${visibleItems.length} of ${filteredItems.length} matches`,
      ),
    ),
    createElement(
      "section",
      { className: "demo-grid" },
      createElement(
        "article",
        { className: "results-panel" },
        createElement("h2", null, "Results"),
        createElement(
          "ul",
          { className: "results-list" },
          ...visibleItems.map((item) =>
            createElement(
              "li",
              { className: "result-card", key: item.id },
              createElement("p", { className: "result-category" }, item.category),
              createElement("h3", null, item.title),
              createElement("p", { className: "result-excerpt" }, item.excerpt),
            ),
          ),
        ),
        filteredItems.length === 0
          ? createElement(
              "p",
              { className: "empty-state", role: "status" },
              "No demo items match the current query.",
            )
          : createElement(
              "button",
              {
                className: "load-more",
                disabled: !hasMore,
                onClick: () => setVisibleCount((count) => count + PAGE_SIZE),
              },
              hasMore ? "Load more results" : "All results loaded",
            ),
      ),
      createElement(
        "aside",
        { className: "metrics-panel" },
        createElement("h2", null, "Render metrics"),
        createElement(
          "dl",
          { className: "metrics-list" },
          createElement("dt", null, "Observed renders"),
          createElement("dd", { id: "metric-renders" }, String(metrics.renderCount)),
          createElement("dt", null, "Last commit window"),
          createElement("dd", { id: "metric-commit-ms" }, `${metrics.lastCommitMs} ms`),
          createElement("dt", null, "Visible items"),
          createElement("dd", { id: "metric-visible" }, String(metrics.visibleCount)),
          createElement("dt", null, "Active query"),
          createElement("dd", { id: "metric-query" }, metrics.activeQuery),
        ),
        createElement(
          "p",
          { className: "metrics-note" },
          "Metrics here are learning aids. They show when this runtime redraws more work, not production-grade profiling.",
        ),
      ),
    ),
  );
}

export function mountRuntimeDemo(container: HTMLElement): void {
  render(createElement(DemoApp, null), container);
}

export function resetRuntimeDemo(): void {
  resetRuntime();
}
