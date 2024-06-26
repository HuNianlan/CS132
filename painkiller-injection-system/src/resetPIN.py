from PyQt5.QtWidgets import *

class ResetPINPage(QDialog):
    '''
    This is a class for Page to Reset PIN.

    ResetPINPage class create a window to reset PIN and reply corresponding information,
    update the PIN in the database if the new PIN is valid.

    Attributes:
        processor:   A InjectProcessor class to process all the functions.
    '''

    def __init__(self, processor):
        super().__init__()
        self.processor = processor
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Reset PIN")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.label1 = QLabel("Create New PIN:", self)
        self.lineedit1 = QLineEdit(self)
        self.lineedit1.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label1)
        layout.addWidget(self.lineedit1)

        self.label2 = QLabel("Confirm new PIN:", self)
        self.lineedit2 = QLineEdit(self)
        self.lineedit2.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label2)
        layout.addWidget(self.lineedit2)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.button(QDialogButtonBox.Ok).setText("Confirm")
        self.button_box.accepted.connect(self.confirm)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def confirm(self):
        password1 = self.lineedit1.text()
        password2 = self.lineedit2.text()

        if not password1.isdigit() or len(password1) != 6:
            QMessageBox.warning(self, 'Invalid PIN', 'PIN must be 6 digits, please reset!')
            self.lineedit1.setText("")
            self.lineedit2.setText("")
            return

        if password1 != password2:
            QMessageBox.warning(self, 'Invalid PIN', 'PINs does not match, please reset!')
            self.lineedit1.setText("")
            self.lineedit2.setText("")
            return

        self.getProcessr().resetPIN(password1)
        QMessageBox.information(self, 'Information', 'Reset PIN successfully!')
        
        self.accept()
    
    def getProcessr(self):
        return self.processor
