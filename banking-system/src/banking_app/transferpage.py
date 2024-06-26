from PyQt5 import QtCore, QtWidgets


class Ui_Transfer(object):
    def setupUi(self, Transfer):
        Transfer.setObjectName("Transfer")
        Transfer.resize(401, 693)
        Transfer.setMinimumSize(QtCore.QSize(401, 693))
        Transfer.setMaximumSize(QtCore.QSize(401, 693))
        self.label = QtWidgets.QLabel(Transfer)
        self.label.setGeometry(QtCore.QRect(150, 190, 71, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Transfer)
        self.label_2.setGeometry(QtCore.QRect(40, 270, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Transfer)
        self.label_3.setGeometry(QtCore.QRect(40, 320, 111, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Transfer)
        self.lineEdit.setGeometry(QtCore.QRect(160, 270, 151, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Transfer)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 320, 151, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Transfer)
        self.pushButton.setGeometry(QtCore.QRect(130, 390, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Transfer)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 430, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Transfer)
        QtCore.QMetaObject.connectSlotsByName(Transfer)

    def retranslateUi(self, Transfer):
        _translate = QtCore.QCoreApplication.translate
        Transfer.setWindowTitle(_translate("Transfer", "Form"))
        self.label.setText(_translate("Transfer", "TRANSFER"))
        self.label_2.setText(_translate("Transfer", "RECEIVER"))
        self.label_3.setText(_translate("Transfer", "AMOUNT(YUAN)"))
        self.pushButton.setText(_translate("Transfer", "CONFIRM"))
        self.pushButton_2.setText(_translate("Transfer", "BACK"))
