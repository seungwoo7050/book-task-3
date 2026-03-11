import { expect, test } from "@playwright/test";

test("runs recommendation and offline eval flow", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "MCP 실험 콘솔" })).toBeVisible();

  await page.getByRole("button", { name: "Candidate 실행" }).click();

  await expect(
    page.getByText(
      /Release Check Bot는 release-management, changesets, semver 역량이 직접 맞습니다\..*실사용 신호 기준으로도 우선순위가 강화되었습니다\./i
    )
  ).toBeVisible();

  await page.getByRole("button", { name: "Compare 갱신" }).click();
  await expect(page.getByText("Baseline nDCG@3")).toBeVisible();
  await expect(page.getByText("Uplift")).toBeVisible();
});
