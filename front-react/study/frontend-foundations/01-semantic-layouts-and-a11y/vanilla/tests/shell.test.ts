import { beforeEach, describe, expect, it } from "vitest";
import { mountSettingsShell } from "../src/app";

describe("mountSettingsShell", () => {
  beforeEach(() => {
    document.body.innerHTML = '<div id="app"></div>';
  });

  it("renders semantic landmarks and labeled controls", () => {
    const container = document.querySelector<HTMLElement>("#app");
    mountSettingsShell(container!);

    expect(document.querySelector("header")).not.toBeNull();
    expect(document.querySelector("nav[aria-label='Settings sections']")).not.toBeNull();
    expect(document.querySelector("main")).not.toBeNull();
    expect(document.querySelector("aside")).not.toBeNull();
    expect(document.querySelector("label[for='workspaceName']")?.textContent).toContain(
      "Workspace name",
    );
    expect(document.querySelector("#workspaceName-help")?.textContent).toContain(
      "Shown in internal dashboards",
    );
  });

  it("marks invalid fields and focuses the first invalid input on submit", () => {
    const container = document.querySelector<HTMLElement>("#app");
    mountSettingsShell(container!);

    const workspaceName = document.querySelector<HTMLInputElement>("#workspaceName")!;
    const supportEmail = document.querySelector<HTMLInputElement>("#supportEmail")!;
    const form = document.querySelector<HTMLFormElement>("#settings-form")!;
    const status = document.querySelector<HTMLElement>("#save-status")!;

    workspaceName.value = "ab";
    supportEmail.value = "invalid";
    form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));

    expect(workspaceName.getAttribute("aria-invalid")).toBe("true");
    expect(supportEmail.getAttribute("aria-invalid")).toBe("true");
    expect(document.activeElement).toBe(workspaceName);
    expect(status.textContent).toContain("Fix 2 fields");
  });

  it("announces a save status for valid values", () => {
    const container = document.querySelector<HTMLElement>("#app");
    mountSettingsShell(container!);

    const workspaceName = document.querySelector<HTMLInputElement>("#workspaceName")!;
    const supportEmail = document.querySelector<HTMLInputElement>("#supportEmail")!;
    const form = document.querySelector<HTMLFormElement>("#settings-form")!;
    const status = document.querySelector<HTMLElement>("#save-status")!;

    workspaceName.value = "Ops Seoul";
    supportEmail.value = "ops-seoul@example.com";
    form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));

    expect(status.textContent).toContain("Settings saved for Ops Seoul");
    expect(workspaceName.hasAttribute("aria-invalid")).toBe(false);
  });
});
