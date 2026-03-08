import { beforeEach, describe, expect, it } from "vitest";
import { mountBoard } from "../src/app";

describe("mountBoard", () => {
  beforeEach(() => {
    localStorage.clear();
    window.history.replaceState({}, "", "/");
    document.body.innerHTML = '<div id="app"></div>';
  });

  it("syncs search and filters to the URL", () => {
    const container = document.querySelector<HTMLElement>("#app")!;
    mountBoard(container, localStorage);

    const search = document.querySelector<HTMLInputElement>("#searchInput")!;

    search.value = "Ops";
    search.dispatchEvent(new Event("input", { bubbles: true }));
    const status = document.querySelector<HTMLSelectElement>("#statusFilter")!;
    status.value = "open";
    status.dispatchEvent(new Event("change", { bubbles: true }));

    expect(window.location.search).toContain("search=Ops");
    expect(window.location.search).toContain("status=open");
  });

  it("uses delegated click actions for selection and editing", () => {
    const container = document.querySelector<HTMLElement>("#app")!;
    mountBoard(container, localStorage);

    const selectButton = document.querySelector<HTMLButtonElement>(
      'button[data-action="select"][data-id="task-102"]',
    )!;
    selectButton.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(document.querySelector(".detail-grid")?.textContent).toContain(
      "Refresh escalation macros",
    );

    const editButton = document.querySelector<HTMLButtonElement>(
      'button[data-action="edit"][data-id="task-102"]',
    )!;
    editButton.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    const input = document.querySelector<HTMLInputElement>('[data-edit-id="task-102"]')!;
    input.value = "Refresh escalation templates";

    const saveButton = document.querySelector<HTMLButtonElement>(
      'button[data-action="save"][data-id="task-102"]',
    )!;
    saveButton.dispatchEvent(new MouseEvent("click", { bubbles: true }));

    expect(document.querySelector(".detail-grid")?.textContent).toContain(
      "Refresh escalation templates",
    );
    expect(localStorage.getItem("front-react:foundations:board")).toContain(
      "Refresh escalation templates",
    );
  });
});
