import { beforeEach, describe, expect, it, vi } from "vitest";
import { mountDirectoryExplorer } from "../src/app";
import type { ExplorerService } from "../src/types";

function createMockService(): ExplorerService {
  return {
    async listDirectory(query) {
      if (query.simulateFailure) {
        throw new Error("Simulated directory failure.");
      }

      return [
        {
          id: "doc-1",
          title: "Incident response runbook",
          category: "runbook",
          owner: "Ops",
          summary: "Respond to incidents.",
          body: "Runbook body",
        },
      ].filter((item) =>
        item.title.toLowerCase().includes(query.search.toLowerCase()),
      );
    },

    async getDirectoryItem(id) {
      return {
        id,
        title: "Incident response runbook",
        category: "runbook",
        owner: "Ops",
        summary: "Respond to incidents.",
        body: "Runbook body",
      };
    },
  };
}

describe("mountDirectoryExplorer", () => {
  beforeEach(() => {
    vi.useRealTimers();
    window.history.replaceState({}, "", "/");
    document.body.innerHTML = '<div id="app"></div>';
  });

  it("syncs search to the URL and loads detail", async () => {
    const container = document.querySelector<HTMLElement>("#app")!;
    mountDirectoryExplorer(container, createMockService());

    await Promise.resolve();
    await Promise.resolve();

    const search = document.querySelector<HTMLInputElement>("#searchInput")!;
    search.value = "Incident";
    search.dispatchEvent(new Event("input", { bubbles: true }));

    await Promise.resolve();
    await Promise.resolve();

    expect(window.location.search).toContain("search=Incident");
    expect(document.querySelector(".detail-article")?.textContent).toContain(
      "Incident response runbook",
    );
  });

  it("shows retry UI after a simulated failure and recovers on retry", async () => {
    const container = document.querySelector<HTMLElement>("#app")!;
    mountDirectoryExplorer(container, createMockService());

    await Promise.resolve();
    await Promise.resolve();

    document
      .querySelector<HTMLElement>('[data-action="simulate-failure"]')!
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));
    document
      .querySelector<HTMLInputElement>("#searchInput")!
      .dispatchEvent(new Event("input", { bubbles: true }));

    await Promise.resolve();
    await Promise.resolve();

    expect(document.querySelector("#list-status")?.textContent).toContain(
      "Simulated directory failure.",
    );

    document
      .querySelector<HTMLElement>('[data-action="retry-list"]')!
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));

    await Promise.resolve();
    await Promise.resolve();

    expect(document.querySelector(".result-list")?.textContent).toContain(
      "Incident response runbook",
    );
  });
});
