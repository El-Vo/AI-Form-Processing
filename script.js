document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.querySelector('#reports-table tbody');

    // Hilfsfunktion zum Extrahieren des Datums aus Dateinamen wie "...WG-20260526..."
    function extractDate(filename) {
        // Dekodiert URL-Zeichenfolgen (%20 zu Leerzeichen), um den Regex sicher anzuwenden
        const decodedName = decodeURIComponent(filename);
        const match = decodedName.match(/WG-(\d{4})(\d{2})(\d{2})/);
        if (match) {
            return `${match[3]}.${match[2]}.${match[1]}`;
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