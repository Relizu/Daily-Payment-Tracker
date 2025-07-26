from PySide6.QtWidgets import QLineEdit ,QRadioButton ,QHBoxLayout ,QFrame ,QLabel ,QPushButton

class item(QFrame):
    def __init__(self,n,cust="",paid="",doct="",delete_callback=None):
        super().__init__()
        self.delete_callback = delete_callback
        self.doc = QLineEdit()
        self.doc.setPlaceholderText("employee")
        self.doc.setText(doct)
        self.cus = QLineEdit()
        self.cus.setPlaceholderText("customer")
        self.cus.setText(cust)
        self.paid1 = QRadioButton()
        self.paid2 = QRadioButton()
        if paid=="1":
            self.paid1.setChecked(True)
            self.tored()
        elif paid =="2":
            self.paid2.setChecked(True)
            self.togreen()
        self.paid1.toggled.connect(self.tored)
        self.paid2.toggled.connect(self.togreen)
        deleteitem = QPushButton("X")
        deleteitem.clicked.connect(self.removeitem)
        layout = QHBoxLayout()
        layout.addWidget(deleteitem)
        layout.addWidget(self.doc)
        layout.addWidget(self.paid1)
        layout.addWidget(self.paid2)
        layout.addWidget(self.cus)
        layout.addWidget(QLabel("."+str(n)))
        self.setLayout(layout)

    def tored(self):
        self.setStyleSheet("""
    QFrame ,QRadioButton{
        background-color: red;
    }
    *{
        background-color: white;
        color: black; 
    }
""")
    def togreen(self):
        self.setStyleSheet("""
    QFrame , QRadioButton{
        background-color: green;
    }
    *{
        background-color: white;
        color: black;  
    }
""")
    def removeitem(self):
        if self.delete_callback:
            name = self.cus.text()
            self.delete_callback(name)
        self.deleteLater()
    def getvalues(self):
        if self.paid1.isChecked():
            paid ="1"
        elif self.paid2.isChecked():
            paid ="2"
        else:
            paid=""
        return (self.cus.text(),paid,self.doc.text())