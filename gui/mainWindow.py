from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QDateEdit, QDial, QDialog, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QPushButton, QTableView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from models.child import Child
from models.childrepo import ChildRepo
from gui.childItem import ChildItem
import datetime as dt

class MainWindow(QMainWindow):
    def __init__(self, matrix, repo: ChildRepo):
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
        date: QDateEdit = self.buttonArea["dob"]
        currentDate = dt.date.today()
        date.setMinimumDate(QDate(currentDate.year-11, 7, 31))
        date.setMaximumDate(QDate(currentDate.year-5, 8, 1))
        self.layout.addLayout(layout)

    def connectButtons(self):
        btn_addChild: QPushButton = self.buttonArea.get("addChild")
        btn_addChild.clicked.connect(self.addChild)
        self.table.itemDoubleClicked.connect(self.openEditDialog)

    def openEditDialog(self, info: ChildItem):
        columns = {
            0: {"dataName": "firstNames", "humanName": "first names"},
            1: {"dataName": "lastName", "humanName": "last name"},
            2: {"dataName": "dob", "humanName": "date of birth"},
            3: {"dataName": "score1", "humanName": "first score"},
            4: {"dataName": "score2", "humanName": "second score"}
        }
        dialog = QDialog()
        layout = QVBoxLayout()
        dialog.setLayout(layout)
        editingField = columns[info.column()]
        lineEdit = QLineEdit()
        layout.addWidget(lineEdit)
        if info.column() in (0,1,2):
            dialog.setWindowTitle(f"Edit {editingField['humanName']}")
            lineEdit.setText(info.child.__dict__[editingField["dataName"]])
            updateButton = QPushButton("Update")
            layout.addWidget(updateButton)
            updateButton.clicked.connect(lambda: self.updateChild(editingField, lineEdit, info, dialog))
        else:
            dialog.setWindowTitle(f"Generate new {editingField['humanName']}")
            generateButton = QPushButton("Generate")
            layout.addWidget(generateButton)
            generateButton.clicked.connect(
                lambda: self.generateChildScore(editingField, lineEdit, info, dialog))
        dialog.exec()

    def updateChild(self, field: dict, lineEdit: QLineEdit, item: ChildItem, d: QDialog):
        oldChild = item.child
        args = {k:v for k,v in oldChild.__dict__.items() if k != "age"}
        args[field["dataName"]] = lineEdit.text()
        newChild = Child(**args)
        self.repo.update(newChild._id, newChild)
        self.populateTable()
        d.close()

    def generateChildScore(self, field: dict, lineEdit: QLineEdit, item: ChildItem, d: QDialog):
        testScore = int(lineEdit.text())
        child = item.child
        score = self.matrix.getScore(child.age, testScore)
        args = {k: v for k, v in child.__dict__.items() if k != "age"}
        args[field["dataName"]] = score
        newChild = Child(**args)
        self.repo.update(child._id, newChild)
        self.populateTable()
        d.close()
        

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
        # self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

    
    def populateTable(self):
        self.table.setRowCount(0)
        for i, child in enumerate(self.repo.getAll()):
            self.table.insertRow(i)
            col = 0
            item = ChildItem(child.firstNames, child)
            self.table.setItem(i, col, item)
            col = 1
            item = ChildItem(child.lastName, child)
            self.table.setItem(i, col, item)
            col = 2
            item = ChildItem(child.dob, child)
            self.table.setItem(i, col, item)
            col = 3
            item = ChildItem(child.score1, child)
            self.table.setItem(i, col, item)
            col = 4
            item = ChildItem(child.score2, child)
            self.table.setItem(i, col, item)
            col = 5
            delBtn = QPushButton("Delete")
            delBtn.clicked.connect(lambda: self.deleteChild(child._id))
            self.table.setCellWidget(i, col, delBtn)

    def addChild(self):
        b = self.buttonArea
        args = [
            b["firstNames"].text(),
            b["lastName"].text(),
            b["dob"].date().toPyDate().isoformat()
        ]
        child = Child(*args)
        self.repo.add(child)
        for widget in self.buttonArea.values():
            if type(widget) == "PyQt6.QtWidgets.QLineEdit":
                widget.setText("")
        self.clearInputs()
        self.populateTable()

    def deleteChild(self, childId):
        self.repo.delete(childId)
        self.populateTable()

    def clearInputs(self):
        for widget in self.buttonArea.values():
            if type(widget) == QLineEdit:
                widget.setText("")
