import { expect, test } from "@playwright/test";

test("updates query params and loads detail from the directory list", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Search").fill("policy");
  await page.getByRole("button", { name: /Escalation policy handbook/i }).click();

  await expect(page).toHaveURL(/search=policy/);
  await expect(page).toHaveURL(/item=doc-102/);
  await expect(page.getByText("Viewing Escalation policy handbook.")).toBeVisible();
});

test("recovers from a simulated failure and keeps keyboard navigation viable", async ({
  page,
}) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Simulate next request failure" }).click();
  await page.getByLabel("Category").selectOption("runbook");

  await expect(page.getByText("Simulated directory failure.").first()).toBeVisible();
  await page.getByRole("button", { name: "Retry directory request" }).click();

  await expect(page.getByRole("button", { name: /Incident response runbook/i })).toBeVisible();

  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Enter");

  await expect(page.getByText("Viewing Incident response runbook.")).toBeVisible();
});
