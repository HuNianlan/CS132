# from PyQt5 import QtCore, QtWidgets, QtGui

# class Ui_CheckPINPage(object):
#     def setupUi(self, CheckPINPage):
#         CheckPINPage.setObjectName("CheckPINPage")
#         CheckPINPage.setGeometry(QtCore.QRect(0, 0, 841, 491))  # 调整为与显示屏一致的大小
#         CheckPINPage.setMinimumSize(QtCore.QSize(841, 491))
#         CheckPINPage.setMaximumSize(QtCore.QSize(841, 491))

#         self.label = QtWidgets.QLabel(CheckPINPage)
#         self.label.setGeometry(QtCore.QRect(320, 100, 201, 41))  # 调整位置，放在上半部分中央
#         font = QtGui.QFont()
#         font.setPointSize(20)
#         self.label.setFont(font)
#         self.label.setAlignment(QtCore.Qt.AlignCenter)  # 将文本居中对齐
#         self.label.setObjectName("label")

#         self.pinEdit = QtWidgets.QLineEdit(CheckPINPage)
#         self.pinEdit.setGeometry(QtCore.QRect(250, 200, 341, 41))  # 调整位置和大小，放在中间
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.pinEdit.setFont(font)
#         self.pinEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # 将输入模式设置为密码模式
#         self.pinEdit.setAlignment(QtCore.Qt.AlignCenter)  # 将文本居中对齐
#         self.pinEdit.setObjectName("pinEdit")

#         self.confirmButton = QtWidgets.QPushButton(CheckPINPage)
#         self.confirmButton.setGeometry(QtCore.QRect(300, 300, 121, 41))  # 调整位置，放在下半部分中央
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.confirmButton.setFont(font)
#         self.confirmButton.setObjectName("confirmButton")

#         self.backButton = QtWidgets.QPushButton(CheckPINPage)
#         self.backButton.setGeometry(QtCore.QRect(300, 350, 121, 41))  # 调整位置，放在下半部分中央
#         font = QtGui.QFont()
#         font.setPointSize(14)
#         self.backButton.setFont(font)
#         self.backButton.setObjectName("backButton")

#         self.retranslateUi(CheckPINPage)
#         QtCore.QMetaObject.connectSlotsByName(CheckPINPage)

#     def retranslateUi(self, CheckPINPage):
#         _translate = QtCore.QCoreApplication.translate
#         CheckPINPage.setWindowTitle(_translate("CheckPINPage", "Check PIN"))
#         self.label.setText(_translate("CheckPINPage", "Enter PIN"))
#         self.confirmButton.setText(_translate("CheckPINPage", "CONFIRM"))
#         self.backButton.setText(_translate("CheckPINPage", "BACK"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     CheckPINPage = QtWidgets.QWidget()
#     ui = Ui_CheckPINPage()
#     ui.setupUi(CheckPINPage)
#     CheckPINPage.show()
#     sys.exit(app.exec_())


from PyQt5.QtWidgets import *

class CheckPINPage(QDialog):
    '''
    This is a class for Page to Check PIN.

    CheckPINPage class create a window to check PIN and reply corresponding information.

    Attributes:
        processor:   A InjectProcessor class to process all the functions.
        times:  An int of attempting times left to check.
    '''

    def __init__(self, processor,id):
        super().__init__()
        self.processor = processor
        self.times = 3
        self.accout_id = id
        self.initUI()
    
    def initUI(self):
        self.setGeometry(200, 200, 450, 200)
        self.setWindowTitle('Check PIN')
        
        self.label = QLabel(f"Please enter the PIN:", self)
        # self.label = QLabel(f"Please enter the PIN ({self.times} times left):", self)
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

        if self.getProcessor().check_password(self.accout_id,entered_PIN):
            self.accept()
        else:
            # self.times = self.times - 1
            # if self.times > 0:
            QMessageBox.warning(self, "Wrong PIN", "Please type in correct PIN!")
            self.checkPIN.clear()
            self.label.setText(f"Please enter the PIN ({self.times} times left):")
            return
            # else:
            #     QMessageBox.critical(self, 'Error', 'No attempts left, PIN check failed!')
            #     self.reject()
    
    def getProcessor(self):
        return self.processor
