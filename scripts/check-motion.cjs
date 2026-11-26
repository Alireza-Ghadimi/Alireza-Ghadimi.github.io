/* Browser checks for the public animated homepage. Run against a local server. */
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const base = process.env.SITE_URL || 'http://127.0.0.1:4173';
(async () => {
  const browser = await chromium.launch({headless: true, ...(process.env.CHROMIUM_PATH ? {executablePath: process.env.CHROMIUM_PATH} : {})});
  const errors = [];
  const context = await browser.newContext({viewport: {width: 1440, height: 960}});
  const page = await context.newPage();
  page.on('pageerror', error => errors.push(error.message));
  page.on('response', response => {
    if (response.url().startsWith(base) && response.status() >= 400) errors.push(`${response.status()} ${response.url()}`);
  });
  const gifCount = () => page.locator('.project-motion[src$=".gif"]').count();
  try {
    await page.goto(`${base}/animated/?from=bookmark#work`);
    await page.waitForURL(`${base}/?from=bookmark#work`);
    await page.goto(`${base}/`);
    assert.equal(await page.locator('h1').innerText(), 'Alireza\nGhadimi.');
    assert.equal(await page.locator('.project-motion').count(), 15);
    const resumes = await page.locator('a[download]').evaluateAll(nodes => nodes.map(node => new URL(node.href).pathname));
    assert.deepEqual(resumes, Array(2).fill('/assets/Alireza-Ghadimi-Resume.pdf'));
    await page.waitForTimeout(1500);
    assert.equal(await gifCount(), 0, 'Offscreen GIFs should start as posters');
    const data = await page.locator('#category-data').textContent().then(JSON.parse);
    const tested = new Set();
    for (const category of data) {
      await page.locator(`[data-filter="${category.id}"]`).click();
      const visible = page.locator('.work-card:not([hidden])');
      assert(await visible.count() > 0);
      assert.equal(await page.locator('#work-panel').getAttribute('aria-labelledby'), `tab-${category.id}`);
      for (const trigger of await visible.locator('[data-case]').all()) {
        const id = await trigger.getAttribute('data-case');
        if (tested.has(id)) continue;
        await trigger.click();
        const dialog = page.locator(`#case-${id}`);
        assert(await dialog.isVisible());
        await page.keyboard.press('Escape');
        await page.waitForFunction(() => !document.querySelector('dialog[open]'));
        assert.equal(await page.evaluate(() => document.activeElement.dataset.case), id, 'Dialog focus was not restored');
        tested.add(id);
      }
    }
    assert.equal(tested.size, 15);
    await page.locator('#tab-selected').click();
    await page.locator('.project-motion').first().scrollIntoViewIfNeeded();
    await page.waitForFunction(() => !!document.querySelector('.project-motion[src$=".gif"]'));
    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.waitForFunction(() => !document.querySelector('.project-motion[src$=".gif"]'));
    await page.emulateMedia({reducedMotion: 'no-preference'});
    await page.waitForFunction(() => !!document.querySelector('.project-motion[src$=".gif"]'));
    await page.locator('#tab-selected').focus();
    await page.keyboard.press('End');
    assert.equal(await page.locator('#tab-biomedical').getAttribute('aria-selected'), 'true');
    await page.keyboard.press('Home');
    assert.equal(await page.locator('#tab-selected').getAttribute('aria-selected'), 'true');

    for (const width of [320, 390, 768, 1440]) {
      await page.setViewportSize({width, height: 900});
      await page.goto(`${base}/`);
      await page.waitForTimeout(1500);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Horizontal overflow at ${width}px`);
      if (width < 641) {
        await page.locator('.menu-toggle').click();
        assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'true');
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
      }
      for (const selector of ['#work', '#experience', '#research', '#background', '#contact', '.leaflab-section']) {
        await page.locator(selector).evaluate(node => node.scrollIntoView({block: 'start', behavior: 'instant'}));
        await page.waitForTimeout(1100);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Overflow at ${width}px ${selector}`);
      }
    }

    await page.emulateMedia({reducedMotion: 'reduce'});
    await page.goto(`${base}/`);
    await page.locator('.project-motion').first().scrollIntoViewIfNeeded();
    assert.equal(await page.locator('#motion-toggle').count(), 0);
    assert.equal(await gifCount(), 0);
    assert.equal(await page.evaluate(() => document.getAnimations().filter(a => a.playState === 'running').length), 0);
    const offline = await browser.newContext({javaScriptEnabled: false, viewport: {width: 390, height: 844}});
    const fallback = await offline.newPage();
    await fallback.goto(`${base}/`);
    assert.equal(await fallback.locator('.work-card:visible').count(), 15);
    assert.equal(await fallback.locator('.project-motion[src$=".png"]').count(), 15);
    await offline.close();
    assert.deepEqual(errors, []);
    console.log('PASS: public homepage, legacy redirect, 15 dialogs, 6 tabs, GIF visibility and reduced motion, no-JS fallback, mobile menu, and responsive scrolling.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
