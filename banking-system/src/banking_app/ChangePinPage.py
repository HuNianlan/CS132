from PyQt5 import QtCore, QtWidgets


class Ui_ChangePin(object):
    def setupUi(self, ChangePin):
        ChangePin.setObjectName("ChangePin")
        ChangePin.resize(401, 693)
        ChangePin.setMinimumSize(QtCore.QSize(401, 693))
        ChangePin.setMaximumSize(QtCore.QSize(401, 693))


        # self.listView = QtWidgets.QListView(ChangePin)
        # self.listView.setGeometry(QtCore.QRect(0,0,401, 693))
        # self.listView.setObjectName("listView")
        # self.listView.setStyleSheet("QListView { background-image: url('hhh.png'); }")


        self.label = QtWidgets.QLabel(ChangePin)
        self.label.setGeometry(QtCore.QRect(150, 190, 71, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ChangePin)
        self.label_2.setGeometry(QtCore.QRect(40, 270, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(ChangePin)
        self.label_3.setGeometry(QtCore.QRect(40, 320, 120, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(ChangePin)
        self.lineEdit.setGeometry(QtCore.QRect(170, 270, 151, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(ChangePin)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 320, 151, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(ChangePin)
        self.pushButton.setGeometry(QtCore.QRect(130, 390, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(ChangePin)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 430, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(ChangePin)
        QtCore.QMetaObject.connectSlotsByName(ChangePin)

    def retranslateUi(self, ChangePin):
        _translate = QtCore.QCoreApplication.translate
        ChangePin.setWindowTitle(_translate("ChangePin", "Form"))
        self.label.setText(_translate("ChangePin", "ChangePin"))
        self.label_2.setText(_translate("ChangePin", "NEW PIN"))
        self.label_3.setText(_translate("ChangePin", "CONFIRM NEW PIN"))
        self.pushButton.setText(_translate("ChangePin", "CONFIRM"))
        self.pushButton_2.setText(_translate("ChangePin", "BACK"))
