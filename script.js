document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.querySelector('#reports-table tbody');

function extractDate(filename) {
        const decodedName = decodeURIComponent(filename);

        // Format 1: WG-JJJJMMTT- (8 Ziffern, direkt gefolgt von einem Bindestrich)
        let match = decodedName.match(/WG-(\d{4})(\d{2})(\d{2})-/);
        if (match) {
            return `${match[3]}.${match[2]}.${match[1]}`;
        }

        // Format 2: WG-JJJJ-MM-TTT... (ISO-Timestamp mit Bindestrichen, "T" folgt)
        match = decodedName.match(/WG-(\d{4})-(\d{2})-(\d{2})T/);
        if (match) {
            return `${match[3]}.${match[2]}.${match[1]}`;
        }

        // Format 3: WG-<Unix-Timestamp in Millisekunden> (10-13 Ziffern, altes Format)
        match = decodedName.match(/WG-(\d{10,13})(?:\.html)?$/);
        if (match) {
            const d = new Date(parseInt(match[1], 10));
            if (!isNaN(d.getTime())) {
                const dd = String(d.getDate()).padStart(2, '0');
                const mm = String(d.getMonth() + 1).padStart(2, '0');
                return `${dd}.${mm}.${d.getFullYear()}`;
            }
        }

        return "Unbekannt";
    }

    try {
        // Lädt die durch generate_index.js erzeugte JSON-Liste
        const response = await fetch('data/index.json');
        
        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen der index.json (HTTP ${response.status})`);
        }

        const uniqueReports = await response.json();

        // Tabelle befüllen
        uniqueReports.forEach(filename => {
            const decodedFilename = decodeURIComponent(filename);
            const row = document.createElement('tr');

            // Datum
            const dateCell = document.createElement('td');
            dateCell.textContent = extractDate(decodedFilename);
            row.appendChild(dateCell);

            // Dateiname mit Link zur Subseite
            const filenameCell = document.createElement('td');
            const link = document.createElement('a');
            link.href = `data/${filename}`;
            link.textContent = decodedFilename;
            link.target = '_blank'; 
            filenameCell.appendChild(link);
            row.appendChild(filenameCell);

            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error("Fehler beim Laden der Berichte aus dem data/ Verzeichnis:", error);
        
        const errorRow = document.createElement('tr');
        const errorCell = document.createElement('td');
        errorCell.colSpan = 2;
        errorCell.style.color = "red";
        errorCell.textContent = "Konnte das Verzeichnis 'data/' nicht auslesen. Stellen Sie sicher, dass das Webserver-Directory-Listing aktiv ist oder eine Index-Datei vorliegt.";
        tableBody.appendChild(errorRow);
    }
});
