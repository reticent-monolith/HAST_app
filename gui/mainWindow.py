from PyQt6.QtWidgets import QDateEdit, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from models.child import Child

class MainWindow(QMainWindow):
    def __init__(self, matrix, repo):
        super().__init__()
        self.repo = repo
        self.matrix = matrix

        self.setWindowTitle("HAST Scorer")
        self.resize(800,600)
        self.layout = QVBoxLayout()
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.setupButtonArea()
        self.setupTable()

        self.connectButtons()
        self.populateTable()

        self.show()

    def setupButtonArea(self):
        layout = QHBoxLayout()
        self.buttonArea = {
            "fnameLabel": QLabel("First names"),
            "firstNames": QLineEdit(),
            "lnameLabel": QLabel("Last name"),
            "lastName": QLineEdit(),
            "dobLabel": QLabel("Date of birth"),
            "dob": QDateEdit(calendarPopup=True),
            "addChild": QPushButton("Add child")
        }
        for widget in self.buttonArea.values():
            layout.addWidget(widget)
        self.layout.addLayout(layout)

    def connectButtons(self):
        btn_addChild: QPushButton = self.buttonArea.get("addChild")
        btn_addChild.clicked.connect(self.addChild)

    def setupTable(self):
        self.table = QTableWidget(0, 6)
        self.layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels([
            "First Names",
            "Surname",
            "Date of birth",
            "Score 1",
            "Score 2",
            ""
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    def populateTable(self):
        self.table.setRowCount(0)
        for i, child in enumerate(self.repo.getAll()):
            self.table.insertRow(i)
            col = 0
            item = QTableWidgetItem(' '.join(child.firstNames))
            self.table.setItem(i, col, item)
            col = 1
            item = QTableWidgetItem(child.lastName)
            self.table.setItem(i, col, item)
            col = 2
            item = QTableWidgetItem(child.dob)
            self.table.setItem(i, col, item)
            col = 3
            item = QTableWidgetItem(child.score1)
            self.table.setItem(i, col, item)
            col = 4
            item = QTableWidgetItem(child.score2)
            self.table.setItem(i, col, item)
            col = 5
            delBtn = QPushButton("Delete")
            delBtn.clicked.connect(lambda: self.deleteChild(child._id))
            self.table.setCellWidget(i, col, delBtn)

    def addChild(self):
        b = self.buttonArea
        args = [
            b["firstNames"].text().split(' '),
            b["lastName"].text(),
            b["dob"].date().toPyDate().isoformat()
        ]
        child = Child(*args)
        self.repo.add(child)
        for widget in self.buttonArea.values():
            if type(widget) == "PyQt6.QtWidgets.QLineEdit":
                widget.setText("")
        self.populateTable()

    def deleteChild(self, childId):
        self.repo.delete(childId)
        self.populateTable()
