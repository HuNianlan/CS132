from PyQt5 import QtCore, QtWidgets,QtGui


class Ui_Transfer(object):
    def setupUi(self, Transfer):
        Transfer.setObjectName("Transfer")
        Transfer.resize(841, 491)  # 调整为与显示屏一致的大小
        Transfer.setMinimumSize(QtCore.QSize(841, 491))
        Transfer.setMaximumSize(QtCore.QSize(841, 491))
        self.label = QtWidgets.QLabel(Transfer)
        self.label.setGeometry(QtCore.QRect(350, 50, 141, 41))  # 调整位置，放在上半部分中央
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Transfer)
        self.label_2.setGeometry(QtCore.QRect(200, 150, 111, 31))  # 调整位置，放在中央偏上
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Transfer)
        self.label_3.setGeometry(QtCore.QRect(200, 210, 111, 31))  # 调整位置，放在中央偏下
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Transfer)
        self.lineEdit.setGeometry(QtCore.QRect(350, 150, 271, 31))  # 调整位置和大小
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Transfer)
        self.lineEdit_2.setGeometry(QtCore.QRect(350, 210, 271, 31))  # 调整位置和大小
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Transfer)
        self.pushButton.setGeometry(QtCore.QRect(300, 300, 141, 41))  # 调整位置，放在中央
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Transfer)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 360, 141, 41))  # 调整位置，放在中央
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Transfer)
        QtCore.QMetaObject.connectSlotsByName(Transfer)

    def retranslateUi(self, Transfer):
        _translate = QtCore.QCoreApplication.translate
        Transfer.setWindowTitle(_translate("Transfer", "Form"))
        self.label.setText(_translate("Transfer", "TRANSFER"))
        self.label_2.setText(_translate("Transfer", "RECEIVER"))
        self.label_3.setText(_translate("Transfer", "AMOUNT\n(YUAN)"))
        self.pushButton.setText(_translate("Transfer", "CONFIRM"))
        self.pushButton_2.setText(_translate("Transfer", "BACK"))
