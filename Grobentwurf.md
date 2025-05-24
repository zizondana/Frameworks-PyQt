## Grobentwurf: To‑Do Listen Verwaltungstool

### Einleitung

In diesem Projekt entwickeln wir ein einfaches und benutzerfreundliches Tool zur Verwaltung täglicher Aufgaben. Der Anwender kann Aufgaben hinzufügen, bearbeiten, löschen und ihren Status visuell verfolgen.

### Gesamtziele

* Bereitstellung einer minimalen, intuitiven Benutzeroberfläche mit PyQt5 und Qt Designer
* Unterstützung der grundlegenden CRUD-Operationen (Anlegen, Lesen, Aktualisieren, Löschen) für Aufgaben
* Speichern und Laden der Aufgaben in einer **SQLite-Datenbank**
* Darstellung des Erledigt‑/Unerledigt‑Status mittels Checkboxen
* Live-Suche zur schnellen Aufgabenfilterung

### Hauptfunktionen

1. **Aufgabe hinzufügen**: Eingabe des Aufgabentitels über einen Dialog
2. **Aufgabe bearbeiten**: Änderung des Titels einer bestehenden Aufgabe
3. **Aufgabe löschen**: Entfernen der ausgewählten Aufgabe aus der Liste
4. **Status umschalten**: Checkbox, um den Erledigt‑Status zu setzen
5. **Suche**: Live‑Filterung der Aufgabenliste anhand von Texteingabe
6. **CSV‑Export**: Export der Aufgabenliste als CSV-Datei
7. **Gantt‑Diagramm**: Einfache Gantt‑Visualisierung der Aufgaben

### Projektstruktur

```text
.
├── .venv/                  # Virtuelle Umgebung
├── gui/                    # UI-Design-Datei (mainwindow.ui)
├── logic/                  # Programm-Logik (task_manager.py)
├── data/                   # Persistente Datenspeicherung (tasks.db)
├── main.py                 # Anwendungseinstiegspunkt
├── requirements.txt        # Python-Abhängigkeiten
├── README.md               # Projektdokumentation
└── LICENSE                 # MIT-Lizenz
```

**Zusammenfassung**: Dieser Grobentwurf fasst auf einer halben Seite die Projektidee, Hauptfunktionen und Struktur zusammen und dient als Grundlage für die erste Woche der Entwicklung.
