import { test, expect } from "@playwright/test";

test("ページタイトルが表示される", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/石油備蓄/);
});

test("ヘッダータイトルが表示される", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("[data-testid='header-title']")).toBeVisible();
});

test("3枚のリザーブカードが表示される", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("[data-testid='reserve-card']")).toHaveCount(3, {
    timeout: 15_000,
  });
});

test("チャートが表示される", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("[data-testid='reserves-chart']")).toBeVisible({
    timeout: 15_000,
  });
});

test("言語切替で日本語タイトルに変わる", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("[data-testid='reserve-card']")).toHaveCount(3, {
    timeout: 15_000,
  });
  await page.locator("select").selectOption("ja");
  await expect(page.locator("[data-testid='header-title']")).toContainText(
    "日本の石油備蓄量"
  );
});
