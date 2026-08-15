#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

const candidate = path.resolve(process.argv[2] || "");
const output = path.resolve(process.argv[3] || path.join(candidate, "browser-evidence"));
if (!fs.existsSync(path.join(candidate, "index.html"))) {
  throw new Error("Usage: browser_evaluate.cjs <candidate> [output-directory]");
}
fs.mkdirSync(output, { recursive: true });

const commonChromePaths = {
  darwin: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  linux: "/usr/bin/google-chrome",
  win32: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
};
const executablePath = process.env.CHROME_BIN || commonChromePaths[process.platform];
const launchOptions = { headless: true };
if (executablePath && fs.existsSync(executablePath)) {
  launchOptions.executablePath = executablePath;
}

async function inspectViewport(browser, name, width, height, reducedMotion = "no-preference") {
  const page = await browser.newPage({ viewport: { width, height }, reducedMotion });
  const consoleErrors = [];
  const pageErrors = [];
  const networkRequests = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => pageErrors.push(String(error)));
  page.on("request", (request) => {
    const url = request.url();
    if (!url.startsWith("file:") && !url.startsWith("data:") && !url.startsWith("blob:")) {
      networkRequests.push(url);
    }
  });
  await page.goto(pathToFileURL(path.join(candidate, "index.html")).href, {
    waitUntil: "load",
  });
  await page.waitForTimeout(250);
  const state = await page.evaluate(() => ({
    title: document.title,
    textLength: document.body.innerText.trim().length,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    warningVisible: [...document.querySelectorAll("body *")].some((element) => {
      const text = element.textContent || "";
      const style = getComputedStyle(element);
      return /demonstration data/i.test(text)
        && /not for navigation/i.test(text)
        && style.display !== "none"
        && style.visibility !== "hidden";
    }),
    focusedElements: document.querySelectorAll(
      "button, a[href], input, select, textarea, [tabindex]:not([tabindex='-1'])"
    ).length,
  }));
  const screenshot = `${name}.png`;
  await page.screenshot({ path: path.join(output, screenshot), fullPage: true });
  await page.close();
  return {
    name,
    width,
    height,
    reducedMotion,
    screenshot,
    ...state,
    noHorizontalOverflow: state.scrollWidth <= state.clientWidth,
    consoleErrors,
    pageErrors,
    networkRequests,
    passed:
      state.textLength > 100
      && state.warningVisible
      && state.scrollWidth <= state.clientWidth
      && consoleErrors.length === 0
      && pageErrors.length === 0
      && networkRequests.length === 0,
  };
}

