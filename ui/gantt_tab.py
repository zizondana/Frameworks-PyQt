from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import datetime
from PyQt6.QtCore import Qt

class GanttTab(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.clicked.connect(self.draw_gantt_chart)
        layout.addWidget(self.btn_refresh, alignment=Qt.AlignmentFlag.AlignRight)

        self.draw_gantt_chart()

    def draw_gantt_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
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
        ax.set_xlabel("Date")
        ax.set_title("📊 Gantt Chart")
        self.canvas.draw()
