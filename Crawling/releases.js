const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const XLSX=require('xlsx');


(async () => {
    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
    await page.setViewport({
      width: 1336,
      height: 768
    });

    await page.goto('https://www.kpopmap.com/update-march-2023-k-pop-comeback-schedule/', {timeout: 60000});

    const content = await page.content();
    const $ = cheerio.load(content);
    const lists = $("div.article");
    const data = [['Date', 'Release']];
    
    lists.each((index, list) => {
        const when = $(list).find("h2 > strong").text().trim();  
        const whenArr = when.match(/\w+\.\s\d+/g);
        const formattedWhen = whenArr.map(w => w.replace(/\./, '. '));      
        $(list).find('.article > h3 + p').each((i, elem) => {
            const text=$(elem).text().trim().replace("`", '');
            if(i<formattedWhen.length){
                data.push([formattedWhen[i], text]);
            }else{
                data.push([`April. ${i-formattedWhen.length+1}`, text]);
            }
    
        });
    });
    await browser.close();
    
    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
    XLSX.writeFile(workbook, 'schedule:release.xlsx');
    
})();


