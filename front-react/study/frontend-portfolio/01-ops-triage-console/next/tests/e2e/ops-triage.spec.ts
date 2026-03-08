import { expect, test, type Locator, type Page } from "@playwright/test";

async function rowForIssue(page: Page, issueId: string): Promise<Locator> {
  return page.locator("tr", { has: page.getByText(issueId) }).first();
}

async function tabTo(page: Page, locator: Locator, maxTabs = 40) {
  for (let index = 0; index < maxTabs; index += 1) {
    await page.keyboard.press("Tab");
    const isFocused = await locator.evaluate(
      (element) => element === document.activeElement,
    );

    if (isFocused) {
      return;
    }
  }

  throw new Error("Unable to focus target element via keyboard navigation.");
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Ops Triage Console" }),
  ).toBeVisible();
});

test("updates an issue from detail and can undo the change", async ({ page }) => {
  await page
    .getByRole("button", { name: /Checkout retries spike after wallet fallback/ })
    .click();
  await expect(
    page.getByRole("heading", { name: "OPS-101 issue detail" }),
  ).toBeVisible();

  await page.getByRole("combobox", { name: "Issue status" }).click();
  await page.getByRole("option", { name: "Resolved" }).click();
  await page.getByTestId("apply-triage").click();

  await expect(page.getByText("Issue updated")).toBeVisible();
  await page.getByRole("button", { name: "Close dialog" }).click();
  await page.getByRole("button", { name: "Undo" }).click();

  const row = await rowForIssue(page, "OPS-101");
  await expect(row.getByText("Investigating")).toBeVisible();
});

test("applies a saved-view bulk update and clears the queue", async ({ page }) => {
  await page.getByRole("button", { name: "Untriaged" }).click();
  await page.getByRole("checkbox", { name: "Select all rows" }).click();
  await page.getByRole("combobox", { name: "Bulk status" }).click();
  await page.getByRole("option", { name: "Resolved" }).click();
  await page.getByTestId("apply-bulk-action").click();

  await expect(page.getByText("Bulk update applied")).toBeVisible();
  await expect(page.getByText("No matching issues")).toBeVisible();
});

test("surfaces a simulated write error and retries successfully", async ({ page }) => {
  await page
    .getByRole("button", { name: /Checkout retries spike after wallet fallback/ })
    .click();
  await page.evaluate(() => {
    window.localStorage.setItem(
      "ops-triage-console:runtime",
      JSON.stringify({
        latencyMs: 220,
        failureRate: 0,
        failNextRequest: true,
        mode: "stable",
      }),
    );
  });
  await page.getByRole("combobox", { name: "Issue status" }).click();
  await page.getByRole("option", { name: "Resolved" }).click();
  await page.getByTestId("apply-triage").click();

  await expect(page.getByText("Update failed")).toBeVisible();
  await page.getByRole("button", { name: "Close dialog" }).click();
  await page.getByRole("button", { name: "Retry" }).click();
  await expect(page.getByText("Issue updated")).toBeVisible();
});

test("supports a keyboard-only triage path", async ({ page }) => {
  const searchInput = page.getByTestId("issue-search");
  await tabTo(page, searchInput);
  await page.keyboard.type("search results disappear");

  const titleButton = page.getByRole("button", {
    name: /Search results disappear after filter reset/,
  });
  await tabTo(page, titleButton);
  await page.keyboard.press("Enter");

  const noteField = page.getByLabel("Operator note");
  await expect(noteField).toBeVisible();
  await tabTo(page, noteField);
  await page.keyboard.type("Keyboard handoff note.");

  const applyButton = page.getByTestId("apply-triage");
  await expect(applyButton).toBeVisible();
  await tabTo(page, applyButton);
  await page.keyboard.press("Enter");

  await expect(page.getByText("Issue updated")).toBeVisible();
});
