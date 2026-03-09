import { expect, test } from "@playwright/test";
import path from "node:path";

const assetDir =
  "/Users/woopinbell/work/chat-bot/study1/08-capstone-submission/v1-ranking-hardening/docs/presentation-assets";

test("captures v1 presentation flow", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1200 });
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "MCP 실험 콘솔" })).toBeVisible();
  await page.locator("section.hero").screenshot({
    path: path.join(assetDir, "01-overview.png")
  });

  await page.getByRole("button", { name: "Baseline 실행" }).click();
  await page.getByRole("button", { name: "Candidate 실행" }).click();
  const recommendationCard = page.getByRole("heading", { name: "추천 실험" }).locator("xpath=..");
  await expect(recommendationCard.getByText("release-check-bot").first()).toBeVisible();
  await expect(
    page.getByText(
      /Release Check Bot는 release-management, changesets, semver 역량이 직접 맞습니다\..*실사용 신호 기준으로도 우선순위가 강화되었습니다\./i
    )
  ).toBeVisible();
  await recommendationCard.screenshot({ path: path.join(assetDir, "02-baseline-candidate.png") });

  await page.getByRole("button", { name: "Compare 갱신" }).click();
  await expect(page.getByText("Baseline nDCG@3")).toBeVisible();
  await expect(page.getByText("Candidate nDCG@3")).toBeVisible();
  await page
    .getByRole("heading", { name: "Compare Snapshot" })
    .locator("xpath=..")
    .screenshot({
      path: path.join(assetDir, "03-compare-snapshot.png")
    });

  await page.getByRole("button", { name: "채택 로그 남기기" }).first().click();
  await expect(
    page.getByRole("heading", { name: "Usage Totals" }).locator("xpath=..").getByText("18")
  ).toBeVisible();
  await page.getByLabel("Score Delta").fill("3");
  await page.getByLabel("Note").fill("candidate 정렬이 baseline보다 발표와 운영 설명에 더 적합했습니다.");
  await page.getByRole("button", { name: "피드백 저장" }).click();
  await page
    .getByRole("heading", { name: "Feedback Loop" })
    .locator("xpath=..")
    .screenshot({
      path: path.join(assetDir, "04-usage-feedback.png")
    });

  await page.getByLabel("Experiment Name").fill("signal-rerank-stage-demo");
  await page.getByRole("button", { name: "실험 생성" }).click();
  await expect(page.getByText("signal-rerank-stage-demo")).toBeVisible();
  await page
    .getByRole("heading", { name: "Experiment Console" })
    .locator("xpath=..")
    .screenshot({
      path: path.join(assetDir, "05-experiment-console.png")
    });
});
