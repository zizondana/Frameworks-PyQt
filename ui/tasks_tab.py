from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QScrollArea, QLabel, QPushButton,
    QHBoxLayout, QCheckBox, QDialog, QFormLayout, QComboBox, QDateEdit,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QDate
import qtawesome as qta
import csv

class TasksTab(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.tasks = []

        self.setup_ui()
        self.refresh_task_list()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Form for adding tasks
        form_layout = QHBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title...")
        self.title_input.setStyleSheet("font-size: 16px; padding: 6px;")
        form_layout.addWidget(self.title_input)

        self.tag_input = QComboBox()
        self.tag_input.addItems(["Work", "Private", "Study"])
        self.tag_input.setStyleSheet("font-size: 16px;")
        form_layout.addWidget(self.tag_input)

        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setStyleSheet("font-size: 16px; padding: 6px;")
        form_layout.addWidget(self.due_date_input)

        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        self.priority_input.setStyleSheet("font-size: 16px;")
        form_layout.addWidget(self.priority_input)

        self.btn_add = QPushButton()
        self.btn_add.setIcon(qta.icon('mdi.plus', color='green'))
        self.btn_add.setToolTip("Add Task")
        self.btn_add.setFixedSize(50, 50)
        self.btn_add.clicked.connect(self.add_task)
        form_layout.addWidget(self.btn_add)

        layout.addLayout(form_layout)

        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search tasks...")
        self.search_input.setStyleSheet("font-size: 16px; padding: 8px;")
        self.search_input.textChanged.connect(self.apply_filter)
        layout.addWidget(self.search_input)

        # Scroll area for tasks
        self.task_area = QScrollArea()
        self.task_area.setWidgetResizable(True)
        self.task_list_container = QWidget()
        self.task_list_layout = QVBoxLayout(self.task_list_container)
        self.task_list_layout.setSpacing(10)
        self.task_area.setWidget(self.task_list_container)
        layout.addWidget(self.task_area)

    def refresh_task_list(self):
        for card, _ in self.tasks:
            card.setParent(None)
        self.tasks = []

        all_tasks = self.manager.tasks

        for task in all_tasks:
            card = QWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card.setStyleSheet("""
                QWidget {
                    background-color: #f5f9fc;
                    border-radius: 12px;
                    border: 1px solid #d1e4f3;
                }
            """)

            top_row = QHBoxLayout()
            checkbox = QCheckBox()
            checkbox.setChecked(task["done"])
            checkbox.setFixedSize(30, 30)
            checkbox.stateChanged.connect(lambda _, tid=task["id"]: self.toggle_and_refresh(tid))

            label = QLabel(task["title"])
            label.setStyleSheet("font-size: 20px; font-weight: 600;")
            label.setWordWrap(True)

            btn_edit = QPushButton()
            btn_edit.setIcon(qta.icon('mdi.pencil', color='#1976d2'))
            btn_edit.setFixedSize(35, 35)
            btn_edit.setToolTip("Edit Task")
            btn_edit.setStyleSheet("background: transparent;")
            btn_edit.clicked.connect(lambda _, t=task: self.edit_task_dialog(t))

            btn_delete = QPushButton()
            btn_delete.setIcon(qta.icon('mdi.delete', color='#d32f2f'))
            btn_delete.setFixedSize(35, 35)
            btn_delete.setToolTip("Delete Task")
            btn_delete.setStyleSheet("background: transparent;")
            btn_delete.clicked.connect(lambda _, c=card, tid=task["id"]: self.remove_task(c, tid))

            top_row.addWidget(checkbox)
            top_row.addWidget(label)
            top_row.addStretch()
            top_row.addWidget(btn_edit)
            top_row.addWidget(btn_delete)

            card_layout.addLayout(top_row)

            timestamp_label = QLabel(f"🕒 Added on {task['created_at']}")
            timestamp_label.setStyleSheet("color: #999; font-size: 12px; margin-top: 5px;")
            card_layout.addWidget(timestamp_label)

            info_row = QHBoxLayout()
            info_row.addWidget(QLabel(f"🏷️ {task['tag']}"))
            info_row.addSpacing(30)
            info_row.addWidget(QLabel(f"📅 {task['due_date']}"))
            info_row.addSpacing(30)
            info_row.addWidget(QLabel(f"🔺 {task['priority']}"))
            info_row.addStretch()
            card_layout.addLayout(info_row)

            self.tasks.append((card, label))
            self.task_list_layout.addWidget(card)

    def add_task(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Warning", "Task title cannot be empty!")
            return
        self.manager.add(
            title,
            self.tag_input.currentText(),
            self.due_date_input.date().toString("yyyy-MM-dd"),
            self.priority_input.currentText()
        )
        self.title_input.clear()
        self.refresh_task_list()

    def remove_task(self, card, task_id):
        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete this task?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
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
        dialog.setWindowTitle("Edit Task")
        layout = QFormLayout(dialog)

        title_edit = QLineEdit(task["title"])
        tag_box = QComboBox()
        tag_box.addItems(["Work", "Private", "Study"])
        tag_box.setCurrentText(task["tag"])

        due_edit = QDateEdit()
        due_edit.setDate(QDate.fromString(task["due_date"], "yyyy-MM-dd"))
        due_edit.setCalendarPopup(True)

        prio_box = QComboBox()
        prio_box.addItems(["Low", "Medium", "High"])
        prio_box.setCurrentText(task["priority"])

        layout.addRow("Title:", title_edit)
        layout.addRow("Category:", tag_box)
        layout.addRow("Due Date:", due_edit)
        layout.addRow("Priority:", prio_box)

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(lambda: self.save_edited_task(dialog, task["id"], title_edit.text(), tag_box.currentText(), due_edit.date().toString("yyyy-MM-dd"), prio_box.currentText()))
        layout.addRow(btn_save)

        dialog.exec()

    def save_edited_task(self, dialog, task_id, title, tag, due_date, priority):
        self.manager.edit(task_id, title, tag, due_date, priority)
        dialog.accept()
        self.refresh_task_list()

    def export_tasks(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Tasks", "tasks.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Category", "Due Date", "Priority", "Done", "Created At"])
                for task in self.manager.tasks:
                    writer.writerow([
                        task["title"], task["tag"], task["due_date"], task["priority"],
                        "✔" if task["done"] else "✘", task["created_at"]
                    ])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export tasks:\n{e}")
