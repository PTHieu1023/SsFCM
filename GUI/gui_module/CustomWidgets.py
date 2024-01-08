from PyQt6.QtWidgets import QLineEdit
#from PySide6.QtCore import Signal
#from PySide6.QtCore import Qt

# from abc import abstractmethod

class CustomLineEdit(QLineEdit):
    valid: bool = True

    def __init__(self, parent: None):
        super().__init__(parent = parent)
        self.textChanged.connect(self.check_validation)

    # @abstractmethod
    def check_validation(self):
        pass

    def change_to_state(self, is_valid: bool):
        self.setStyleSheet("color: black;") if is_valid else self.setStyleSheet("color: red;")
        self.valid = is_valid

    def get_value(self):
        return str(self.text())

class NumericLineEdit(CustomLineEdit):
    min_value = - (1 << 31) + 1
    max_value = 1 << 31 - 1
    value_type = None
    def __init__(self, parent = None, type = float):
        super().__init__(parent=parent)
        self.set_value_type(type).set_value_range()

    def set_value_type(self, type = float):
        self.value_type = type
        return self

    def set_value_range(self, min_val = -(1<<31) + 1, max_val = (1<<31)-1):
        try:
            self.min_value = self.value_type(min_val)
            self.max_value = self.value_type(max_val)
        except ValueError:
            self.min_value = -(1<<31) + 1
            self.max_value = 1<<31-1
        return self

    def check_validation(self):
        try:
            if self.text() == "":
                raise ValueError
            val = self.value_type(self.text())
            if val < self.min_value:
                raise ValueError
            if val > self.max_value:
                raise ValueError
            self.change_to_state(True)
        except ValueError:
            self.change_to_state(False)

    def get_value(self):
        try:
            if self.value_type == float:
                return float(super().get_value())
            if self.value_type == int:
                return int(super().get_value())
        except:
            raise Exception(f"{super().get_value()} is invalid for {self.value_type}")
        

