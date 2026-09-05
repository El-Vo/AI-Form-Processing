document.addEventListener('DOMContentLoaded', async () => {
    const finalTableBody = document.querySelector('#final-reports-table tbody');
    const testTableBody = document.querySelector('#test-reports-table tbody');
    const tempTableBody = document.querySelector('#temp-reports-table tbody');

    let allReports = []; // { rawFilename, decodedFilename, type, dateDisplay, dateValue }
    const sortState = {
        final: { column: 'date', direction: 'desc' },
        test: { column: 'date', direction: 'desc' },
        temp: { column: 'date', direction: 'desc' }
    };

    // Erkennt das Datum aus Dateinamen wie:
    // - "WG-20260526-I1FQEY.html"          (aktuelles Format: JJJJMMTT-ZUFALL)
    // - "WG-2026-07-25T20:06:41.755Z.html" (ISO-Timestamp, alt)
    // - "WG-1781617513200.html"            (Unix-Timestamp in ms, alt)
    function parseReportDate(decodedFilename) {
        let match = decodedFilename.match(/WG-(\d{4})(\d{2})(\d{2})-/);
        if (match) {
            const [, y, m, d] = match;
            return { display: `${d}.${m}.${y}`, value: new Date(`${y}-${m}-${d}`).getTime() };
        }

        match = decodedFilename.match(/WG-(\d{4})-(\d{2})-(\d{2})T/);
        if (match) {
            const [, y, m, d] = match;
            return { display: `${d}.${m}.${y}`, value: new Date(`${y}-${m}-${d}`).getTime() };
        }

        match = decodedFilename.match(/WG-(\d{10,13})(?:\.html)?$/);
        if (match) {
            const ts = parseInt(match[1], 10);
            const d = new Date(ts);
            if (!isNaN(d.getTime())) {
                const dd = String(d.getDate()).padStart(2, '0');
                const mm = String(d.getMonth() + 1).padStart(2, '0');
                return { display: `${dd}.${mm}.${d.getFullYear()}`, value: d.getTime() };
            }
        }

        return { display: 'Unbekannt', value: null };
    }

    function getFilterValues() {
        const search = document.getElementById('search-input').value.trim().toLowerCase();
        const fromStr = document.getElementById('date-from').value;
        const toStr = document.getElementById('date-to').value;
        return {
            search,
            from: fromStr ? new Date(fromStr + 'T00:00:00').getTime() : null,
            to: toStr ? new Date(toStr + 'T23:59:59').getTime() : null
        };
    }

    function matchesFilter(report, filters) {
        if (filters.search) {
            const haystack = (report.decodedFilename + ' ' + report.dateDisplay).toLowerCase();
            if (!haystack.includes(filters.search)) return false;
        }
        if (filters.from !== null && (report.dateValue === null || report.dateValue < filters.from)) return false;
        if (filters.to !== null && (report.dateValue === null || report.dateValue > filters.to)) return false;
        return true;
    }

    function sortReports(reports, sort) {
        const sorted = [...reports];
        sorted.sort((a, b) => {
            if (sort.column === 'date') {
                // "Unbekannt"-Daten immer ans Ende, unabhängig von der Richtung
                if (a.dateValue === null && b.dateValue === null) return 0;
                if (a.dateValue === null) return 1;
                if (b.dateValue === null) return -1;
                return sort.direction === 'asc' ? a.dateValue - b.dateValue : b.dateValue - a.dateValue;
            } else {
                const av = a.decodedFilename.toLowerCase();
                const bv = b.decodedFilename.toLowerCase();
                if (av < bv) return sort.direction === 'asc' ? -1 : 1;
                if (av > bv) return sort.direction === 'asc' ? 1 : -1;
                return 0;
            }
        });
        return sorted;
    }

    function updateSortIndicators(tableId, sort) {
        document.querySelectorAll(`#${tableId} th.sortable`).forEach(th => {
            const indicator = th.querySelector('.sort-indicator');
            indicator.textContent = th.dataset.sort === sort.column
                ? (sort.direction === 'asc' ? '\u25b2' : '\u25bc')
                : '';
        });
    }

    function renderTable(type, tbody) {
        const filters = getFilterValues();
        let reports = allReports.filter(r => r.type === type && matchesFilter(r, filters));
        reports = sortReports(reports, sortState[type]);

        tbody.innerHTML = '';

        if (!reports.length) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.colSpan = 2;
            cell.style.fontStyle = 'italic';
            cell.style.color = '#6c757d';
            cell.textContent = 'Keine Berichte gefunden.';
            row.appendChild(cell);
            tbody.appendChild(row);
            return;
        }

        reports.forEach(r => {
            const row = document.createElement('tr');

            const dateCell = document.createElement('td');
            dateCell.textContent = r.dateDisplay;
            row.appendChild(dateCell);

            const filenameCell = document.createElement('td');
            const link = document.createElement('a');
            link.href = `data/${r.rawFilename}`;
            link.textContent = r.decodedFilename;
            link.target = '_blank';
            filenameCell.appendChild(link);
            row.appendChild(filenameCell);

            tbody.appendChild(row);
        });
    }

    function renderAll() {
        renderTable('final', finalTableBody);
        renderTable('test', testTableBody);
        renderTable('temp', tempTableBody);
    }

    function setupSortHandlers(tableId, type) {
        document.querySelectorAll(`#${tableId} th.sortable`).forEach(th => {
            th.addEventListener('click', () => {
                const column = th.dataset.sort;
                const current = sortState[type];
                if (current.column === column) {
                    current.direction = current.direction === 'asc' ? 'desc' : 'asc';
                } else {
                    current.column = column;
                    current.direction = column === 'date' ? 'desc' : 'asc';
                }
                updateSortIndicators(tableId, current);
                renderAll();
            });
        });
        updateSortIndicators(tableId, sortState[type]);
    }

    setupSortHandlers('final-reports-table', 'final');
    setupSortHandlers('test-reports-table', 'test');
    setupSortHandlers('temp-reports-table', 'temp');

    ['search-input', 'date-from', 'date-to'].forEach(id => {
        document.getElementById(id).addEventListener('input', renderAll);
    });
    document.getElementById('reset-filters').addEventListener('click', () => {
        document.getElementById('search-input').value = '';
        document.getElementById('date-from').value = '';
        document.getElementById('date-to').value = '';
        renderAll();
    });

    try {
        const response = await fetch('data/index.json');

        if (!response.ok) {
            throw new Error(`Fehler beim Abrufen der index.json (HTTP ${response.status})`);
        }

        const uniqueReports = await response.json();

        allReports = uniqueReports.map(filename => {
            const decodedFilename = decodeURIComponent(filename);
            const { display, value } = parseReportDate(decodedFilename);
            
            // Bestimme den Typ des Berichts
            let type = 'temp'; // Standard: Temporäre Berichte
            
            if (decodedFilename.startsWith('final_')) {
                type = 'final';
            } else if (decodedFilename.startsWith('metabericht_') || 
                       decodedFilename.includes('Metabericht') || 
                       decodedFilename.includes('Testbericht') ||
                       decodedFilename.startsWith('meta_')) {
                type = 'test';
            } else if (decodedFilename.startsWith('TF-')) {
                // TF-*.html Dateien werden nicht angezeigt (nur über Metabericht verlinkt)
                return null;
            }
            
            return {
                rawFilename: filename,
                decodedFilename,
                type,
                dateDisplay: display,
                dateValue: value
            };
        }).filter(r => r !== null && r.rawFilename !== '.html'); // Filtere null-Einträge (TF-*.html) und leere Dateien heraus

        renderAll();

    } catch (error) {
        console.error("Fehler beim Laden der Berichte aus dem data/ Verzeichnis:", error);

        const errorRow = document.createElement('tr');
        const errorCell = document.createElement('td');
        errorCell.colSpan = 2;
        errorCell.style.color = "red";
        errorCell.textContent = "Konnte das Verzeichnis 'data/' nicht auslesen. Stellen Sie sicher, dass das Webserver-Directory-Listing aktiv ist oder eine Index-Datei vorliegt.";
        finalTableBody.appendChild(errorRow);
    }
});
