import { expect, test } from "@playwright/test";
import path from "node:path";

const assetDir =
  "/Users/woopinbell/work/chat-bot/study1/08-capstone-submission/v2-submission-polish/docs/presentation-assets";

test("captures presentation flow for v2 capstone", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1200 });
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "MCP 제출 운영 콘솔" })).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "01-overview.png"),
    fullPage: true
  });

  await page.getByRole("button", { name: "Candidate 실행" }).click();
  await expect(
    page.getByText(
      /Release Check Bot는 release-management, changesets, semver 역량이 직접 맞습니다\..*실사용 신호 기준으로도 우선순위가 강화되었습니다\./i
    )
  ).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "02-candidate-recommendation.png"),
    fullPage: true
  });

  await page.getByRole("button", { name: "Compare 갱신" }).click();
  await expect(page.getByRole("heading", { name: "Compare Snapshot" })).toBeVisible();
  await expect(page.getByText(/^Uplift$/)).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "03-compare-snapshot.png"),
    fullPage: true
  });

  await page.getByRole("button", { name: "Release Gate 실행" }).scrollIntoViewIfNeeded();
  await page.getByRole("button", { name: "Release Gate 실행" }).click();
  await expect(page.getByRole("heading", { name: "Release Quality" })).toBeVisible();
  await expect(page.getByText("PASS").first()).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "04-release-gate-pass.png"),
    fullPage: true
  });

  await expect(page.getByRole("heading", { name: "Submission Artifact Preview" })).toBeVisible();
  await page.screenshot({
    path: path.join(assetDir, "05-artifact-preview.png"),
    fullPage: true
  });
});
