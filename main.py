import sys
import csv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QHBoxLayout, QProgressBar, QDialog, QFormLayout,
    QComboBox, QDateEdit, QScrollArea, QFileDialog, QCalendarWidget
)
from PyQt6.QtCore import Qt, QDate
from logic.task_manager import TaskManager
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import datetime

class ModernTabApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Modern Productivity App")
        self.setMinimumSize(1000, 650)
        self.manager = TaskManager("data/tasks.db")
        self.dark_mode = False
        self.tasks = []

        self.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar::tab {
                background: #2e8b57;
                color: white;
                padding: 10px 20px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #3cb371;
            }
            QMainWindow {
                background-color: #f3f3f3;
            }
            QLabel {
                font-size: 18px;
            }
        """)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.init_aufgaben_tab()
    def init_aufgaben_tab(self):
        self.aufgaben_tab = QWidget()
        layout = QVBoxLayout(self.aufgaben_tab)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Aufgabe suchen...")
        self.search_input.textChanged.connect(self.apply_filter)
        layout.addWidget(self.search_input)

        self.task_area = QScrollArea()
        self.task_area.setWidgetResizable(True)
        self.task_list_container = QWidget()
        self.task_list_layout = QVBoxLayout(self.task_list_container)
        self.task_area.setWidget(self.task_list_container)
        layout.addWidget(self.task_area)

        btn_row = QHBoxLayout()

        self.btn_add = QPushButton("+ Hinzufügen")
        self.btn_add.clicked.connect(self.add_task)
        btn_row.addWidget(self.btn_add)

        self.btn_export = QPushButton("📤 Exportieren")
        self.btn_export.clicked.connect(self.export_tasks)
        btn_row.addWidget(self.btn_export)

        layout.addLayout(btn_row)
        self.refresh_task_list()

        self.tabs.addTab(self.aufgaben_tab, "🗂 Aufgaben")

        self.init_calendar_tab()
        self.init_gantt_tab()
        self.init_stats_tab()
        self.init_settings_tab()

    def init_calendar_tab(self):
        self.calendar_tab = QWidget()
        layout = QVBoxLayout(self.calendar_tab)

        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.selectionChanged.connect(self.update_calendar_tasks)
        layout.addWidget(self.calendar_widget)

        self.calendar_task_list = QVBoxLayout()
        layout.addLayout(self.calendar_task_list)

        self.tabs.addTab(self.calendar_tab, "📅 Kalender")

    def init_gantt_tab(self):
        self.gantt_tab = QWidget()
        gantt_layout = QVBoxLayout(self.gantt_tab)

        self.gantt_figure = Figure()
        self.gantt_canvas = FigureCanvas(self.gantt_figure)
        gantt_layout.addWidget(self.gantt_canvas)

        self.btn_gantt_refresh = QPushButton("🔄 Aktualisieren")
        self.btn_gantt_refresh.clicked.connect(self.draw_gantt_chart)
        gantt_layout.addWidget(self.btn_gantt_refresh, alignment=Qt.AlignmentFlag.AlignRight)

        self.tabs.addTab(self.gantt_tab, "📊 Gantt")

    def init_stats_tab(self):
        self.stats_tab = QWidget()
        stats_layout = QVBoxLayout(self.stats_tab)

        self.stats_figure = Figure()
        self.stats_canvas = FigureCanvas(self.stats_figure)
        stats_layout.addWidget(self.stats_canvas)

        self.btn_stats_refresh = QPushButton("📈 Aktualisieren")
        self.btn_stats_refresh.clicked.connect(self.draw_stats_chart)
        stats_layout.addWidget(self.btn_stats_refresh, alignment=Qt.AlignmentFlag.AlignRight)

        self.tabs.addTab(self.stats_tab, "📈 Übersicht")

    def init_settings_tab(self):
        self.settings_tab = QWidget()
        settings_layout = QVBoxLayout(self.settings_tab)

        theme_btn = QPushButton("🌙 Theme wechseln (Hell/Dunkel)")
        theme_btn.clicked.connect(self.toggle_theme)
        settings_layout.addWidget(theme_btn)

        export_btn = QPushButton("📁 Speicherort für CSV-Datei wählen")
        export_btn.clicked.connect(self.select_export_path)
        settings_layout.addWidget(export_btn)

        font_note = QLabel("Hinweis: Weitere Einstellungen wie Schriftart folgen später.")
        font_note.setStyleSheet("color: gray;")
        settings_layout.addWidget(font_note)

        self.tabs.addTab(self.settings_tab, "⚙️ Einstellungen")
    def refresh_task_list(self):
        for card, _ in self.tasks:
            card.setParent(None)
        self.tasks.clear()

        all_tasks = self.manager.tasks
        done_count = sum(1 for t in all_tasks if t["done"])
        total_count = len(all_tasks)
        self.progress.setValue(int((done_count / total_count) * 100) if total_count > 0 else 0)

        for task in all_tasks:
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 10, 10, 10)

            top_row = QHBoxLayout()
            checkbox = QCheckBox()
            checkbox.setChecked(task["done"])
            checkbox.stateChanged.connect(lambda _, tid=task["id"]: self.toggle_and_refresh(tid))
            label = QLabel(task["title"])

            btn_edit = QPushButton("✏️")
            btn_edit.setFixedWidth(30)
            btn_edit.clicked.connect(lambda _, t=task: self.edit_task_dialog(t))

            btn_delete = QPushButton("🗑")
            btn_delete.setFixedWidth(30)
            btn_delete.clicked.connect(lambda _, c=card, tid=task["id"]: self.remove_task(c, tid))

            top_row.addWidget(checkbox)
            top_row.addWidget(label)
            top_row.addStretch()
            top_row.addWidget(btn_edit)
            top_row.addWidget(btn_delete)

            card_layout.addLayout(top_row)

            timestamp_label = QLabel(f"🕒 Hinzugefügt am {task['created_at']}")
            timestamp_label.setStyleSheet("color: gray; font-size: 12px;")

            info_row = QHBoxLayout()
            info_row.addWidget(QLabel(f"🏷️ {task['tag']}"))
            info_row.addSpacing(20)
            info_row.addWidget(QLabel(f"📅 {task['due_date']}"))
            info_row.addSpacing(20)
            info_row.addWidget(QLabel(f"🔺 {task['priority']}"))

            card_layout.addWidget(timestamp_label)
            card_layout.addLayout(info_row)

            self.tasks.append((card, label))
            self.task_list_layout.addWidget(card)

    def add_task(self):
        title = self.search_input.text().strip()
        if not title:
            return
        self.manager.add(title, "Allgemein", QDate.currentDate().toString("yyyy-MM-dd"), "Mittel")
        self.search_input.clear()
        self.refresh_task_list()

    def remove_task(self, card, task_id):
        card.setParent(None)
        self.manager.delete(task_id)
        self.refresh_task_list()

    def toggle_and_refresh(self, task_id):
        self.manager.toggle_done(task_id)
        self.refresh_task_list()

    def apply_filter(self, text):
        for card, label in self.tasks:
            card.setVisible(text.lower() in label.text().lower())

    def edit_task_dialog(self, task):
        dialog = QDialog(self)
        dialog.setWindowTitle("Aufgabe bearbeiten")
        layout = QFormLayout(dialog)

        title_edit = QLineEdit(task["title"])
        tag_box = QComboBox()
        tag_box.addItems(["Arbeit", "Privat", "Studium"])
        tag_box.setCurrentText(task["tag"])

        due_edit = QDateEdit()
        due_edit.setDate(QDate.fromString(task["due_date"], "yyyy-MM-dd"))
        due_edit.setCalendarPopup(True)

        prio_box = QComboBox()
        prio_box.addItems(["Niedrig", "Mittel", "Hoch"])
        prio_box.setCurrentText(task["priority"])

        layout.addRow("Titel:", title_edit)
        layout.addRow("Kategorie:", tag_box)
        layout.addRow("Fälligkeitsdatum:", due_edit)
        layout.addRow("Priorität:", prio_box)

        btn_save = QPushButton("Speichern")
        btn_save.clicked.connect(lambda: self.save_edited_task(dialog, task["id"], title_edit.text(), tag_box.currentText(), due_edit.date().toString("yyyy-MM-dd"), prio_box.currentText()))
        layout.addRow(btn_save)

        dialog.exec()

    def save_edited_task(self, dialog, task_id, title, tag, due_date, priority):
        self.manager.edit(task_id, title, tag, due_date, priority)
        dialog.accept()
        self.refresh_task_list()
    def update_calendar_tasks(self):
        # پاک کردن لیست قبلی تسک‌ها در تقویم
        for i in reversed(range(self.calendar_task_list.count())):
            item = self.calendar_task_list.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        selected_date = self.calendar_widget.selectedDate().toString("yyyy-MM-dd")
        tasks_on_date = [t for t in self.manager.tasks if t["due_date"] == selected_date]
def export_tasks(self):
    path, _ = QFileDialog.getSaveFileName(self, "Aufgaben exportieren", "tasks.csv", "CSV-Dateien (*.csv)")
    if not path:
        return
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Titel", "Tag", "Fälligkeitsdatum", "Priorität", "Erledigt", "Erstellt am"])
            for task in self.manager.tasks:
                writer.writerow([
                    task["title"], task["tag"], task["due_date"], task["priority"],
                    "✔" if task["done"] else "✘", task["created_at"]
                ])
    except Exception as e:
        print(f"Fehler beim Exportieren: {e}")

    if not tasks_on_date:
            self.calendar_task_list.addWidget(QLabel("📭 Keine Aufgaben für diesen Tag."))
    else:
        for task in tasks_on_date:
                label = QLabel(f"• {task['title']}  {'✔' if task['done'] else '✘'}")
                label.setStyleSheet("font-size: 16px;")
                self.calendar_task_list.addWidget(label)

    def draw_gantt_chart(self):
        self.gantt_figure.clear()
        ax = self.gantt_figure.add_subplot(111)
        tasks = [t for t in self.manager.tasks if t["due_date"]]

        for i, task in enumerate(tasks):
            try:
                date = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d")
                ax.broken_barh(
                    [(mdates.date2num(date), 1)],
                    (i - 0.4, 0.8),
                    facecolors=("#3cb371" if task["done"] else "#dc143c")
                )
            except Exception:
                continue

        ax.set_yticks(range(len(tasks)))
        ax.set_yticklabels([t["title"] for t in tasks])
        ax.xaxis_date()
        ax.set_xlabel("Datum")
        ax.set_title("📊 Gantt-Diagramm")
        self.gantt_canvas.draw()

    def draw_stats_chart(self):
        self.stats_figure.clear()
        ax = self.stats_figure.add_subplot(111)

        data = {"✔ Erledigt": 0, "✘ Offen": 0}
        for t in self.manager.tasks:
            if t["done"]:
                data["✔ Erledigt"] += 1
            else:
                data["✘ Offen"] += 1

        ax.pie(
            data.values(),
            labels=data.keys(),
            autopct="%1.1f%%",
            startangle=140,
            colors=["#2ecc71", "#e74c3c"]
        )
        ax.set_title("Aufgabenstatus")
        self.stats_canvas.draw()

    def select_export_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "CSV-Datei speichern unter", "tasks.csv", "CSV-Dateien (*.csv)")
        if path:
            try:
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Titel", "Tag", "Fälligkeitsdatum", "Priorität", "Erledigt", "Erstellt am"])
                    for task in self.manager.tasks:
                        writer.writerow([
                            task["title"], task["tag"], task["due_date"], task["priority"],
                            "✔" if task["done"] else "✘", task["created_at"]
                        ])
            except Exception as e:
                print(f"Fehler beim Exportieren: {e}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernTabApp()
    window.show()
    sys.exit(app.exec())
