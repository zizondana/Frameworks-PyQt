from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
)
from PyQt6.QtCore import Qt
import csv

class SettingsTab(QWidget):
    def __init__(self, manager, main_window):
        super().__init__()
        self.manager = manager
        self.main_window = main_window  # برای تغییر تم برنامه
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.theme_btn = QPushButton("🌙 Toggle Theme (Light/Dark)")
        self.theme_btn.clicked.connect(self.main_window.toggle_theme)
        layout.addWidget(self.theme_btn)

        self.export_btn = QPushButton("📁 Choose CSV Save Location")
        self.export_btn.clicked.connect(self.select_export_path)
        layout.addWidget(self.export_btn)

        self.note_label = QLabel("Note: More settings like font selection coming soon.")
        self.note_label.setStyleSheet("color: gray;")
        layout.addWidget(self.note_label)

    def select_export_path(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV File As", "tasks.csv", "CSV Files (*.csv)")
        if path:
            try:
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Title", "Tag", "Due Date", "Priority", "Done", "Created At"])
                    for task in self.manager.tasks:
                        writer.writerow([
                            task["title"], task["tag"], task["due_date"], task["priority"],
                            "✔" if task["done"] else "✘", task["created_at"]
                        ])
            except Exception as e:
                print(f"Error exporting CSV: {e}")
