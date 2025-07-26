from PySide6.QtWidgets import QWidget ,QVBoxLayout ,QScrollArea ,QPushButton , QLabel  ,QHBoxLayout
from PySide6.QtGui import QShortcut ,QKeySequence
from PySide6.QtCore import Qt

from item import item
from datetime import date , timedelta
import sqlite3

class subWindow(QWidget):
    def __init__(self):
        super().__init__()
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self.save)
        self.conn = sqlite3.connect("mydata.db")
        self.cursor = self.conn.cursor() 
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            name TEXT,
            paid TEXT,
            doctor TEXT,
            UNIQUE(date, name)
        )
        """)

        self.conn.commit()

        self.editable=True
        mainlayout= QVBoxLayout()
        self.selecteddate =date.today()
        self.datelabel = QLabel(str(self.selecteddate))
        self.datelabel.setAlignment(Qt.AlignCenter)
        font = self.datelabel.font()
        font.setPointSize(20)  # bigger text
        self.datelabel.setFont(font)
        before = QPushButton("<")
        before.clicked.connect(self.before)
        after = QPushButton(">")
        after.clicked.connect(self.after)
        topper = QHBoxLayout()
        topper.addWidget(before)
        topper.addWidget(self.datelabel)
        topper.addWidget(after)
        self.content =QWidget()
        self.lis = QVBoxLayout()
        self.load()
        self.content.setLayout(self.lis)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.content)
        mainlayout.addLayout(topper)
        mainlayout.addWidget(scroll)
        add = QPushButton("+")
        add.clicked.connect(self.additem)
        mainlayout.addWidget(add)
        self.setLayout(mainlayout)
    
    def additem(self):
        self.lis.addWidget(item(self.lis.count()+1, delete_callback=self.delete_row))
        self.content.setLayout(self.lis)
        self.content.adjustSize()
    def save(self):
        print("saved")
        for i in range(self.lis.count()):
            widget = self.lis.itemAt(i).widget()
            if widget is not None:
                self.cursor.execute("""
                INSERT INTO users (date, name, paid, doctor)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(date, name) DO UPDATE SET
                    paid=excluded.paid,
                    doctor=excluded.doctor
                """,((str(self.selecteddate),) + widget.getvalues()))
                self.cursor.connection.commit()

    def load(self):
        self.cursor.execute("SELECT * FROM users WHERE date=?", (self.selecteddate,))
        rows = self.cursor.fetchall()

        for row in rows:
            self.lis.addWidget(item(self.lis.count()+1,row[2],row[3],row[4], delete_callback=self.delete_row))
        
    def delete_row(self,name):
        if self.editable:
            self.cursor.execute(
                "DELETE FROM users WHERE date=? AND name=?",
                (self.selecteddate, name)
            )
            self.conn.commit()
    
    def before(self):
        self.editable = False
        self.save()
        self.selecteddate = self.selecteddate - timedelta(days = 1)
        self.datelabel.setText(str(self.selecteddate))
        for i in range(self.lis.count()):
            widget = self.lis.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.load()
        self.editable = True
    def after(self):
        self.editable = False
        self.save()
        self.selecteddate = self.selecteddate + timedelta(days = 1)
        self.datelabel.setText(str(self.selecteddate))
        for i in range(self.lis.count()):
            widget = self.lis.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.load()
        self.editable = True