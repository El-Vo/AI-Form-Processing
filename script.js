document.addEventListener('DOMContentLoaded', async () => {
    const endTableBody = document.querySelector('#end-reports-table tbody');
    const interimTableBody = document.querySelector('#interim-reports-table tbody');

    // Extrahiert das Datum aus Dateinamen wie:
    // - "WG-20260526-I1FQEY.html"          (aktuelles Format: JJJJMMTT-ZUFALL)
    // - "WG-2026-07-25T20:06:41.755Z.html" (ISO-Timestamp, alt)
    // - "WG-1781617513200.html"            (Unix-Timestamp in ms, alt)
    function extractDate(filename) {
        const decodedName = decodeURIComponent(filename);

        let match = decodedName.match(/WG-(\d{4})(\d{2})(\d{2})-/);
        if (match) {
            return `${match[3]}.${match[2]}.${match[1]}`;
        }

        match = decodedName.match(/WG-(\d{4})-(\d{2})-(\d{2})T/);
        if (match) {
            return `${match[3]}.${match[2]}.${match[1]}`;
        }

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

    // Zwischenberichte heißen immer "zwischenbericht_{caseId}_{runde}.html"
    function isInterimReport(filename) {
        return filename.startsWith('zwischenbericht_');
    }

    function renderRow(tbody, rawFilename, decodedFilename) {
        const row = document.createElement('tr');

        const dateCell = document.createElement('td');
        dateCell.textContent = extractDate(decodedFilename);
        row.appendChild(dateCell);

        const filenameCell = document.createElement('td');
        const link = document.createElement('a');
        link.href = `data/${rawFilename}`;
        link.textContent = decodedFilename;
        link.target = '_blank';
        filenameCell.appendChild(link);
        row.appendChild(filenameCell);

        tbody.appendChild(row);
    }

    try {
        const response = await fetch('data/index.json');

        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen der index.json (HTTP ${response.status})`);
        }

        const uniqueReports = await response.json();

        uniqueReports.forEach(filename => {
            const decodedFilename = decodeURIComponent(filename);
            if (isInterimReport(decodedFilename)) {
                renderRow(interimTableBody, filename, decodedFilename);
            } else {
                renderRow(endTableBody, filename, decodedFilename);
            }
        });

    } catch (error) {
        console.error("Fehler beim Laden der Berichte aus dem data/ Verzeichnis:", error);

        const errorRow = document.createElement('tr');
        const errorCell = document.createElement('td');
        errorCell.colSpan = 2;
        errorCell.style.color = "red";
        errorCell.textContent = "Konnte das Verzeichnis 'data/' nicht auslesen. Stellen Sie sicher, dass das Webserver-Directory-Listing aktiv ist oder eine Index-Datei vorliegt.";
        endTableBody.appendChild(errorRow);
    }
});
