from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCalendarWidget
)
from PyQt6.QtCore import Qt

class CalendarTab(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.selectionChanged.connect(self.update_calendar_tasks)
        layout.addWidget(self.calendar_widget)

        self.task_list_layout = QVBoxLayout()
        layout.addLayout(self.task_list_layout)

        self.update_calendar_tasks()  # Load initial tasks

    def update_calendar_tasks(self):
        # Clear previous widgets
        for i in reversed(range(self.task_list_layout.count())):
            item = self.task_list_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        selected_date = self.calendar_widget.selectedDate().toString("yyyy-MM-dd")
        tasks_on_date = [t for t in self.manager.tasks if t["due_date"] == selected_date]

        if not tasks_on_date:
            self.task_list_layout.addWidget(QLabel("📭 No tasks for this day."))
        else:
            for task in tasks_on_date:
                label = QLabel(f"• {task['title']}  {'✔' if task['done'] else '✘'}")
                label.setStyleSheet("font-size: 16px;")
                self.task_list_layout.addWidget(label)
