from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtWidgets import QDateEdit, QDialog, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from models.child import Child
from models.childrepo import ChildRepo
import datetime as dt
import hast



class MainWindow(QMainWindow):
    def __init__(self, repo: ChildRepo):
        super().__init__()
        self.repo = repo
        self.children = []
        self.setWindowTitle("HAST Scorer")
        self.resize(900,600)
        self.setWindowIcon(QIcon("./icons/exam.png"))
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
            if type(widget) in (QLineEdit,):
                widget.setFixedWidth(200)
            if type(widget) in (QDateEdit,):
                widget.setFixedWidth(100)
            if type(widget) in (QLabel,):
                widget.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(widget)
        date: QDateEdit = self.buttonArea["dob"]
        currentDate = dt.date.today()
        date.setMinimumDate(QDate(currentDate.year-11, 7, 31))
        date.setMaximumDate(QDate(currentDate.year-5, 8, 1))
        self.layout.addLayout(layout)

    def connectButtons(self):
        btn_addChild: QPushButton = self.buttonArea.get("addChild")
        btn_addChild.clicked.connect(self.addChild)

    def setupTable(self):
        self.table = QTableWidget(0, 7)
        self.layout.addWidget(self.table)
        self.table.setHorizontalHeaderLabels([
            "First Names",
            "Surname",
            "Date of birth",
            "Age",
            "HAST Score 1",
            "Spelling age",
            ""
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader()
        # self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)

    
    def populateTable(self):
        self.table.setRowCount(0)
        for i, child in enumerate(self.repo.getAll()):
            self.children.append(child)
            self.table.insertRow(i)
            col = 0
            item = QTableWidgetItem(child.firstNames)
            self.table.setItem(i, col, item)
            col = 1
            item = QTableWidgetItem(child.lastName)
            self.table.setItem(i, col, item)
            col = 2
            item = QTableWidgetItem(child.dob)
            self.table.setItem(i, col, item)
            col = 3
            stringAge = f"{child.age[0]} years {child.age[1]} months"
            item = QTableWidgetItem(stringAge)
            self.table.setItem(i, col, item)
            col = 4
            item = QTableWidgetItem(child.score1)
            self.table.setItem(i, col, item)
            col = 5
            stringAge = f"{child.spellingAge[0]} years {child.spellingAge[1]} months" if child.spellingAge != None else ""
            item = QTableWidgetItem(stringAge)
            self.table.setItem(i, col, item)
            col = 6
            scoreBtn = QPushButton("Score")
            self.connectButtonToChild(child._id, scoreBtn, "score")
            delBtn = QPushButton("Delete")
            self.connectButtonToChild(child._id, delBtn, "delete")
            btnWidget = QWidget()
            btnL = QHBoxLayout()
            btnL.setContentsMargins(0,0,0,0)
            btnL.addWidget(scoreBtn)
            btnL.addWidget(delBtn)
            btnWidget.setLayout(btnL)
            self.table.setCellWidget(i, col, btnWidget)

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

    def scoreChild(self, id: int):
        child = self.repo.get(id)
        # create dialog with mark entry, generate button, save button, cancel button, and display for child data
        d = QDialog()
        d.setWindowIcon(QIcon("./icons/exam.png"))
        d.setWindowTitle(f"Add score for {child.firstNames} {child.lastName}")
        lay = QVBoxLayout()
        d.setLayout(lay)
        display = [
            (QLabel("Name: "), QLabel(f"{child.firstNames} {child.lastName}")),
            (QLabel("Date of birth: "), QLabel(child.dob)),
            (QLabel("Age: "), QLabel(f"{child.age[0]} years {child.age[1]} months")),
            (QLabel("HAST Score: "), QLabel(child.score1)),
        ]
        # Because you can't subscript None
        if child.spellingAge != None: 
            display.append((QLabel("Spelling age: "), QLabel(
                f"{child.spellingAge[0]} years {child.spellingAge[1]} months")))
        else:
            display.append((QLabel("Spelling age: "), QLabel(None)))
        for label, value in display:
            row = QHBoxLayout()
            row.setSpacing(5)
            row.addWidget(label)
            row.addWidget(value)
            lay.addLayout(row)
        row = QHBoxLayout()
        markEdit = QLineEdit()
        markEdit.setValidator(QIntValidator(0, 65))
        markEdit.setPlaceholderText("Mark")
        genBtn = QPushButton("Generate")
        row.addWidget(markEdit)
        row.addWidget(genBtn)
        lay.addLayout(row)
        # generate button runs hast.getScore() using passed in child data and updates copied child object
        def generateScores(mark: int):
            try:
                score = hast.getScore(child.age, mark)
                spellingAge = hast.getSpellingAge(mark)
            except Exception as e:
                print(e)
                return
            child.score1 = score
            child.spellingAge = spellingAge
            # refresh
            display[3][1].setText(child.score1)
            display[4][1].setText(f"{child.spellingAge[0]} years {child.spellingAge[1]} months")
            markEdit.setText("")
        genBtn.clicked.connect(lambda: generateScores(int(markEdit.text())))
        # save button pushes the child copy to the database to update the existing child
        saveBtn = QPushButton("Save")
        lay.addWidget(saveBtn)
        saveBtn.clicked.connect(lambda: self.repo.update(child._id, child))
        saveBtn.clicked.connect(d.close)
        #   call populateTable()
        # cancel button just closes the dialog without any updates
        d.exec()
        self.populateTable()

    def deleteChild(self, childId):
        self.repo.delete(childId)
        self.populateTable()

    def clearInputs(self):
        for widget in self.buttonArea.values():
            if type(widget) == QLineEdit:
                widget.setText("")

    def connectButtonToChild(self, childId: int, button: QPushButton, func: str):
        """Because of lazy lambdas again..."""
        if func == "score":
            button.clicked.connect(lambda: self.scoreChild(childId))
        elif func == "delete":
            button.clicked.connect(lambda: self.deleteChild(childId))
