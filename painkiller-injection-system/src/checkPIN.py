from PyQt5.QtWidgets import *

class CheckPINPage(QDialog):
    '''
    This is a class for Page to Check PIN.

    CheckPINPage class create a window to check PIN and reply corresponding information.

    Attributes:
        processor:   A InjectProcessor class to process all the functions.
        times:  An int of attempting times left to check.
    '''

    def __init__(self, processor):
        super().__init__()
        self.processor = processor
        self.times = 3
        self.initUI()
    
    def initUI(self):
        self.setGeometry(200, 200, 450, 200)
        self.setWindowTitle('Check PIN')

        self.label = QLabel(f"Please enter the PIN ({self.times} times left):", self)
        self.label.setGeometry(10, 10, 400, 50)
        self.checkPIN = QLineEdit(self)
        self.checkPIN.setEchoMode(QLineEdit.Password)
        self.checkPIN.setGeometry(70, 60, 200, 50)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.button(QDialogButtonBox.Ok).setText("Confirm")
        self.button_box.accepted.connect(self.Confirm)
        self.button_box.rejected.connect(self.reject)
        self.button_box.setGeometry(45, 115, 250, 50)

    def Confirm(self):
        entered_PIN = self.checkPIN.text()

        if self.getProcessor().checkPIN(entered_PIN):
            self.accept()
        else:
            self.times = self.times - 1
            if self.times > 0:
                QMessageBox.warning(self, "Wrong PIN", "Please type in correct PIN!")
                self.checkPIN.clear()
                self.label.setText(f"Please enter the PIN ({self.times} times left):")
                return
            else:
                QMessageBox.critical(self, 'Error', 'No attempts left, PIN check failed!')
                self.reject()
    
    def getProcessor(self):
        return self.processor
