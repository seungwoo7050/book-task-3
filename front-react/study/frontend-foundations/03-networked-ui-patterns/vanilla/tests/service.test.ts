import { beforeEach, describe, expect, it, vi } from "vitest";
import { createRequestTracker } from "../src/state";
import { explorerService } from "../src/service";

describe("explorerService", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  it("rejects with AbortError when list requests are aborted", async () => {
    const controller = new AbortController();
    const promise = explorerService.listDirectory(
      { search: "", category: "all" },
      controller.signal,
    );
    const rejection = expect(promise).rejects.toMatchObject({ name: "AbortError" });

    controller.abort();
    await vi.runAllTimersAsync();
    await rejection;
  });

  it("tracks only the latest token for race-aware updates", () => {
    const tracker = createRequestTracker();
    const first = tracker.next();
    const second = tracker.next();

    expect(tracker.isLatest(first)).toBe(false);
    expect(tracker.isLatest(second)).toBe(true);
  });
});
