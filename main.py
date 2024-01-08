import sys
from PyQt6.QtWidgets import QApplication

from GUI.Controllers.main_ui_controller import FCM_Visualization

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = FCM_Visualization()
    widget.show()
    sys.exit(app.exec())


