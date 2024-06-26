from PyQt5 import QtCore, QtWidgets

class Ui_SelectPage(object):
    def setupUi(self, SelectPage):
        SelectPage.setObjectName("SelectPage")
        SelectPage.resize(401, 693)
        SelectPage.setMinimumSize(QtCore.QSize(401, 693))
        SelectPage.setMaximumSize(QtCore.QSize(401, 693))

        self.stackedWidget = QtWidgets.QStackedWidget(SelectPage)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 401, 693))
        self.stackedWidget.setObjectName("stackedWidget")

        self.selectPage = QtWidgets.QWidget()
        self.selectPage.setObjectName("selectPage")

        self.pushButton = QtWidgets.QPushButton(self.selectPage)
        self.pushButton.setGeometry(QtCore.QRect(30, 230, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.pushButton_2 = QtWidgets.QPushButton(self.selectPage)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 290, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.pushButton_3 = QtWidgets.QPushButton(self.selectPage)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 230, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)

        self.pushButton_4 = QtWidgets.QPushButton(self.selectPage)
        self.pushButton_4.setGeometry(QtCore.QRect(200, 290, 113, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.stackedWidget.addWidget(self.selectPage)

        self.retranslateUi(SelectPage)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SelectPage)

    def retranslateUi(self, SelectPage):
        _translate = QtCore.QCoreApplication.translate
        SelectPage.setWindowTitle(_translate("SelectPage", "Form"))
        self.pushButton.setText(_translate("SelectPage", "transfer"))
        self.pushButton_2.setText(_translate("SelectPage", "query"))
        self.pushButton_3.setText(_translate("SelectPage", "change pin"))
        self.pushButton_4.setText(_translate("SelectPage", "log out"))


