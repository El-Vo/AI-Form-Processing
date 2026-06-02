# AI-Form-Processing
Forschungsprojekt zur automatisierten Bearbeitung von Formularen öffentlicher Institutionen via LLM-Agenten (Projektseminar SoSe 2026).

**Projektmitglieder:** Elias (schreibt euch gern dazu!)

## n8n Dashboard

Dieses Repository stellt eine statische Seite über GitHub Pages bereit, die einen Überblick über vergangene Berichte bietet. Wir verwenden die Seite, um Kennzahlen über unseren Workflow zu tracken.

### Ablauf

- n8n PROD Workflow wird ausgeführt.
- Das Schlusserzeugnis (HTML-Bericht) wird automatisch auf den Branch `n8n-workflow-results` gepusht.
- Mit manuellem Ausführen der n8n-Node "Update Website" am Ende des Workflows werden die Änderungen im `data/` Verzeichnis auf dem obigen Branch auf `main` gepushed (außerdem wird `n8n-workflow-results` auf `main` rebased). Siehe dazu auch die GitHub Action [import-data.yml](.github/workflows/import-data.yml).
- Mit jedem Push auf `main` wird die `index.json` generiert und das GitHub Pages Deployment angestoßen. Siehe dazu auch die Action [pages.yml](.github/workflows/pages.yml).

### Hinweise

- Nur auf `n8n-workflow-results` pushen, wenn unsere Testdaten angepasst werden sollen.
- Die erstellte GitHub Pages Seite wird statisch ausgeliefert; es gibt kein Backend oder Datenbank. Unsere Informationen stammen ausschließlich aus dem `data/` Verzeichnis und den HTML-Dateien, die von `index.json` indexiert werden.
- Bibliotheken oder Erweiterungen zur Dashboard-Erstellung müssen clientseitig eingebunden werden, damit sie im Browser "live" gerendert werden können (z. B. für Filter, Visualisierungen, etc.).