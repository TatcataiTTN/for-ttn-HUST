// Layer 2 test: duyệt thật bằng Chrome hệ thống (puppeteer-core), kiểm tra SQL sandbox + bank thật chạy.
const puppeteer = require("puppeteer-core");

const BASE = process.env.BASE || "http://localhost:8921";
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: true });
  const page = await browser.newPage();
  const errors = [];
  page.on("console", (msg) => { if (msg.type() === "error" && !msg.text().includes("Failed to load resource")) errors.push(msg.text()); });
  page.on("pageerror", (e) => errors.push("pageerror: " + e.message));

  console.log("== Mo trang module 02 ==");
  await page.goto(`${BASE}/vi/modules/02-schema-alignment/index.html`, { waitUntil: "networkidle0", timeout: 30000 });

  // cho SQLBank.init chay xong (fetch + wasm load)
  await page.waitForSelector("#sb-mount-m02 .sb-main", { timeout: 20000 });
  console.log("OK: SQL sandbox shell da render");

  const sidebarCount = await page.$$eval("#sb-mount-m02 .sb-item", els => els.length);
  console.log(`OK: sidebar sandbox co ${sidebarCount} cau (ky vong 50)`);
  if (sidebarCount !== 50) throw new Error(`Sidebar sandbox sai so luong: ${sidebarCount}`);

  // chay thu referenceSql cua cau dang mo (m02-001) bang nut "Xem loi giai mau" roi copy vao editor roi Cham diem
  await page.click("#sb-mount-m02 #sb-show-sol");
  const solText = await page.$eval("#sb-mount-m02 .sb-sol", el => el.textContent);
  console.log("OK: lay duoc loi giai mau:", solText.slice(0, 60));

  await page.evaluate((sql) => {
    const ta = document.querySelector("#sb-mount-m02 #sb-editor");
    ta.value = sql;
  }, solText);
  await page.click("#sb-mount-m02 #sb-grade");
  await page.waitForFunction(() => document.querySelector("#sb-mount-m02 #sb-out p.ok, #sb-mount-m02 #sb-out p.no"), { timeout: 5000 });
  const gradeMsg = await page.$eval("#sb-mount-m02 #sb-out p", el => el.textContent);
  console.log("OK: ket qua cham diem cau dau:", gradeMsg);
  if (!gradeMsg.includes("Chính xác")) throw new Error("Cham sai: referenceSql cua chinh cau hoi lai khong duoc cham DUNG");

  // thu 1 cau SAI co chu dich de chac chan grading phan biet dung/sai
  await page.evaluate(() => { document.querySelector("#sb-mount-m02 #sb-editor").value = "SELECT 1;"; });
  await page.click("#sb-mount-m02 #sb-grade");
  await page.waitForFunction(() => document.querySelector("#sb-mount-m02 #sb-out p.no, #sb-mount-m02 #sb-out p.ok"), { timeout: 5000 });
  const gradeMsg2 = await page.$eval("#sb-mount-m02 #sb-out p", el => el.textContent);
  console.log("OK: cham cau SAI co chu dich:", gradeMsg2);
  if (!gradeMsg2.includes("Chưa khớp")) throw new Error("Grading khong phat hien duoc cau sai ro ret 'SELECT 1'");

  // kiem tra Bank 150 (thuc te 96) cau: mo bank.html
  console.log("== Mo trang bank.html ==");
  await page.goto(`${BASE}/vi/modules/02-schema-alignment/bank.html`, { waitUntil: "networkidle0", timeout: 20000 });
  await page.waitForSelector(".bk-item", { timeout: 10000 });
  const bkItemCount = await page.$$eval(".bk-item", els => els.length);
  console.log(`OK: bank hien thi ${bkItemCount} cau/trang (ky vong 15/trang)`);
  if (bkItemCount !== 15) throw new Error(`Bank page size sai: ${bkItemCount}`);

  // bam 1 dap an dung thu
  await page.evaluate(() => {
    const item = document.querySelector('.bk-item[data-li="0"]');
    item.__correctIdxForTest = true;
  });
  // doc du lieu cau dau de biet dap an dung roi bam dung option
  const firstQCorrectText = await page.evaluate(() => {
    const item = document.querySelector('.bk-item[data-li="0"]');
    const opts = [...item.querySelectorAll(".bk-opt")];
    return opts.length;
  });
  console.log("OK: cau dau co", firstQCorrectText, "phuong an");
  // bam option dau tien (du dung hay sai, chi test co phan hoi + giai thich hien ra)
  await page.click('.bk-item[data-li="0"] .bk-opt');
  await page.waitForSelector('.bk-item[data-li="0"] .bk-explain:not([hidden])', { timeout: 5000 });
  const explainText = await page.$eval('.bk-item[data-li="0"] .bk-explain', el => el.textContent);
  console.log("OK: bam dap an -> hien giai thich:", explainText.slice(0, 50));

  console.log("\n=== CONSOLE ERRORS ===", errors.length ? errors : "(khong co)");
  if (errors.length) throw new Error("Co console error, xem log tren");

  console.log("\n✅ TAT CA KIEM TRA LAYER-2 PASS");
  await browser.close();
})().catch((e) => { console.error("❌ TEST FAIL:", e); process.exit(1); });
