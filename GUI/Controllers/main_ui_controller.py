import numpy as np
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog

from GUI.py_forms.main_ui import Ui_fcm_visualizer
from GUI.Controllers.main_ui_controller import *

from APIs.data_processor import *
from APIs.machine_learning.data_clustering.semi_supervised_fuzzy_c_means import *
from APIs.machine_learning.data_clustering.validator import *

class FCM_Visualization(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.data = np.zeros((1, 3))
		self.data_processor = DataProcess()
		self.ui = Ui_fcm_visualizer()
		self.ui.setupUi(self)
		self.setup_form_validation()
		self.setupSlot()
	
	def show_message_dialog(self, title: str = "Notice", message: str = ""):
		notice_box = QMessageBox(self)
		match title:
			case "Notice": notice_box.setIcon(QMessageBox.Icon.Information)
			case "Error": notice_box.setIcon(QMessageBox.Icon.Critical)
			case "Warning": notice_box.setIcon(QMessageBox.Icon.Warning)
			case "Confirm": notice_box.setIcon(QMessageBox.Icon.Question)
		notice_box.setWindowTitle(title)
		notice_box.setText(message)
		notice_box.setStandardButtons(QMessageBox.StandardButton.Ok)
		notice_box.exec()
	
	def setupSlot(self):
		# self.ui.select_fcm_mode.stateChanged(lambda:self.ui.table_prime_u.setEnabled(self.ui.select_fcm_mode.isChecked()))
		self.ui.btn_export_data.disconnect()
		self.ui.btn_browser.disconnect()
		self.ui.btn_fcm.disconnect()
		self.ui.btn_browser.clicked.connect(self.on_btn_file_browser_clicked)
		self.ui.btn_export_data.clicked.connect(self.on_btn_export_data_clicked)
		self.ui.btn_fcm.clicked.connect(self.on_btn_fcm_clicked)
		self.ui.line_n_cluster.textChanged.connect(lambda :self.update_u_table(table = self.ui.table_prime_u))
		lines_edit = [self.ui.line_eps, self.ui.line_n_cluster, self.ui.line_max_iter, self.ui.line_fuziness]
		for line in lines_edit:
			line.textChanged.connect(
				lambda: self.ui.btn_fcm.setEnabled(all([line_input.valid for line_input in lines_edit])))
	
	def setup_form_validation(self):
		cui = self.ui
		cui.line_eps.set_value_range(min_val=0)
		cui.line_fuziness.set_value_range(min_val=1)
		cui.line_n_cluster.set_value_type(int).set_value_range(min_val=1)
		cui.line_max_iter.set_value_type(int).set_value_range(min_val=0)
	def on_btn_file_browser_clicked(self):
		default_folder = "D:/projects/code/zHJuniikPy/CODE PYTHON/GraduateResearch1/dataset"
		file_path, _ = QFileDialog.getOpenFileName(self, "Select a data file", default_folder)
		if file_path:
			self.ui.line_data_src.setText(file_path)
			
	def on_btn_export_data_clicked(self):
		def update_figures_list():
			self.ui.list_figures.clear()
			self.ui.list_figures.addItems(list(self.data.columns))
		
		try:
			src = self.ui.line_data_src.text()
			self.data = export_data(src)
			update_figures_list()
			self.ui.table_data.update_data_view(self.data)
			self.ui.graph_combo.set_data(self.data)
			self.update_supervised_table()
		except Exception as e:
			self.show_message_dialog("Error", f"Error on exporting data!\n{str(e)}")
	
	def on_btn_fcm_clicked(self):
		cui = self.ui
		
		figures = [item.text() for item in
			   list(cui.list_figures.selectedItems())]  # Get figures of dataset that use for clustering
		if not figures:
			return self.show_message_dialog("Error", "There is no figures in dataset")
		
		selected_data = self.data_processor.preprocess_data(self.data[figures])
		c = cui.line_n_cluster.get_value()  # Number of cluster
		m = cui.line_fuziness.get_value()  # Fuzziness index
		max_iter = cui.line_max_iter.get_value()  # Max time update in loop
		eps = cui.line_eps.get_value() # expected error of result
		u_prime = np.zeros((selected_data.shape[0], c))
		if self.ui.select_fcm_mode.isChecked():
			self.export_supervised_matrix(u_prime)
		print("Clustering...")
		u, v, d = ssfcm(selected_data, c, m, max_iter, eps, u_prime)
		validator = get_validator_criteria(selected_data, u, v, m)
		# validator = {}
		print("Updating GUI...")
		self.update_u_table(table= self.ui.table_u, u_matrix= u)
		self.ui.graph_combo.set_data(color_ratios=u).update_content()
		self.log_fcm_result(figures, v, d, validator)
		
	def log_fcm_result(self,figures, v:np.ndarray, d: int, validator):
		v = pd.DataFrame(data = self.data_processor.reverse_scale_data(v), columns= figures, index=range(v.shape[0]))
		result = f'Converged after {d} times\nValidator Criteria:\n'
		for valid in validator:
			result += f'{valid} = {validator[valid]}\n'
		result += 'Centroids:\n'
		result += v.to_string(col_space=32, justify='right')
		self.ui.text_cmd.setText(result)
	
	def update_supervised_table(self):
		table = self.ui.table_prime_u
		table.setColumnCount(1)
		table.setRowCount(self.data.shape[0])
		table.setHorizontalHeaderLabels(['Cluster'])
	
	def export_supervised_matrix(self, u_prime: np.ndarray):
		table = self.ui.table_prime_u
		n_cluster = u_prime.shape[1]
		row = table.rowCount()
		for i in range (row):
			item = table.item(i, 0)
			val = int(item.text()) if item is not None and item.text() else 0
			if val in range(1, n_cluster+1):
				u_prime[i, val-1] = 0.5
		
	
	def update_u_table(self, table, u_matrix: np.ndarray = None):
		if u_matrix is not None:
			columns = [f'CLuster {i+1}' for i in range(u_matrix.shape[1])]
			u = import_array_to_data(u_matrix, columns)
			table.update_data_view(u, '{:.6f}')
			return None
		if not self.ui.line_n_cluster.valid:
			return None
		row = self.data.shape[0]
		col = self.ui.line_n_cluster.get_value()
		df = pd.DataFrame(0, index=range(row), columns=[f'Cluster {i+1}' for i in range(col)])
		table.update_data_view(df)