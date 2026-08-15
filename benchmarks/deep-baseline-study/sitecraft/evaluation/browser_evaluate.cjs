#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const http = require("node:http");
const path = require("node:path");
const { chromium } = require("playwright");

const candidate = path.resolve(process.argv[2] || "");
const output = path.resolve(process.argv[3] || path.join(candidate, "browser-evidence"));
if (!fs.existsSync(path.join(candidate, "index.html"))) {
  throw new Error("Usage: browser_evaluate.cjs <candidate> [output-directory]");
}
fs.mkdirSync(output, { recursive: true });

const mime = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json" };
const server = http.createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
  if (pathname === "/favicon.ico") {
    response.writeHead(204).end();
    return;
  }
  const relative = pathname === "/" ? "index.html" : pathname.replace(/^\//, "");
  const target = path.resolve(candidate, relative);
  if (!target.startsWith(`${candidate}${path.sep}`) || !fs.existsSync(target) || !fs.statSync(target).isFile()) {
    response.writeHead(404).end("not found");
    return;
  }
  response.writeHead(200, { "content-type": mime[path.extname(target)] || "application/octet-stream" });
  fs.createReadStream(target).pipe(response);
});

const chromePaths = { darwin: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", linux: "/usr/bin/google-chrome" };
const launchOptions = { headless: true };
const chrome = process.env.CHROME_BIN || chromePaths[process.platform];
if (chrome && fs.existsSync(chrome)) launchOptions.executablePath = chrome;

async function loadPage(browser, base, contextOptions = {}) {
  const context = await browser.newContext(contextOptions);
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  const outsideRequests = [];
  page.on("console", message => { if (message.type() === "error") consoleErrors.push(message.text()); });
  page.on("pageerror", error => pageErrors.push(String(error)));
  page.on("request", request => {
    const url = request.url();
    if (!url.startsWith(base) && !url.startsWith("data:") && !url.startsWith("blob:")) outsideRequests.push(url);
  });
  await page.goto(base, { waitUntil: "networkidle" });
  return { context, page, consoleErrors, pageErrors, outsideRequests };
}

async function viewportCheck(browser, base, name, width, height, reducedMotion = "no-preference") {
  const state = await loadPage(browser, base, { viewport: { width, height }, reducedMotion });
  const layout = await state.page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    title: document.title,
    textLength: document.body.innerText.trim().length,
    routes: document.querySelectorAll('[data-testid="route-list"] [data-route-id]').length,
    visibleControls: [...document.querySelectorAll("button,input,select,[tabindex]")].filter(element => {
      const style = getComputedStyle(element);
      return style.display !== "none" && style.visibility !== "hidden";
    }).length,
  }));
  await state.page.screenshot({ path: path.join(output, `${name}.png`), fullPage: true });
  await state.context.close();
  return {
    name, width, height, reducedMotion, ...layout,
    noHorizontalOverflow: layout.scrollWidth <= layout.clientWidth,
    consoleErrors: state.consoleErrors,
    pageErrors: state.pageErrors,
    outsideRequests: state.outsideRequests,
    passed: layout.scrollWidth <= layout.clientWidth && layout.textLength > 300 && layout.routes === 3 && layout.visibleControls >= 8 && state.consoleErrors.length === 0 && state.pageErrors.length === 0 && state.outsideRequests.length === 0,
  };
}

