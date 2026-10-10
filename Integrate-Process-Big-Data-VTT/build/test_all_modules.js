// Layer 2 test: duyệt tất cả 5 module (sandbox + bank) bằng Chrome hệ thống.
const puppeteer = require("puppeteer-core");
const BASE = process.env.BASE || "http://localhost:8921";
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const MODULES = [
  { slug: "00-nen-tang-csdl", prefix: "m00", sqlCount: 50 },
  { slug: "01-data-integration-overview", prefix: "m01", sqlCount: 16 },
  { slug: "02-schema-alignment", prefix: "m02", sqlCount: 50 },
  { slug: "03-mediation-query-bigdata", prefix: "m03", sqlCount: 16 },
  { slug: "04-record-linkage-entity-resolution", prefix: "m04", sqlCount: 50 },
];

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
  let failures = 0;

  for (const m of MODULES) {
    const page = await browser.newPage();
    const errors = [];
    page.on("console", (msg) => { if (msg.type() === "error" && !msg.text().includes("Failed to load resource")) errors.push(msg.text()); });
    page.on("pageerror", (e) => errors.push("pageerror: " + e.message));

    console.log(`\n== ${m.slug} ==`);
    try {
      await page.goto(`${BASE}/vi/modules/${m.slug}/index.html`, { waitUntil: "networkidle0", timeout: 30000 });
      await page.waitForSelector(`#sb-mount-${m.prefix} .sb-main`, { timeout: 15000 });
      const n = await page.$$eval(`#sb-mount-${m.prefix} .sb-item`, els => els.length);
      console.log(`  sandbox: ${n} cau (ky vong ${m.sqlCount})`);
      if (n !== m.sqlCount) { console.log(`  FAIL: so cau sandbox sai`); failures++; }

      // chay + cham 1 cau dau bang chinh loi giai mau
      await page.click(`#sb-mount-${m.prefix} #sb-show-sol`);
      const sol = await page.$eval(`#sb-mount-${m.prefix} .sb-sol`, el => el.textContent);
      await page.evaluate((sql, p) => { document.querySelector(`#sb-mount-${p} #sb-editor`).value = sql; }, sol, m.prefix);
      await page.click(`#sb-mount-${m.prefix} #sb-grade`);
      await page.waitForFunction((p) => document.querySelector(`#sb-mount-${p} #sb-out p.ok, #sb-mount-${p} #sb-out p.no`), { timeout: 5000 }, m.prefix);
      const grade = await page.$eval(`#sb-mount-${m.prefix} #sb-out p`, el => el.textContent);
      console.log(`  cham cau dau: ${grade.slice(0, 40)}`);
      if (!grade.includes("Chính xác")) { console.log("  FAIL: cham sai cau dau"); failures++; }

      await page.goto(`${BASE}/vi/modules/${m.slug}/bank.html`, { waitUntil: "networkidle0", timeout: 20000 });
      await page.waitForSelector(".bk-item", { timeout: 10000 });
      const bkCount = await page.$$eval(".bk-item", els => els.length);
      console.log(`  bank trang 1: ${bkCount} cau`);
      await page.click(".bk-item .bk-opt");
      await page.waitForSelector(".bk-item .bk-explain:not([hidden])", { timeout: 5000 });
      console.log("  bank: bam dap an -> co giai thich OK");

      if (errors.length) { console.log("  CONSOLE ERRORS:", errors); failures++; }
      else console.log("  khong co console error");
    } catch (e) {
      console.log("  EXCEPTION:", e.message);
      failures++;
    }
    await page.close();
  }

  await browser.close();
  console.log(failures ? `\n❌ CO ${failures} LOI` : "\n✅ TAT CA 5 MODULE PASS");
  process.exit(failures ? 1 : 0);
})();
