import { expect, test } from "@playwright/test";

test("guards direct onboarding access without a session", async ({ page }) => {
  await page.goto("/onboarding?step=review");

  await expect(page.getByText("Sign in before opening the onboarding flow")).toBeVisible();
  await page.getByRole("link", { name: "Back to sign-in" }).click();
  await expect(page.getByRole("heading", { name: /Build trust before the first workspace goes live/i })).toBeVisible();
});

test("supports sign-in, draft restore, and submit retry", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/onboarding/);

  await page.getByLabel("Workspace name").fill("Lattice Cloud");
  await page.getByLabel("Industry").fill("Developer tooling");
  await page.getByLabel("Region").selectOption("Seoul");
  await page.getByLabel("Team size").selectOption("11-50");
  await page.getByLabel("Compliance contact").fill("not-an-email");
  await page.getByRole("button", { name: "Save draft" }).click();
  await expect(page.getByText("Enter a valid compliance contact email.")).toBeVisible();

  await page.getByLabel("Compliance contact").fill("compliance@latticecloud.dev");
  await page.getByRole("button", { name: "Save draft" }).click();
  await expect(page.getByText("Draft saved to the local demo workspace.")).toBeVisible();

  await page.reload();
  await expect(page.getByLabel("Workspace name")).toHaveValue("Lattice Cloud");

  await page.getByRole("button", { name: "Go to invites" }).click();
  await page.getByLabel("Invite email").fill("ops@latticecloud.dev");
  await page.getByLabel("Role").selectOption("Admin");
  await page.getByRole("button", { name: "Add invite" }).click();
  await expect(page.getByText("ops@latticecloud.dev")).toBeVisible();

  await page.getByRole("button", { name: "Continue to review" }).click();
  await page.getByRole("checkbox", { name: /Simulate the next submit failure/i }).check();
  await page.getByRole("button", { name: "Mark review complete" }).click();
  await page.getByRole("button", { name: "Submit onboarding" }).click();
  await expect(page.getByText(/Submission failed/i)).toBeVisible();

  await page.getByRole("button", { name: "Submit onboarding" }).click();
  await expect(page.getByText(/Submitted Lattice Cloud at/i)).toBeVisible();
});
