# To-Do App (PyQt6 Version)

Ein einfaches Aufgabenverwaltungstool mit moderner Benutzeroberfläche in **PyQt6** und Datenpersistenz über **SQLite**.

## Features

- Aufgaben erstellen, bearbeiten, löschen
- Aufgabenstatus (erledigt / offen) per Checkbox ändern
- Live-Suche nach Titel
- Export der Aufgabenliste als CSV
- Gantt-Diagramm zur Visualisierung (mit matplotlib)

## Installation

1. Repository klonen:
```bash
git clone <repository-url>
cd <projektordner>
```

2. Virtuelle Umgebung erstellen & aktivieren:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Start der Anwendung

```bash
python main.py
```

## Projektstruktur

```
.
├── data/                    # SQLite-Datenbank (tasks.db)
├── gui/                     # UI-Design-Datei (mainwindow.ui)
├── logic/                   # Programmlogik (task_manager.py)
├── tests/                   # Unit-Tests (test_task_manager.py)
├── main.py                  # Anwendungseinstiegspunkt
├── requirements.txt         # Abhängigkeiten
└── README.md                # Diese Datei
```

## Technologien

- PyQt6 für die GUI
- SQLite für Datenspeicherung
- matplotlib für Gantt-Chart
- pytest für automatisierte Tests

## Lizenz

Dieses Projekt verwendet die MIT-Lizenz. Siehe `LICENSE` für Details.

---

📌 Hinweis: Dieses Projekt ist kompatibel mit **Python 3.10+** und verwendet ausschließlich **SQLite** (kein JSON mehr).