async function staticFallback(browser, base) {
  const state = await loadPage(browser, base, { javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  const text = await state.page.locator("body").innerText();
  await state.context.close();
  const routeNames = ["Bracken Rise", "Rowan Loop", "Tor Line"].filter(name => text.includes(name));
  return { routeNames, passed: routeNames.length === 3 && text.length > 250 };
}

async function chooseGroup(page, value) {
  const group = page.locator('[data-testid="group-needs"]');
  if ((await group.evaluate(element => element.tagName)) === "SELECT") {
    await group.selectOption(value);
    return;
  }
  const select = group.locator("select");
  if (await select.count()) {
    await select.selectOption(value);
    return;
  }
  const control = group.locator(`button[value="${value}"], input[value="${value}"], [data-value="${value}"]`).first();
  if (await control.count()) {
    if ((await control.getAttribute("type")) === "radio") await control.check({ force: true }); else await control.click();
    return;
  }
  const byText = group.getByText(new RegExp(`^${value}$`, "i")).first();
  if (await byText.count()) await byText.click();
}

async function interactionCheck(browser, base) {
  const state = await loadPage(browser, base, { viewport: { width: 390, height: 844 } });
  const page = state.page;
  const routes = page.locator('[data-testid="route-list"] [data-route-id]');
  const closed = page.locator('[data-testid="route-list"] [data-route-id="bracken-rise"]');
  const closedDisabled = await closed.evaluate(element => element.disabled === true || element.getAttribute("aria-disabled") === "true");
  await closed.click({ force: true }).catch(() => {});
  const closedNotSelected = (await closed.getAttribute("aria-pressed")) !== "true";
  const summaryAfterClosedReview = await page.locator('[data-testid="plan-summary"]').innerText();
  const confirmControl = page.locator('[data-testid="confirm-plan"]');
  const confirmDisabledAfterClosed = await confirmControl.evaluate(element => element.disabled === true || element.getAttribute("aria-disabled") === "true");
  const essentials = page.locator('[data-testid="essentials"] input[type="checkbox"]');
  const essentialCount = await essentials.count();
  let closedReviewStatus = await page.locator('[data-testid="plan-status"]').innerText();
  let closedCannotBecomePlan = confirmDisabledAfterClosed;
  if (!confirmDisabledAfterClosed) {
    for (let index = 0; index < essentialCount; index += 1) await essentials.nth(index).check();
    await confirmControl.click();
    await page.waitForTimeout(50);
    closedReviewStatus = await page.locator('[data-testid="plan-status"]').innerText();
    closedCannotBecomePlan = /Rowan Loop/i.test(summaryAfterClosedReview) && /Rowan Loop/i.test(closedReviewStatus) && !/Bracken Rise confirmed|confirmed[^.]*Bracken Rise/i.test(closedReviewStatus);
  }

  await chooseGroup(page, "child");
  await page.waitForTimeout(100);
  const confirmDisabledAfterGroup = await confirmControl.evaluate(element => element.disabled === true || element.getAttribute("aria-disabled") === "true");
  const summaryAfterGroup = await page.locator('[data-testid="plan-summary"]').innerText();
  const groupUpdatesGuidance = /child|family|young/i.test(summaryAfterGroup) && /Rowan Loop/i.test(summaryAfterGroup);

  const rowan = page.locator('[data-testid="route-list"] [data-route-id="rowan-loop"]');
  await rowan.focus();
  await page.keyboard.press("ArrowRight");
  await page.waitForTimeout(100);
  const activeId = await page.evaluate(() => document.activeElement?.getAttribute("data-route-id"));
  const selectedId = await routes.evaluateAll(elements => elements.find(element => element.getAttribute("aria-pressed") === "true")?.getAttribute("data-route-id") || null);
  const arrowNavigation = activeId === "tor-line" && selectedId === "tor-line";

  for (let index = 0; index < essentialCount; index += 1) {
    const box = essentials.nth(index);
    if (await box.isChecked()) await box.uncheck();
  }
  await confirmControl.click({ force: true });
  await page.waitForTimeout(50);
  const status = page.locator('[data-testid="plan-status"]');
  const invalidText = await status.innerText();
  const invalidFocus = await status.evaluate(element => document.activeElement === element || element.contains(document.activeElement));
  const invalidGuard = essentialCount > 0 && /check|essential|remain|required|missing|need/i.test(invalidText) && invalidFocus;

  for (let index = 0; index < essentialCount; index += 1) await essentials.nth(index).check();
  await confirmControl.click({ force: true });
  await page.waitForTimeout(50);
  const successText = await status.innerText();
  const successSummary = /Tor Line/i.test(successText) && /child|family|young/i.test(successText) && /ready|confirmed|plan/i.test(successText);
  const routeCount = await routes.count();

  await page.screenshot({ path: path.join(output, "interaction-final.png"), fullPage: true });
  await state.context.close();
  return {
    routeCount, closedDisabled, closedNotSelected, confirmDisabledAfterClosed,
    confirmDisabledAfterGroup, closedCannotBecomePlan,
    summaryAfterClosedReview, closedReviewStatus,
    groupUpdatesGuidance, arrowNavigation, activeId, selectedId, essentialCount,
    invalidGuard, invalidFocus, invalidText, successSummary, successText,
    consoleErrors: state.consoleErrors, pageErrors: state.pageErrors, outsideRequests: state.outsideRequests,
    passed: closedCannotBecomePlan && !confirmDisabledAfterGroup && groupUpdatesGuidance && arrowNavigation && invalidGuard && successSummary && state.consoleErrors.length === 0 && state.pageErrors.length === 0 && state.outsideRequests.length === 0,
  };
}

async function reducedMotionCheck(browser, base) {
  const state = await loadPage(browser, base, { viewport: { width: 390, height: 844 }, reducedMotion: "reduce" });
  const result = await state.page.evaluate(() => {
    const offenders = [...document.querySelectorAll("body *")].filter(element => {
      const style = getComputedStyle(element);
      return style.display !== "none" && style.visibility !== "hidden" && style.animationIterationCount === "infinite" && parseFloat(style.animationDuration) > 0.05;
    }).map(element => `${element.tagName.toLowerCase()}${element.id ? `#${element.id}` : ""}`);
    return { offenders };
  });
  await state.context.close();
  return { ...result, passed: result.offenders.length === 0 };
}

(async () => {
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  const base = `http://127.0.0.1:${address.port}/`;
  const browser = await chromium.launch(launchOptions);
  try {
    const viewports = [
      await viewportCheck(browser, base, "desktop-1440x1000", 1440, 1000),
      await viewportCheck(browser, base, "mobile-390x844", 390, 844),
      await viewportCheck(browser, base, "narrow-320x800", 320, 800),
    ];
    const staticFallbackResult = await staticFallback(browser, base);
    const interaction = await interactionCheck(browser, base);
    const reducedMotion = await reducedMotionCheck(browser, base);
    const result = {
      project: "cairn",
      candidate: path.basename(candidate),
      browser: "Google Chrome via Playwright",
      viewports, staticFallback: staticFallbackResult, interaction, reducedMotion,
      passed: viewports.every(item => item.passed) && staticFallbackResult.passed && interaction.passed && reducedMotion.passed,
      evidenceBoundary: "Headless Chrome covers the listed viewports and scripted interactions; it is not screen-reader, native-device, production, or cross-browser evidence.",
    };
    fs.writeFileSync(path.join(output, "browser-results.json"), `${JSON.stringify(result, null, 2)}\n`);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exitCode = result.passed ? 0 : 1;
  } finally {
    await browser.close();
    server.close();
  }
})().catch(error => { console.error(error); server.close(); process.exitCode = 2; });
