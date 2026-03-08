import { expect, test } from "@playwright/test";

test("exposes landmarks, labels, and responsive grid behavior", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("banner")).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Settings sections" })).toBeVisible();
  await expect(page.getByRole("main")).toBeVisible();
  await expect(page.getByRole("complementary")).toBeVisible();
  await expect(page.getByLabel("Workspace name")).toBeVisible();
  await expect(page.getByText("Shown in internal dashboards and review queues.")).toBeVisible();

  const grid = page.getByTestId("workspace-grid");
  await expect(grid).toBeVisible();

  await page.setViewportSize({ width: 1280, height: 900 });
  const desktopColumns = await grid.evaluate((element) => {
    return window.getComputedStyle(element).gridTemplateColumns;
  });
  expect(desktopColumns.split(" ").length).toBeGreaterThan(1);

  await page.setViewportSize({ width: 768, height: 900 });
  const mobileColumns = await grid.evaluate((element) => {
    return window.getComputedStyle(element).gridTemplateColumns;
  });
  expect(mobileColumns.split(" ").length).toBe(1);
});

test("supports keyboard-only submission with visible validation messaging", async ({
  page,
}) => {
  await page.goto("/");

  await page.keyboard.press("Tab");
  await expect(page.locator(":focus")).toHaveText("Skip to main content");

  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await expect(page.locator("#workspaceName")).toBeFocused();

  await page.keyboard.press("ControlOrMeta+A");
  await page.keyboard.type("ab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("ControlOrMeta+A");
  await page.keyboard.type("invalid");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Space");

  await expect(page.getByText("Fix 2 fields before saving.")).toBeVisible();
  await expect(page.locator("#workspaceName")).toBeFocused();

  await page.locator("#workspaceName").fill("Ops Seoul");
  await page.locator("#supportEmail").fill("ops-seoul@example.com");
  await page.getByRole("button", { name: "Save settings" }).click();

  await expect(page.getByText("Settings saved for Ops Seoul (Asia/Seoul).")).toBeVisible();
});
