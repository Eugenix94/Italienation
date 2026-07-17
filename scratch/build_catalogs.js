const { execSync } = require('child_process');
const path = require('path');

console.log("Delegating catalog rebuild to high-precision Python direct links builder...");
try {
    // Try finding python executables
    let py = "python";
    try {
        execSync('python --version', { stdio: 'ignore' });
    } catch {
        try {
            py = '"C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"';
            execSync(`${py} --version`, { stdio: 'ignore' });
        } catch {
            py = 'py';
        }
    }
Object.entries(cats).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`  ${k}: ${v}`));
