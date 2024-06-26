from PyQt5 import QtCore, QtWidgets,QtGui

class Ui_DepositCash(object):
    def setupUi(self, DepositCash):
        DepositCash.setObjectName("DepositCash")
        DepositCash.setGeometry(QtCore.QRect(0, 0, 841, 491))  # 调整为与显示屏一致的大小
        DepositCash.setMinimumSize(QtCore.QSize(841, 491))
        DepositCash.setMaximumSize(QtCore.QSize(841, 491))
        
        self.label = QtWidgets.QLabel(DepositCash)
        self.label.setGeometry(QtCore.QRect(320, 100, 201, 41))  # 调整位置，放在上半部分中央
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLineEdit(DepositCash)
        self.label_2.setGeometry(QtCore.QRect(150, 220, 541, 41))  # 调整位置，放在中间
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        
        # self.lineEdit = QtWidgets.QLineEdit(DepositCash)
        # self.lineEdit.setGeometry(QtCore.QRect(150, 220, 311, 21))  # 调整位置和大小，放在中间
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # self.lineEdit.setFont(font)
        # self.lineEdit.setObjectName("lineEdit")
        
        self.pushButton = QtWidgets.QPushButton(DepositCash)
        self.pushButton.setGeometry(QtCore.QRect(300, 350, 121, 41))  # 调整位置，放在下半部分中央
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        self.pushButton_2 = QtWidgets.QPushButton(DepositCash)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 400, 121, 41))  # 调整位置，放在下半部分中央
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(DepositCash)
        QtCore.QMetaObject.connectSlotsByName(DepositCash)

    def retranslateUi(self, DepositCash):
        _translate = QtCore.QCoreApplication.translate
        DepositCash.setWindowTitle(_translate("DepositCash", "Deposit Cash"))
        self.label.setText(_translate("DepositCash", "Deposit Cash"))
        # self.label_2.setText(_translate("DepositCash", "Deposit Amount"))
        self.pushButton.setText(_translate("DepositCash", "CONFIRM"))
        self.pushButton_2.setText(_translate("DepositCash", "BACK"))
