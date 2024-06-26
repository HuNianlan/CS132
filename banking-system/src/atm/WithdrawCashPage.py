from PyQt5 import QtCore, QtWidgets,QtGui

class Ui_WithdrawCash(object):
    def setupUi(self, WithdrawCash):
        WithdrawCash.setObjectName("WithdrawCash")
        WithdrawCash.setGeometry(QtCore.QRect(0, 0, 841, 491))  # 调整为与显示屏一致的大小
        WithdrawCash.setMinimumSize(QtCore.QSize(841, 491))
        WithdrawCash.setMaximumSize(QtCore.QSize(841, 491))
        
        self.label = QtWidgets.QLabel(WithdrawCash)
        self.label.setGeometry(QtCore.QRect(320, 100, 201, 41))  # 调整位置，放在上半部分中央
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(WithdrawCash)
        self.label_2.setGeometry(QtCore.QRect(180, 200, 61, 16))  # 调整位置，放在中间
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        self.lineEdit = QtWidgets.QLineEdit(WithdrawCash)
        self.lineEdit.setGeometry(QtCore.QRect(150, 220, 311, 21))  # 调整位置和大小，放在中间
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        
        self.pushButton = QtWidgets.QPushButton(WithdrawCash)
        self.pushButton.setGeometry(QtCore.QRect(300, 350, 121, 41))  # 调整位置，放在下半部分中央
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        self.pushButton_2 = QtWidgets.QPushButton(WithdrawCash)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 400, 121, 41))  # 调整位置，放在下半部分中央
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(WithdrawCash)
        QtCore.QMetaObject.connectSlotsByName(WithdrawCash)

    def retranslateUi(self, WithdrawCash):
        _translate = QtCore.QCoreApplication.translate
        WithdrawCash.setWindowTitle(_translate("WithdrawCash", "Withdraw Cash"))
        self.label.setText(_translate("WithdrawCash", "Withdraw Cash"))
        self.label_2.setText(_translate("WithdrawCash", "Amount"))
        self.pushButton.setText(_translate("WithdrawCash", "CONFIRM"))
        self.pushButton_2.setText(_translate("WithdrawCash", "BACK"))
