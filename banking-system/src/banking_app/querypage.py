from PyQt5 import QtCore, QtWidgets

class Ui_Query(object):
    def setupUi(self, Query):
        Query.setObjectName("Query")
        Query.resize(401, 693)
        Query.setMinimumSize(QtCore.QSize(401, 693))
        Query.setMaximumSize(QtCore.QSize(401, 693))
        self.label = QtWidgets.QLabel(Query)
        self.label.setGeometry(QtCore.QRect(140, 160, 131, 31))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Query)
        self.label_3.setGeometry(QtCore.QRect(80, 210, 251, 201))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(Query)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 430, 113, 32))
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
                f"Balance: {result['balance']}\n"
                f"Creation Time: {result['creation_time']}"
            )
        else:
            result_text = "Account not found"
        self.label_3.setText(result_text)