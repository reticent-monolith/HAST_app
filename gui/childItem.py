from PyQt6.QtWidgets import QTableWidgetItem
from models.child import Child

class ChildItem(QTableWidgetItem):
    def __init__(self, text: str, child: Child):
        super().__init__(text)
        self.child = child