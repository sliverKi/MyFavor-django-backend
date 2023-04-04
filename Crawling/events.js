const puppeteer = require('puppeteer')
const cheerio = require('cheerio') 
const XLSX=require('xlsx');

(async () => {
    const browser= await puppeteer.launch({headless : false});
    const page=await browser.newPage();
    await page.setViewport({
        width: 1336,
        height: 768
    });

    await page.goto('https://www.kpopmap.com/calendar/concert-fanmeeting/', {timeout: 90000});

    const links = await page.$$eval('.post-data h3 a', links =>links.map(link=>link.href));//해당 페이지에 일치하는 모든 요소 선택 
    //console.log(links)
    
    const data=[];
    
    for(let link of links){
        await page.goto(link);

        const title= await page.$eval('.post-header > h1', title=>title.textContent.trim()); //해당 페이지에 일치하는 첫번째 요소 선택
        let info = await page.$eval('.article',content=> {

            const h2Info=content.querySelector('h2+p');
            const h3Info=content.querySelector('h3+p');
            if (h2Info) return h2Info.textContent.trim();
            if (h3Info) return h3Info.textContent.trim();
            return ''; 
        });
        data.push({Title: title, Info: info});
    //console.log(`Title: ${title}`);
    //console.log(`Info: ${info}`);
    ///console.log('-----------------------------------------------------------------');
    }
    await browser.close();
    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
    XLSX.writeFile(workbook, 'schedule:event.xlsx');
})();

