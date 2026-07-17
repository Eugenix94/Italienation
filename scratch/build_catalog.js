const { execSync } = require('child_process');
const path = require('path');

console.log("Delegating catalog rebuild to high-precision Python direct links builder...");
try {
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
    const scriptPath = path.join(__dirname, '..', 'scripts', 'rebuild_catalogs_with_direct_links.py');
    execSync(`${py} "${scriptPath}"`, { stdio: 'inherit' });
} catch (err) {
    console.error("Failed to run python direct links builder:", err);
}
