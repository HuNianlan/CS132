from PyQt5 import QtCore, QtWidgets

class Ui_LoginPage(object):
    def setupUi(self, loginPage):
        loginPage.setObjectName("loginPage")
        loginPage.resize(401, 693)
        loginPage.setMinimumSize(QtCore.QSize(401, 693))
        loginPage.setMaximumSize(QtCore.QSize(401, 693))



        # self.listView = QtWidgets.QListView(loginPage)
        # self.listView.setGeometry(QtCore.QRect(0,0,401, 693))
        # self.listView.setObjectName("listView")
        # self.listView.setStyleSheet("QListView { background-image: url('YourCodeExample/banking_app/hhh.png'); }")

        self.pushButton_3 = QtWidgets.QPushButton(loginPage)
        self.pushButton_3.setGeometry(QtCore.QRect(120, 500, 161, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)

        self.lineEdit = QtWidgets.QLineEdit(loginPage)
        self.lineEdit.setGeometry(QtCore.QRect(160, 360, 201, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(loginPage)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 420, 201, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(loginPage)
        self.label.setGeometry(QtCore.QRect(70, 370, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(loginPage)
        self.label_2.setGeometry(QtCore.QRect(70, 420, 60, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(loginPage)
        QtCore.QMetaObject.connectSlotsByName(loginPage)

    def retranslateUi(self, loginPage):
        _translate = QtCore.QCoreApplication.translate
        loginPage.setWindowTitle(_translate("loginPage", "Log In"))
        self.pushButton_3.setText(_translate("loginPage", "Log in"))
        self.label.setText(_translate("loginPage", "      id"))
        self.label_2.setText(_translate("loginPage", "password"))
