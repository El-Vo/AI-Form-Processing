# AI-Form-Processing
Forschungsprojekt zur automatisierten Bearbeitung von Formularen öffentlicher Institutionen via LLM-Agenten (Projektseminar SoSe 2026).
**Projektmitglieder:** Elias

## Setup & Voraussetzungen
Das Projekt nutzt **LangGraph** zur Orchestrierung der Workflow-Schritte und den Paketmanager **uv**.

- `uv` installieren: [Offizielle Anleitung](https://docs.astral.sh/uv/getting-started/installation/)

**Hinweis:** `uv` kümmert sich automatisch um die richtige Python-Version (3.12) und alle Abhängigkeiten. Ggf. Terminal nach der Installation neu starten.

Für die Installation der Abhängigkeiten:
```bash
uv sync
```

## LLM Konfiguration (Mistral, OpenAI-kompatibel)

```bash
setx OPENAI_API_KEY "<dein-mistral-api-key>"
setx OPENAI_BASE_URL "https://api.mistral.ai/v1"
setx OPENAI_MODEL "mistral-small"
```

## Projekt (CLI) starten
In dem Projekt ist ein Workflow für die Wohngeldberechnung implementiert.
Das CLI Tool erlaubt es, Mocks einzulesen und im Terminal den Ablauf (inkl. Human-in-the-Loop Interaktionen) interaktiv nachzuvollziehen.

Führe im Projektverzeichnis Folgendes aus:

```bash
uv run python -m src.wohngeld.cli
```

Hierbei wirst du im Terminal aufgefordert, eine Mock-Datei auszuwählen und an bestimmten Unterbrechungspunkten Entscheidungen zu treffen.