async function exerciseInteraction(browser) {
  const page = await browser.newPage({ viewport: { width: 1024, height: 900 } });
  const networkRequests = [];
  page.on("request", (request) => {
    const url = request.url();
    if (!url.startsWith("file:") && !url.startsWith("data:") && !url.startsWith("blob:")) {
      networkRequests.push(url);
    }
  });
  await page.goto(pathToFileURL(path.join(candidate, "index.html")).href, {
    waitUntil: "load",
  });

  const timeControl = page
    .locator("button, [role='tab'], [role='radio'], label")
    .filter({ hasText: "09:00" })
    .last();
  let pointerUpdate = false;
  let keyboardUpdate = false;
  let selectedStateExposed = false;
  if ((await timeControl.count()) > 0) {
    await timeControl.click();
    await page.waitForTimeout(100);
    pointerUpdate = await page.evaluate(
      () => /31\s*kn/i.test(document.body.innerText) && /1\.8\s*m/i.test(document.body.innerText)
    );
    selectedStateExposed = await timeControl.evaluate((element) => {
      let owner = element;
      if (owner.tagName === "LABEL" && owner.htmlFor) {
        owner = document.getElementById(owner.htmlFor) || owner;
      }
      return owner.getAttribute("aria-selected") === "true"
        || owner.getAttribute("aria-pressed") === "true"
        || owner.getAttribute("aria-checked") === "true"
        || owner.checked === true;
    });

    await page.reload({ waitUntil: "load" });
    const keyboardControl = page
      .locator("button, [role='tab'], [role='radio'], label")
      .filter({ hasText: "09:00" })
      .last();
    const focusKind = await keyboardControl.evaluate((element) => {
      let owner = element;
      if (owner.tagName === "LABEL" && owner.htmlFor) {
        owner = document.getElementById(owner.htmlFor) || owner;
      }
      owner.focus();
      return owner.tagName;
    });
    await page.keyboard.press(focusKind === "INPUT" ? "Space" : "Enter");
    await page.waitForTimeout(100);
    keyboardUpdate = await page.evaluate(
      () => /31\s*kn/i.test(document.body.innerText) && /1\.8\s*m/i.test(document.body.innerText)
    );
  }

  const email = page.locator('input[type="email"]').first();
  let invalidRejected = false;
  let submittingState = false;
  let successState = false;
  let failureState = false;
  let validHandledLocally = false;
  let formStateText = "";
  if ((await email.count()) > 0) {
    await email.fill("not-an-email");
    invalidRejected = await email.evaluate((element) => !element.checkValidity());
    await email.fill("crew@example.test");
    await page.locator("form").first().evaluate((form) => form.requestSubmit());
    submittingState = await page.evaluate(() => {
      const text = document.body.innerText;
      const submit = document.querySelector('button[type="submit"]');
      return /(?:submitting|running|working|please wait|loading)/i.test(text)
        || submit?.disabled === true
        || submit?.getAttribute("aria-busy") === "true";
    });
    await page.waitForTimeout(1200);
    formStateText = await page.evaluate(() => document.body.innerText);
    successState = /(?:complete|success|ready|thanks|thank you)/i.test(formStateText);
    validHandledLocally = /(?:not\s+(?:sent|stored|transmit|retained)|nothing\s+(?:sent|stored|transmit)|no\s+[^.]{0,30}\s(?:was\s+)?(?:sent|stored|transmitted|retained)|local(?:ly|[- ]only))/i.test(formStateText);

    await email.fill("fail@demo.test");
    await page.locator("form").first().evaluate((form) => form.requestSubmit());
    await page.waitForTimeout(1200);
    formStateText = await page.evaluate(() => document.body.innerText);
    failureState = /(?:failed|failure|interrupted|could not|try again)/i.test(formStateText);
  }
  await page.screenshot({ path: path.join(output, "interaction-final.png"), fullPage: true });
  await page.close();
  return {
    pointerUpdate,
    keyboardUpdate,
    selectedStateExposed,
    invalidRejected,
    submittingState,
    successState,
    failureState,
    validHandledLocally,
    networkRequests,
    passed:
      pointerUpdate
      && keyboardUpdate
      && selectedStateExposed
      && invalidRejected
      && submittingState
      && successState
      && failureState
      && validHandledLocally
      && networkRequests.length === 0,
  };
}

(async () => {
  const browser = await chromium.launch(launchOptions);
  try {
    const viewports = [];
    viewports.push(await inspectViewport(browser, "desktop-1440x1000", 1440, 1000));
    viewports.push(await inspectViewport(browser, "mobile-390x844", 390, 844));
    viewports.push(await inspectViewport(browser, "narrow-320x800", 320, 800));
    viewports.push(await inspectViewport(browser, "reduced-motion-390x844", 390, 844, "reduce"));
    const interaction = await exerciseInteraction(browser);
    const result = {
      candidate: path.basename(candidate),
      browser: "Google Chrome via Playwright",
      source: "local index.html",
      viewports,
      interaction,
      passed: viewports.every((item) => item.passed) && interaction.passed,
      evidenceBoundary:
        "Headless Chrome evidence covers these exact viewports and interactions; it is not a screen-reader, native-device, production, or cross-browser claim.",
    };
    fs.writeFileSync(path.join(output, "browser-results.json"), `${JSON.stringify(result, null, 2)}\n`);
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exitCode = result.passed ? 0 : 1;
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 2;
});
