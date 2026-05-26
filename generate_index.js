const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');
const outputFile = path.join(dataDir, 'index.json');

try {
    // Falls das Verzeichnis nicht existiert, abbrechen (vermeidet Fehler in leeren Repos)
    if (!fs.existsSync(dataDir)) {
        console.warn(`Verzeichnis ${dataDir} existiert nicht. Keine index.json generiert.`);
        process.exit(0);
    }

    // Lese alle Dateien im data-Verzeichnis und filtere nach .html
    const files = fs.readdirSync(dataDir);
    const htmlFiles = files.filter(file => file.endsWith('.html'));

    // Schreibe die Liste als JSON-Datei zurück in den data/ Ordner
    fs.writeFileSync(outputFile, JSON.stringify(htmlFiles, null, 2));
    
    console.log(`Erfolgreich index.json mit ${htmlFiles.length} Berichten generiert.`);
} catch (err) {
    console.error('Fehler bei der Generierung der index.json:', err);
    process.exit(1);
}