from PyQt5 import QtCore, QtWidgets

class CardInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CardInputDialog, self).__init__(parent)
        self.setWindowTitle('Enter Card Number')
        self.setFixedSize(300, 150)
        layout = QtWidgets.QVBoxLayout()

        self.input_line = QtWidgets.QLineEdit(self)
        layout.addWidget(self.input_line)

        button_layout = QtWidgets.QHBoxLayout()
        self.confirm_button = QtWidgets.QPushButton('Confirm', self)
        self.confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QtWidgets.QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_card_id(self):
        return self.input_line.text()


class CashInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CashInputDialog, self).__init__(parent)
        self.setWindowTitle('Money in the cashiers box')
        self.setFixedSize(300, 150)
        layout = QtWidgets.QVBoxLayout()

        self.input_line = QtWidgets.QLineEdit(self)
        self.input_line.setAlignment(QtCore.Qt.AlignRight)
        layout.addWidget(self.input_line)

        button_layout = QtWidgets.QHBoxLayout()
        self.confirm_button = QtWidgets.QPushButton('Confirm', self)
        self.confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QtWidgets.QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_cash(self):
        if (self.input_line.text() == ""):
            return "0"
        return self.input_line.text()
    
    def check_cash(self,amount):
        self.input_line.setText(amount)
