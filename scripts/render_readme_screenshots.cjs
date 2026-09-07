#!/usr/bin/env node
// Render only the repository's synthetic documentation, with an isolated browser.
const { chromium } = require('playwright');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
const fs = require('node:fs');
const root = path.resolve(__dirname, '..');
(async () => {
  const options = { headless: true, timeout: 30000 };
  if (process.env.CHROME) options.executablePath = process.env.CHROME;
  else if (process.platform === 'darwin') options.executablePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const browser = await chromium.launch(options);
  try {
    fs.mkdirSync(path.join(root, 'docs/images'), { recursive: true });
    for (const lang of ['zh', 'en']) {
      for (const [shot, height] of [['chat',1000], ['home',1000], ['map',900], ['logistics',1000]]) {
        const page = await browser.newPage({ viewport: { width:1600, height }, deviceScaleFactor:1 });
        // Illustrations are self-contained; do not load remote assets or profiles.
        await page.route(/^https?:/, route => route.abort());
        const url = pathToFileURL(path.join(root, 'docs/demo-screenshots.html'));
        url.search = new URLSearchParams({lang, shot}).toString();
        await page.goto(url.href, { waitUntil:'load', timeout:15000 });
        await page.evaluate(() => document.fonts.ready);
        if (await page.locator(`.shot-${shot}`).isVisible() === false) throw new Error(`Hidden illustration: ${shot}`);
        await page.screenshot({ path:path.join(root, `docs/images/${shot}-${lang}.png`), timeout:15000 });
        console.log(`Rendered ${shot}-${lang}: 1600 × ${height}`);
        await page.close();
      }
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
