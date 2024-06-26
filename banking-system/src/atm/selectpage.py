from PyQt5 import QtCore, QtWidgets, QtGui

class Ui_SelectPage(object):
    def setupUi(self, SelectPage):
        SelectPage.setObjectName("SelectPage")
        SelectPage.setGeometry(QtCore.QRect(0, 0, 841, 491))  # 保持与 DisplayWidget 一致的大小

        self.stackedWidget = QtWidgets.QStackedWidget(SelectPage)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 841, 491))
        self.stackedWidget.setObjectName("stackedWidget")

        self.selectPage = QtWidgets.QWidget()
        self.selectPage.setObjectName("selectPage")

        self.label = QtWidgets.QLabel(self.selectPage)
        self.label.setGeometry(QtCore.QRect(200, 170, 441, 51))  # 屏幕中央
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("Please choose service")

        self.transfer = QtWidgets.QPushButton(self.selectPage)
        self.transfer.setGeometry(QtCore.QRect(50, 150, 150, 50))  # 左上
        self.transfer.setObjectName("pushButton")
        self.transfer.setFocusPolicy(QtCore.Qt.NoFocus)

        self.query = QtWidgets.QPushButton(self.selectPage)
        self.query.setGeometry(QtCore.QRect(50, 220, 150, 50))  # 左下
        self.query.setObjectName("query")
        self.query.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.changepin = QtWidgets.QPushButton(self.selectPage)
        self.changepin.setGeometry(QtCore.QRect(641, 150, 150, 50))  # 右上
        self.changepin.setObjectName("changepin")
        self.changepin.setFocusPolicy(QtCore.Qt.NoFocus)

        self.closeaccount = QtWidgets.QPushButton(self.selectPage)
        self.closeaccount.setGeometry(QtCore.QRect(641, 220, 150, 50))  # 右下
        self.closeaccount.setObjectName("closeaccount")
        self.closeaccount.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.ReturnCard = QtWidgets.QPushButton(self.selectPage)
        self.ReturnCard.setGeometry(QtCore.QRect(641, 420, 150, 50))  # 屏幕中央
        self.ReturnCard.setObjectName("ReturnCard")
        self.ReturnCard.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.DepositCash = QtWidgets.QPushButton(self.selectPage)  # Deposit Cash
        self.DepositCash.setGeometry(QtCore.QRect(50, 290, 150, 50))  # 屏幕左侧中央
        self.DepositCash.setObjectName("DepositCash")
        self.DepositCash.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.WithdrawCash = QtWidgets.QPushButton(self.selectPage)  # Withdraw Cash
        self.WithdrawCash.setGeometry(QtCore.QRect(641, 290, 150, 50))  # 屏幕右侧中央
        self.WithdrawCash.setObjectName("WithdrawCash")
        self.WithdrawCash.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.stackedWidget.addWidget(self.selectPage)

        self.retranslateUi(SelectPage)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SelectPage)

    def retranslateUi(self, SelectPage):
        _translate = QtCore.QCoreApplication.translate
        SelectPage.setWindowTitle(_translate("SelectPage", "Select Action"))
        self.transfer.setText(_translate("SelectPage", "Transfer"))
        self.query.setText(_translate("SelectPage", "Query"))
        self.changepin.setText(_translate("SelectPage", "Change PIN"))
        self.closeaccount.setText(_translate("SelectPage", "Close Account"))
        self.ReturnCard.setText(_translate("SelectPage", "Return Card"))
        self.DepositCash.setText(_translate("SelectPage", "Deposit Cash"))
        self.WithdrawCash.setText(_translate("SelectPage", "Withdraw Cash"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     SelectPage = QtWidgets.QWidget()
#     ui = Ui_SelectPage()
#     ui.setupUi(SelectPage)
#     SelectPage.show()
#     sys.exit(app.exec_())
