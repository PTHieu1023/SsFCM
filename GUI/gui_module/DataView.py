from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

import pandas as pd
import numpy as np

class DataTable(QTableWidget):

    def __init__(self, parent = None):
        super().__init__(parent = parent)

    def update_data_view(self, data: pd.DataFrame, format_style: str = ""):
        self.clear()
        self.setRowCount(data.shape[0])
        self.setColumnCount(data.shape[1])
        self.setHorizontalHeaderLabels(data.columns)
        for row in data.iterrows():
            for col_index, value in enumerate(row[1]):
                str_val = "    " + (format_style.format(value) if format_style else str(value))
                item = QTableWidgetItem(str_val)
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.setItem(row[0], col_index, item)
        self.resizeColumnsToContents()
    
    def extract_data(self):
        rows = self.rowCount()
        cols = self.columnCount()
        data = np.zeros((rows, cols), dtype=float)
        try:
            for i in range(rows):
                for j in range(cols):
                    item = self.item(i, j)
                    data[i, j] = float(item.text()) if item is not None and item.text() else 0
        except:
            print('Some data is in invalid format')
        return data
