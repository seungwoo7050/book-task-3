export interface DemoItem {
  id: string;
  title: string;
  category: string;
  excerpt: string;
}

export const DEMO_ITEMS: DemoItem[] = [
  {
    id: "render-inspector",
    title: "Render Inspector",
    category: "metrics",
    excerpt: "Track which interactions force the runtime to redraw a larger slice of the tree.",
  },
  {
    id: "keyboard-path",
    title: "Keyboard Path",
    category: "interaction",
    excerpt: "Keep the result list navigable while delegated events stay on the root container.",
  },
  {
    id: "debounce-loop",
    title: "Debounce Loop",
    category: "search",
    excerpt: "Show how effect cleanup prevents stale timers from committing older queries.",
  },
  {
    id: "load-window",
    title: "Load Window",
    category: "pagination",
    excerpt: "Expose a small paginated window instead of rendering the whole list at once.",
  },
  {
    id: "effect-queue",
    title: "Effect Queue",
    category: "effects",
    excerpt: "Observe setup and cleanup ordering after commit rather than during render.",
  },
  {
    id: "shared-runtime",
    title: "Shared Runtime",
    category: "integration",
    excerpt: "Consume hooks and event logic from the shared package instead of copying code.",
  },
  {
    id: "list-pruning",
    title: "List Pruning",
    category: "search",
    excerpt: "Search narrows the DOM tree before the user asks for another page of results.",
  },
  {
    id: "commit-gap",
    title: "Commit Gap",
    category: "metrics",
    excerpt: "Make it explicit that render calculations happen before commit touches the DOM.",
  },
  {
    id: "event-bubble",
    title: "Event Bubble",
    category: "interaction",
    excerpt: "Keep bubbling visible while the runtime dispatches handlers from a root listener.",
  },
  {
    id: "runtime-limit",
    title: "Runtime Limit",
    category: "limitations",
    excerpt: "Document what this learning runtime does not support and where product code should move on.",
  },
];
