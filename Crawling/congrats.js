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

    await page.goto('https://www.kpopmap.com/calendar/upcoming-festival-awards-lineup-results/', {timeout: 90000});
    const links = await page.$$eval('.post-data h3 a', links =>links.map(link=>link.href));//해당 페이지에 일치하는 모든 요소 선택 
    //console.log(links)
    const data=[];

    for(let link of links){
        await page.goto(link);
        
        const title = await page.$eval('.post-header > h1', title=>title.textContent);
        const context= await page.$eval('.article> h2', context=>context.textContent.trim()); //해당 페이지에 일치하는 첫번째 요소 선택
        const info = await page.$eval('.article > h2+p', info=>info.textContent.trim());
        data.push({Title: title, Info: info});
    console.log(`Title: ${title}`);
    console.log(`Context: ${context}`);
    console.log(`Info: ${info}`);
    console.log('-----------------------------------------------------------------');
    }
    await browser.close();
    const worksheet = XLSX.utils.json_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
    XLSX.writeFile(workbook, 'schedule:congrats.xlsx');
    
})();

    // h2 밑에 바로 있는 것들은 출력 ok/
    //1. h2~p / h2~p 인 경우 
    //2. div 밑에 있는 겨웅 
    //3. h2+p 이고, if <p> <strong > 있는 거 제외 
    
