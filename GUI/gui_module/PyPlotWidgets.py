# This Python file uses the following encoding: utf-8
#from PySide6 import QtCore
#from PySide6.QtWidgets import QWidget
from PyQt6.QtWidgets import QWidget, QComboBox, QHBoxLayout, QGridLayout

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
import pandas as pd
import numpy as np

cluster_colors = [
    "#FF0000",  # Red
    "#00FF00",  # Green
    "#0000FF",  # Blue
    "#FF00FF",  # Purple
    "#FFFF00",  # Orange
    "#00FFFF",  # Yellow
    "#33FF33",  # Teal
    "#FF3333",  # Pink
    "#3333FF",  # Cyan
    "#2D2D2D"   # Brown
]
default_color = "#3333FF"
def mix_color(rate) -> str:
    r, g, b = 0, 0, 0
    color_rate = list(rate)
    num_cluster = len(color_rate)
    for i in range(num_cluster):
        cluster_color = hexa_to_rgb(cluster_colors[i])
        r += int(color_rate[i] * cluster_color[0])
        g += int(color_rate[i] * cluster_color[1])
        b += int(color_rate[i] * cluster_color[2])
    return f"#{hex(r)[2:].zfill(2)}{hex(g)[2:].zfill(2)}{hex(b)[2:].zfill(2)}"
def hexa_to_rgb(hex_color: str) -> list:
    return [ int(hex_color[1:3], 16), int(hex_color[3:5], 16),int(hex_color[5:7], 16)]

def get_color_set(color_rate_matrix: np.ndarray = None) -> str | list[str]:
    if color_rate_matrix is None:
        return default_color
    return [mix_color(i) for i in color_rate_matrix]

class Graph2DAxisComboBox(QWidget):
    x_combo: QComboBox
    y_combo: QComboBox
    
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.figures = None
        layout = QHBoxLayout(self)
        self.x_combo = QComboBox(self)
        self.y_combo = QComboBox(self)
        layout.addWidget(self.x_combo)
        layout.addWidget(self.y_combo)
    
    def set_figures(self, data):
        figures = list(data.columns)
        self.x_combo.clear()
        self.y_combo.clear()
        self.x_combo.addItems(figures)
        self.y_combo.addItems(figures)
        self.x_combo.setCurrentIndex(0)
        self.y_combo.setCurrentIndex(1 % len(figures))
        return self

class QCustomPyPlot(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize= (100, 100), dpi = 80, tight_layout= True)
        self.plot = fig.add_subplot()
        super().__init__(fig)
        # self.plot.set_aspect('equal', adjustable='datalim')
        self.setParent(parent)
        self.setMouseTracking(True)
        self.mpl_connect('scroll_event', self.on_scroll)
    
    def update_plot(self,data: pd.DataFrame, color_set = default_color, x_label:str = 0, y_label: str = 1):
        self.plot.clear()
        if x_label == "" or y_label == "":
            return self
        if color_set is None or len(color_set) != data.shape[0]:
            color_set = default_color
        self.plot.scatter(x = data[x_label], y = data[y_label], c = color_set)
        self.plot.set_xlabel(x_label)
        self.plot.set_ylabel(y_label)
        self.plot.set_title(f'{x_label} vs {y_label}')
        self.draw()
        return self
    
    def on_scroll(self, event):
        if event.button == 'up':
            self.zoom(1.1)
        elif event.button == 'down':
            self.zoom(0.9)
    
    def zoom(self, factor):
        xlim = self.plot.get_xlim()
        ylim = self.plot.get_ylim()
        new_xlim = (
            (xlim[0] - xlim[1]) / 2 * (1 - factor) + xlim[0],
            (xlim[1] - xlim[0]) / 2 * (1 - factor) + xlim[1]
        )
        new_ylim = (
            (ylim[0] - ylim[1]) / 2 * (1 - factor) + ylim[0],
            (ylim[1] - ylim[0]) / 2 * (1 - factor) + ylim[1]
        )
        self.plot.set_xlim(new_xlim)
        self.plot.set_ylim(new_ylim)
        self.draw()


class QGraph(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.data = None
        self.color_set = None
        self.grid = self.grid = QGridLayout(self)
        self.graph_content = QCustomPyPlot(self)
        self.graph_tools = NavigationToolbar(self.graph_content, self)
        self.axis_boxes = Graph2DAxisComboBox(self)
        self.link_content_to_controller()
        self.setupUi()
    def setupUi(self):
        self.setStyleSheet("border: 1px solid black;")
        self.grid.setContentsMargins(3, 3, 3, 3)
        self.grid.setSpacing(3)
        self.grid.addWidget(self.graph_content, 0, 0, 1, 2)
        self.grid.addWidget(self.graph_tools, 1, 0, 1, 1)
        self.grid.addWidget(self.axis_boxes, 1, 1, 1, 1)
        self.grid.setColumnStretch(0, 6)
        self.grid.setColumnStretch(1, 4)
        self.grid.setRowStretch(0, 8)
        self.grid.setRowStretch(1, 1)
    
    def link_content_to_controller(self):
        self.axis_boxes.x_combo.currentTextChanged.connect(self.update_content)
        self.axis_boxes.y_combo.currentTextChanged.connect(self.update_content)
    
    def update_content(self):
        x_label = self.axis_boxes.x_combo.currentText()
        y_label = self.axis_boxes.y_combo.currentText()
        self.graph_content.update_plot(self.data, self.color_set, x_label= x_label, y_label = y_label)
	    
    def set_data(self, data: pd.DataFrame = None, color_ratios: np.ndarray = None):
        if data is not None:
            self.data = data
            self.axis_boxes.set_figures(data)
        self.color_set = get_color_set(color_ratios)
        if len(self.color_set) != self.data.shape[0]:
            self.color_set = default_color
        return self

