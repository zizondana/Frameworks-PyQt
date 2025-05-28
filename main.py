import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from qt_material import apply_stylesheet
from logic.task_manager import TaskManager

from ui.tasks_tab import TasksTab
from ui.calendar_tab import CalendarTab
from ui.gantt_tab import GanttTab
from ui.stats_tab import StatsTab
from ui.settings_tab import SettingsTab

class ModernTabApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Modern Productivity App")
        self.setMinimumSize(1000, 650)
        self.manager = TaskManager("data/tasks.db")
        self.dark_mode = False

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tasks_tab = TasksTab(self.manager)
        self.calendar_tab = CalendarTab(self.manager)
        self.gantt_tab = GanttTab(self.manager)
        self.stats_tab = StatsTab(self.manager)
        self.settings_tab = SettingsTab(self.manager, self)

        self.tabs.addTab(self.tasks_tab, "🗂 Aufgaben")
        self.tabs.addTab(self.calendar_tab, "📅 Kalender")
        self.tabs.addTab(self.gantt_tab, "📊 Gantt")
        self.tabs.addTab(self.stats_tab, "📈 Übersicht")
        self.tabs.addTab(self.settings_tab, "⚙️ Einstellungen")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            apply_stylesheet(app, theme='dark_blue.xml')
        else:
            apply_stylesheet(app, theme='light_blue.xml')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')  
    window = ModernTabApp()
    window.show()
    sys.exit(app.exec())
