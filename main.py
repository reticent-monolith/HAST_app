from models.child import Child
from models.hastmatrix import HASTMatrix
from models.childrepo import ChildRepo
from gui.mainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import sys

m = HASTMatrix()
cr = ChildRepo()

app = QApplication([])
gui = MainWindow(m, cr)
sys.exit(app.exec())
