const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log('PAGE LOG ERROR:', msg.text());
    } else {
      console.log('PAGE LOG:', msg.text());
    }
  });

  page.on('pageerror', error => {
    console.log('PAGE ERROR:', error.message);
  });

  page.on('requestfailed', request => {
    console.log('REQUEST FAILED:', request.url(), request.failure().errorText);
  });

  try {
    console.log('Navigating to http://localhost:5173/Italienation/ ...');
    await page.goto('http://localhost:5173/Italienation/', { waitUntil: 'networkidle2' });
    console.log('Page loaded successfully');
  } catch (error) {
    console.error('Failed to load page:', error);
  }

  await browser.close();
})();
