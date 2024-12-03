from main_m import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
from solver_be import Solv
import sys


class MainM(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.open_first_form)

    
    def open_first_form(self):
        try:
            self.first_form = Solv()
            self.close()
            self.first_form.show()
        except Exception as e:
            print(f"Ошибка при открытии окна: {e}")
    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wind = MainM()
    wind.show()
    sys.exit(app.exec())
