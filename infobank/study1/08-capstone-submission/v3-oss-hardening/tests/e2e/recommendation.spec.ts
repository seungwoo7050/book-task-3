import { expect, test, type Page } from "@playwright/test";

async function login(page: Page, email: string, password: string) {
  await page.goto("/");
  const emailField = page.getByRole("textbox", { name: "Email", exact: true });
  await emailField.waitFor({ state: "visible" });
  await emailField.fill(email);
  await page.getByRole("textbox", { name: "Password", exact: true }).fill(password);
  await page.getByRole("button", { name: "로그인" }).click();
  await expect(page.getByRole("heading", { name: "MCP OSS 운영 콘솔" })).toBeVisible();
}

test("owner creates access", async ({ page }) => {
  await login(page, "owner@study1.local", "ChangeMe123!");
  await expect(page.getByRole("heading", { name: "Team Access" })).toBeVisible();

  const suffix = Date.now().toString().slice(-6);
  const operatorEmail = `operator-e2e-${suffix}@study1.local`;
  const viewerEmail = `viewer-e2e-${suffix}@study1.local`;
  const operatorPassword = "Operator123!";
  const viewerPassword = "Viewer123!";

  await page.getByRole("textbox", { name: "Email", exact: true }).fill(
    operatorEmail
  );
  await page.getByRole("textbox", { name: "Name", exact: true }).fill("Operator E2E");
  await page.getByRole("combobox", { name: "Role", exact: true }).selectOption("operator");
  await page.getByRole("textbox", { name: "Password", exact: true }).fill(operatorPassword);
  await page.getByRole("button", { name: "사용자 생성" }).click();
  await expect(page.getByText("사용자를 생성했습니다.", { exact: true })).toBeVisible();

  await page.getByRole("textbox", { name: "Email", exact: true }).fill(
    viewerEmail
  );
  await page.getByRole("textbox", { name: "Name", exact: true }).fill("Viewer E2E");
  await page.getByRole("combobox", { name: "Role", exact: true }).selectOption("viewer");
  await page.getByRole("textbox", { name: "Password", exact: true }).fill(viewerPassword);
  await page.getByRole("button", { name: "사용자 생성" }).click();
  await expect(page.getByText("사용자를 생성했습니다.", { exact: true })).toBeVisible();
});

test("operator runs jobs", async ({ page }) => {
  await login(page, "operator@study1.local", "Operator123!");

  await page.getByRole("button", { name: "Export Bundle" }).click();
  await expect(page.getByPlaceholder('{"catalogEntries":[...]}')).toContainText(
    '"catalogEntries"'
  );
  await page.getByRole("button", { name: "Import Bundle" }).click();
  await expect(page.getByText("catalog bundle import를 적용했습니다.", { exact: true })).toBeVisible();

  await page.getByRole("button", { name: "Candidate 실행" }).click();
  await expect(
    page.getByText(/실사용 신호 기준으로도 우선순위가 강화되었습니다\./i).first()
  ).toBeVisible();

  await page.getByRole("button", { name: "Compare Job" }).click();
  await expect(page.getByText(/compare snapshot이 완료됐고 uplift/i).first()).toBeVisible();

  await page.getByRole("button", { name: "Release Gate Job" }).click();
  await expect(page.getByText("release gate가 PASS로 완료됐습니다.").first()).toBeVisible();

  await page.getByRole("button", { name: "Artifact Export Job" }).click();
  await expect(page.getByText("submission artifact export가 완료됐습니다.").first()).toBeVisible();
  await expect(page.getByRole("heading", { name: "Latest Artifact Preview" })).toBeVisible();
});

test("viewer sees read-only console", async ({ page }) => {
  await login(page, "viewer@study1.local", "Viewer123!");
  await expect(page.getByText("viewer는 운영 실행 버튼이 비활성화됩니다.")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Latest Artifact Preview" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Candidate 실행" })).toHaveCount(0);
});
