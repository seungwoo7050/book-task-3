import { expect, test } from "@playwright/test";

test("syncs filters to URL and persists edits across reload", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Search").fill("Ops");
  await page.getByLabel("Status").selectOption("open");

  await expect(page).toHaveURL(/search=Ops/);
  await expect(page).toHaveURL(/status=open/);

  await page.getByRole("button", { name: "Select" }).first().click();
  await page.getByRole("button", { name: "Edit" }).first().click();
  await page.locator('[data-edit-id="task-101"]').fill("Reconcile queue ownership map");
  await page.getByRole("button", { name: "Save" }).click();

  await expect(page.getByText("Saved title update for task-101.")).toBeVisible();

  await page.reload();
  await expect(page.getByLabel("Search")).toHaveValue("Ops");
  await expect(page.getByText("Reconcile queue ownership map").first()).toBeVisible();
});

test("supports keyboard selection and inline edit submission", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Search").fill("Refresh");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Enter");

  await expect(page.getByText("Selected task-102.")).toBeVisible();

  await page.keyboard.press("Tab");
  await page.keyboard.press("Enter");
  await expect(page.locator('[data-edit-id="task-102"]')).toBeFocused();

  await page.keyboard.press("ControlOrMeta+A");
  await page.keyboard.type("Refresh blocked escalation playbook");
  await page.keyboard.press("Enter");

  await expect(page.getByText("Saved title update for task-102.")).toBeVisible();
  await expect(page.getByText("Refresh blocked escalation playbook").first()).toBeVisible();
});
