import { expect, test } from "@playwright/test";
import path from "node:path";

const assetDir =
  "/Users/woopinbell/work/chat-bot/study1/08-capstone-submission/v0-initial-demo/docs/presentation-assets";

test("captures v0 presentation flow", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1200 });
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "MCP 추천 운영 데모" })).toBeVisible();
  await page.locator("section.hero").screenshot({
    path: path.join(assetDir, "01-overview.png")
  });

  await page.getByRole("button", { name: "추천 실행" }).click();
  await expect(page.getByText("release-check-bot")).toBeVisible();
  await expect(
    page.getByText(
      /Release Check Bot는 .*현재 클라이언트 1\.2\.0 \/ stdio \/ node 환경과 호환됩니다\./i
    )
  ).toBeVisible();
  await page
    .getByRole("heading", { name: "추천 실행" })
    .locator("xpath=..")
    .screenshot({
      path: path.join(assetDir, "02-baseline-recommendation.png")
    });

  await page.getByRole("button", { name: "오프라인 평가 실행" }).click();
  await expect(page.getByText("Top-3 recall")).toBeVisible();
  await expect(page.getByText("Explanation completeness")).toBeVisible();
  await page
    .getByRole("heading", { name: "오프라인 평가" })
    .locator("xpath=..")
    .screenshot({
      path: path.join(assetDir, "03-offline-eval.png")
    });

  await page
    .getByRole("heading", { name: "카탈로그 샘플" })
    .locator("xpath=..")
    .screenshot({
      path: path.join(assetDir, "04-seeded-catalog.png")
    });
});
