from PySide6.QtWidgets import QMainWindow
from subwindow import subWindow
from PySide6.QtGui import QCloseEvent

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Payment Tracker")
        self.resize(500,500)
        self.window = subWindow()
        self.setCentralWidget(self.window)
    def closeEvent(self, event: QCloseEvent):
        self.window.save()  # Call save before closing
        event.accept()