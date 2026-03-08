import { expect, test } from "@playwright/test";

test("runs recommendation and offline eval flow", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "MCP 추천 운영 데모" })).toBeVisible();

  await page.getByLabel("추천 질의").fill("배포 전에 manifest 호환성과 릴리즈 체크를 같이 보고 싶어요");
  await page.getByLabel("release-management").check();
  await page.getByLabel("semver").check();
  await page.getByRole("button", { name: "추천 실행" }).click();

  await expect(page.getByText("release-check-bot")).toBeVisible();
  await expect(
    page.getByText(/Release Check Bot는 .*현재 클라이언트 1\.2\.0 \/ stdio \/ node 환경과 호환됩니다\./i)
  ).toBeVisible();

  await page.getByRole("button", { name: "오프라인 평가 실행" }).click();
  await expect(page.getByText("Top-3 recall")).toBeVisible();
  await expect(page.getByText("100.0%")).toBeVisible();
});
