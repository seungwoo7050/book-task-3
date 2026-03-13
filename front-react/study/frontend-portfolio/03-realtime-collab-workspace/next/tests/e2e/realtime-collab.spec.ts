import { expect, test } from "@playwright/test";

test("syncs board edits and presence across two pages", async ({ browser }) => {
  const context = await browser.newContext();
  const atlas = await context.newPage();
  const rio = await context.newPage();

  await atlas.goto("/?viewer=atlas");
  await rio.goto("/?viewer=rio");

  await expect(atlas.getByTestId("presence-list")).toContainText("Atlas");
  await expect(atlas.getByTestId("presence-list")).toContainText("Rio", {
    timeout: 10_000,
  });

  await atlas.getByTestId("card-input-card-1").fill("War room sync");
  await expect(rio.getByTestId("card-input-card-1")).toHaveValue(
    "War room sync",
  );
});

test("replays queued patches after reconnect and surfaces conflicts", async ({
  browser,
}) => {
  const context = await browser.newContext();
  const atlas = await context.newPage();
  const rio = await context.newPage();

  await atlas.goto("/?viewer=atlas");
  await rio.goto("/?viewer=rio");

  await atlas.getByTestId("disconnect-button").click();
  await expect(atlas.getByTestId("connection-status")).toHaveText(
    "Disconnected",
  );

  await atlas.getByTestId("card-input-card-2").fill("Queued while offline");
  await expect(rio.getByTestId("card-input-card-2")).not.toHaveValue(
    "Queued while offline",
  );

  await atlas.getByTestId("reconnect-button").click();
  await expect(rio.getByTestId("card-input-card-2")).toHaveValue(
    "Queued while offline",
    { timeout: 10_000 },
  );

  await atlas.getByTestId("card-input-card-1").fill("Atlas version");
  await rio.getByTestId("card-input-card-1").fill("Rio version");
  await expect(atlas.getByTestId("conflict-banner")).toContainText("Conflict detected", {
    timeout: 10_000,
  });
});
