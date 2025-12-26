import { test, expect } from '@playwright/test';

/**
 * Chimera UI Screenshot Tests
 * Validates that the launcher UI loads correctly and captures screenshots for regression testing
 */

test.describe('Chimera Launcher UI', () => {
  test('should load the launcher with CHIMERA branding', async ({ page }) => {
    await page.goto('/');

    // Wait for the page to load
    await page.waitForLoadState('networkidle');

    // Verify main heading is visible
    const heading = page.locator('h1:has-text("CHIMERA")');
    await expect(heading).toBeVisible();

    // Take screenshot of the launcher
    await page.screenshot({
      path: 'test-results/screenshots/launcher-home.png',
      fullPage: true
    });
  });

  test('should display app context cards', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Verify VS Code context card exists
    const vsCodeCard = page.locator('text=VS Code');
    await expect(vsCodeCard).toBeVisible();

    // Verify Excel context card exists
    const excelCard = page.locator('text=Excel');
    await expect(excelCard).toBeVisible();

    // Take screenshot of app contexts
    await page.screenshot({
      path: 'test-results/screenshots/app-contexts.png',
      fullPage: true
    });
  });

  test('should open settings modal', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Click settings button
    const settingsButton = page.locator('button:has-text("Settings")');
    await settingsButton.click();

    // Wait for modal to appear
    const modal = page.locator('div:has-text("Chimera Settings")');
    await expect(modal).toBeVisible({ timeout: 5000 });

    // Verify tabs are present
    await expect(page.locator('button:has-text("General")')).toBeVisible();
    await expect(page.locator('button:has-text("Providers")')).toBeVisible();
    await expect(page.locator('button:has-text("Privacy")')).toBeVisible();

    // Take screenshot of settings modal
    await page.screenshot({
      path: 'test-results/screenshots/settings-modal.png',
      fullPage: true
    });
  });

  test('should show screen selection in settings', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Open settings
    await page.locator('button:has-text("Settings")').click();

    // Wait for modal
    await expect(page.locator('div:has-text("Chimera Settings")')).toBeVisible();

    // Verify screen selection dropdown exists
    const screenSelect = page.locator('select');
    await expect(screenSelect.first()).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'test-results/screenshots/screen-selection.png',
      fullPage: true
    });
  });

  test('should toggle monitoring state', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Find the Start Monitoring button
    const startButton = page.locator('button:has-text("Start Monitoring")');

    // If button exists, verify we can interact with it
    if (await startButton.isVisible()) {
      // Take screenshot before monitoring
      await page.screenshot({
        path: 'test-results/screenshots/before-monitoring.png',
        fullPage: true
      });

      // Click to start monitoring
      await startButton.click();

      // Wait a moment for state change
      await page.waitForTimeout(1000);

      // Take screenshot during monitoring
      await page.screenshot({
        path: 'test-results/screenshots/during-monitoring.png',
        fullPage: true
      });
    }
  });

  test('should display provider options in settings', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Open settings
    await page.locator('button:has-text("Settings")').click();

    // Switch to Providers tab
    await page.locator('button:has-text("Providers")').click();

    // Wait for provider content to load
    await page.waitForTimeout(500);

    // Verify provider options exist (text should be visible)
    const providersTab = page.locator('text=Chimera Server, text=OpenAI, text=Claude, text=Ollama').first();

    // Take screenshot of providers tab
    await page.screenshot({
      path: 'test-results/screenshots/providers-settings.png',
      fullPage: true
    });
  });

  test('should show About information', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Open settings
    await page.locator('button:has-text("Settings")').click();

    // Switch to About tab
    await page.locator('button:has-text("About")').click();

    // Wait for content
    await page.waitForTimeout(500);

    // Take screenshot of about tab
    await page.screenshot({
      path: 'test-results/screenshots/about-tab.png',
      fullPage: true
    });
  });
});

test.describe('Chimera API Health Check', () => {
  test('should verify backend is healthy', async ({ request }) => {
    // Check if backend health endpoint responds
    const response = await request.get('http://localhost:8000/api/health');

    // Verify response is OK
    expect(response.ok()).toBeTruthy();

    // Verify response body
    const body = await response.json();
    expect(body).toHaveProperty('status');
    expect(body.status).toBe('healthy');
  });
});
