// Spec de ejemplo de Playwright para un flujo. Cópialo a e2e/f01-book.spec.ts y adáptalo.
// Los selectores usan roles y etiquetas, así sobreviven a los cambios de estilo y de marca.
// Si la interfaz de tu app está en español, cambia los nombres de los selectores por tus textos.
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('F01 guest books a meeting', () => {
  test.beforeEach(async ({ page }) => {
    page.on('console', (msg) => {
      if (msg.type() === 'error') throw new Error(`console error: ${msg.text()}`);
    });
    page.on('response', (res) => {
      if (res.status() >= 500) throw new Error(`${res.status()} on ${res.url()}`);
    });
  });

  test('F01-H1 happy path', async ({ page }) => {
    await page.goto('/u/demo/30min');
    await page.getByRole('button', { name: /next available day/i }).click();
    await page.getByRole('button', { name: /10:00/ }).click();
    await page.getByLabel('Name').fill('Test Guest');
    await page.getByLabel('Email').fill('guest@example.test');
    await page.getByRole('button', { name: /confirm/i }).click();
    await expect(page.getByRole('heading', { name: /you are booked/i })).toBeVisible();

    const a11y = await new AxeBuilder({ page }).analyze();
    expect(a11y.violations).toEqual([]);
  });

  test('F01-E1 double submit creates one booking', async ({ page }) => {
    await page.goto('/u/demo/30min');
    await page.getByRole('button', { name: /next available day/i }).click();
    await page.getByRole('button', { name: /11:00/ }).click();
    await page.getByLabel('Name').fill('Twice');
    await page.getByLabel('Email').fill('twice@example.test');
    const confirm = page.getByRole('button', { name: /confirm/i });
    await Promise.all([confirm.click(), confirm.click()]);
    await expect(page.getByRole('heading', { name: /you are booked/i })).toBeVisible();
    // Luego verifica con tu API o con un helper de la base de datos que existe exactamente una reserva.
  });
});
