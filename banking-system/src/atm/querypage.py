from PyQt5 import QtCore, QtWidgets,QtGui

class Ui_Query(object):
    def setupUi(self, Query):
        Query.setObjectName("Query")
        Query.resize(841, 491)  # 调整为与显示屏一致的大小
        Query.setMinimumSize(QtCore.QSize(841, 491))
        Query.setMaximumSize(QtCore.QSize(841, 491))
        self.label = QtWidgets.QLabel(Query)
        self.label.setGeometry(QtCore.QRect(320, 100, 201, 41))  # 调整位置，放在上半部分中央
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Query)
        self.label_3.setGeometry(QtCore.QRect(200, 180, 441, 201))  # 调整位置和大小，放在中间
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(Query)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 420, 141, 41))  # 调整位置，放在下半部分中央
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Query)
        QtCore.QMetaObject.connectSlotsByName(Query)

    def retranslateUi(self, Query):
        _translate = QtCore.QCoreApplication.translate
        Query.setWindowTitle(_translate("Query", "Form"))
        self.label.setText(_translate("Query", "Account Information"))
        self.pushButton_2.setText(_translate("Query", "BACK"))
    
    def display_result(self, result):
        if result:
            result_text = (
                f"Account ID: {result['account_id']}\n"
                f"Balance: {result['balance']} YUAN\n"
                f"Creation Time: {result['creation_time']}"
            )
        else:
            result_text = "Account not found"
        print(result_text)
        self.label_3.setText(result_text)
