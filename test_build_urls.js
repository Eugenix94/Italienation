const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

function findUrlsInDist(dir) {
    let results = [];
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            results = results.concat(findUrlsInDist(filePath));
        } else if (file.endsWith('.js') || file.endsWith('.html') || file.endsWith('.json') || file.endsWith('.css')) {
            const content = fs.readFileSync(filePath, 'utf8');
            const urlRegex = /(https?:\/\/[^\s"'`<>]+)/g;
            let match;
            while ((match = urlRegex.exec(content)) !== null) {
                let url = match[1];
                if (url.endsWith('\\')) url = url.slice(0, -1);
                if (url.endsWith(')')) url = url.slice(0, -1);
                if (url.endsWith(']')) url = url.slice(0, -1);
                if (url.endsWith(',')) url = url.slice(0, -1);
                if (url.endsWith('.')) url = url.slice(0, -1);
                results.push({ url, file: filePath });
            }
        }
    }
    return results;
}

const distDir = path.join(__dirname, 'frontend', 'dist');
if (!fs.existsSync(distDir)) {
    console.error("dist dir not found");
    process.exit(1);
}

const allUrls = findUrlsInDist(distDir);
const uniqueUrls = new Map();
for (const u of allUrls) {
    if (!uniqueUrls.has(u.url)) {
        uniqueUrls.set(u.url, new Set());
    }
    uniqueUrls.get(u.url).add(u.file);
}

console.log(`Found ${uniqueUrls.size} unique URLs to check.`);

// Ignore list for common XML namespaces, localhost, github schema
const ignoreList = [
    'http://www.w3.org/',
    'http://localhost',
    'https://localhost',
    'http://127.0.0.1',
    'https://www.w3.org',
    'https://vite.dev',
    'https://react.dev'
];

async function checkUrl(url) {
    for (const ignore of ignoreList) {
        if (url.startsWith(ignore)) return { url, status: 'IGNORED' };
    }
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);
        
        const response = await fetch(url, {
            method: 'HEAD',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        
        if (response.ok) return { url, status: response.status };
        
        // Retry with GET if HEAD fails (some servers block HEAD)
        const getController = new AbortController();
        const getTimeoutId = setTimeout(() => getController.abort(), 10000);
        const getResponse = await fetch(url, {
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Range': 'bytes=0-100'
            },
            signal: getController.signal
        });
        clearTimeout(getTimeoutId);
        return { url, status: getResponse.status };
    } catch (e) {
        return { url, status: e.name === 'AbortError' ? 'TIMEOUT' : e.message };
    }
}

async function run() {
    let broken = [];
    let timeouts = [];
    
    // Batch processing to not overload DNS
    const urlsArray = Array.from(uniqueUrls.keys());
    const batchSize = 10;
    
    for (let i = 0; i < urlsArray.length; i += batchSize) {
        const batch = urlsArray.slice(i, i + batchSize);
        const results = await Promise.all(batch.map(checkUrl));
        
        for (const res of results) {
            if (res.status === 'IGNORED') continue;
            
            if (res.status === 404 || res.status === 400 || res.status === 403 || res.status === 500) {
                console.log(`[BROKEN ${res.status}] ${res.url}`);
                for (const file of uniqueUrls.get(res.url)) {
                    console.log(`   -> Found in: ${file.replace(__dirname, '')}`);
                }
                broken.push(res);
            } else if (res.status === 'TIMEOUT' || typeof res.status === 'string') {
                if (res.status !== 'TIMEOUT' && !res.status.includes('fetch failed')) {
                    timeouts.push(res);
                }
            }
        }
        process.stdout.write(`Checked ${Math.min(i + batchSize, urlsArray.length)}/${urlsArray.length}\r`);
    }
    
    console.log('\n--- SCAN COMPLETE ---');
    console.log(`Total Broken (404/Error): ${broken.length}`);
    if (broken.length === 0) {
        console.log("No 404s found in the production build!");
    }
}

run();
