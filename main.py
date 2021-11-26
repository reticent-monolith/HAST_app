from models.child import Child
from models.childrepo import ChildRepo
from gui.mainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

cr = ChildRepo()

app = QApplication([])
gui = MainWindow(cr)
sys.exit(app.exec())
