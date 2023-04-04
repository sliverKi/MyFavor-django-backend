const puppeteer = require('puppeteer');
const XLSX=require('xlsx');
(async () => {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();
  await page.setViewport({
    width: 1336,
    height: 768
  });
  await page.goto('https://www.kpopmap.com/kpop-member-profile/red-velvet/');

  const images = await page.$$eval(
      '.profile-item .img-wrap img', 
      images => images.map(image => image.src)
  );
  console.log(images);

  await browser.close();

  const wb=XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(images.map(url=>[url]));
  XLSX.utils.book_append_sheet(wb, ws, 'red-velvet-Members');
  XLSX.writeFile(wb, 'red-velvet.xlsx');
})();
