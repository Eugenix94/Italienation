const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '../frontend/src/assets/originLinks.json');
const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

for (const key in data) {
    if (key.startsWith('eury_') && data[key].includes('dati.istruzione.it')) {
        data[key] = 'https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview';
    }
}

fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
console.log('Successfully updated Eurydice links.');
