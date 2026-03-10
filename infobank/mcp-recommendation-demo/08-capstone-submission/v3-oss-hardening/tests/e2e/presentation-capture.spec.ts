import { expect, test } from "@playwright/test";
import path from "node:path";
import { fileURLToPath } from "node:url";

const assetDir =
  path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../docs/presentation-assets");

test("captures presentation flow for v3 oss hardening", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1200 });
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "MCP OSS 운영 콘솔 로그인" })).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "01-login.png"),
    fullPage: true
  });

  await page.getByRole("button", { name: "로그인" }).click();
  await expect(page.getByRole("heading", { name: "MCP OSS 운영 콘솔" })).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "02-owner-dashboard.png"),
    fullPage: true
  });

  await page.getByRole("button", { name: "Candidate 실행" }).click();
  await expect(
    page.getByText(/실사용 신호 기준으로도 우선순위가 강화되었습니다\./i).first()
  ).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "03-candidate-recommendation.png"),
    fullPage: true
  });

  await page.getByRole("button", { name: "Release Gate Job" }).click();
  await expect(page.getByText("release gate가 PASS로 완료됐습니다.").first()).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "04-job-activity.png"),
    fullPage: true
  });

  await expect(page.getByRole("heading", { name: "Audit Log" })).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "05-audit-log.png"),
    fullPage: true
  });

  await page.getByRole("button", { name: "Artifact Export Job" }).click();
  await expect(page.getByRole("heading", { name: "Latest Artifact Preview" })).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "06-artifact-preview.png"),
    fullPage: true
  });
});
