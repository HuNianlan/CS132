from PyQt5 import QtCore, QtGui, QtWidgets

class WelcomePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WelcomePage, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.balance_label = QtWidgets.QLabel('Welcome to the ATM!', self)
        self.balance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.balance_label.setFixedHeight(50)
        self.balance_label.setStyleSheet("font-size: 24px;") 

        self.insert_card_label = QtWidgets.QLabel('Please Insert Your Card', self)
        self.insert_card_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.insert_card_label.setFixedSize(200, 50)
        self.insert_card_label.setStyleSheet("color: red;")

        self.create_account_button = QtWidgets.QPushButton('Create Account', self)
        self.create_account_button.setFixedSize(150, 50)
        # self.create_account_button.clicked.connect(self.create_account)

        layout.addWidget(self.balance_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.create_account_button, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.insert_card_label, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.setLayout(layout)

