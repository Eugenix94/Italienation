const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'src/views/UnifiedHome.jsx');
let file = fs.readFileSync(filePath, 'utf8');

// Replace the wrapper
file = file.replace('className="w-full space-y-40"', 'className="w-full flex flex-col gap-24"');

// First remove all existing dividers
file = file.replace(/\s*<div className="border-t border-zinc-800\/50 my-8" \/>/g, '');

// Now inject a nice divider between every section
// Match </section> followed by <section
const divider = `

                <div className="w-full flex items-center justify-center py-2 opacity-60">
                  <div className="w-1/2 h-px bg-gradient-to-r from-transparent via-zinc-700 to-transparent"></div>
                </div>

                `;
file = file.replace(/<\/section>\s+<section/g, '</section>' + divider + '<section');

fs.writeFileSync(filePath, file);
console.log('Replaced successfully');
