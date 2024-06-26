from PyQt5 import QtCore, QtWidgets
from banking_app.LogInPage import Ui_LoginPage
from banking_app.selectpage import Ui_SelectPage
from banking_app.transferpage import Ui_Transfer
from banking_app.querypage import Ui_Query
from banking_app.ChangePinPage import Ui_ChangePin
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton

class Ui_APP_UI(QtWidgets.QWidget):
    # query_result_signal = QtCore.pyqtSignal(dict)

    def __init__(self, processor,app_id = None,main_board = None):
        super().__init__()
        self.app_id = app_id
        self.main_board = main_board
        self.setupUi(self, processor)
        self.processor.query_result_signal.connect(self.handle_query)
        self.processor.log_out_signal.connect(self.compusary_log_out)
        # self.stackedWidget.setCurrentWidget(self.selectPage)


    
    def setupUi(self, app_default, processor):
        app_default.setObjectName("app_default")
        app_default.resize(401, 693)
        app_default.setMinimumSize(QtCore.QSize(401, 693))
        app_default.setMaximumSize(QtCore.QSize(401, 693))
        self.stackedWidget = QtWidgets.QStackedWidget(app_default)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 401, 693))
        self.stackedWidget.setObjectName("stackedWidget")
        
        
        main_layout = QVBoxLayout(self)

        main_layout.addWidget(self.stackedWidget)
        
        # top_layout = QHBoxLayout()

        # main_layout.addLayout(top_layout)
        # self.close_button = QPushButton("close_app")
        # top_layout.addWidget(self.close_button)
        # self.close_button.clicked.connect(self.handle_close_app)

        self.loginPage = QtWidgets.QWidget()
        self.ui_loginPage = Ui_LoginPage()
        self.ui_loginPage.setupUi(self.loginPage)
        self.stackedWidget.addWidget(self.loginPage)


        self.selectPage = QtWidgets.QWidget()
        self.ui_SelectPage = Ui_SelectPage()
        self.ui_SelectPage.setupUi(self.selectPage)
        self.stackedWidget.addWidget(self.selectPage)


        self.transferPage = QtWidgets.QWidget()
        self.transferPage.setObjectName("transferPage")
        self.ui_transfer = Ui_Transfer()
        self.ui_transfer.setupUi(self.transferPage)
        self.stackedWidget.addWidget(self.transferPage)

        self.queryPage = QtWidgets.QWidget()
        self.queryPage.setObjectName("queryPage")
        self.ui_query = Ui_Query()
        self.ui_query.setupUi(self.queryPage)
        self.stackedWidget.addWidget(self.queryPage)

        self.changePinPage = QtWidgets.QWidget()
        self.changePinPage.setObjectName("changePinPage")
        self.ui_changePin = Ui_ChangePin()
        self.ui_changePin.setupUi(self.changePinPage)
        self.stackedWidget.addWidget(self.changePinPage)
        

        self.ui_loginPage.pushButton_3.clicked.connect(self.handle_login)


        self.ui_SelectPage.pushButton.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.transferPage))
        self.ui_SelectPage.pushButton_2.clicked.connect(lambda:self.processor.process("query#"+str(self.app_id)))
        self.ui_SelectPage.pushButton_3.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.changePinPage))
        self.ui_SelectPage.pushButton_4.clicked.connect(self.handle_logout)
        
        #back button
        self.ui_transfer.pushButton_2.clicked.connect(self.back_to_select)
        self.ui_changePin.pushButton_2.clicked.connect(self.back_to_select)
        self.ui_query.pushButton_2.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.selectPage))

        self.ui_transfer.pushButton.clicked.connect(self.handle_transfer)
        self.ui_changePin.pushButton.clicked.connect(self.handle_changePin)


        self.retranslateUi(app_default)
        QtCore.QMetaObject.connectSlotsByName(app_default)

        self.processor = processor



    def retranslateUi(self, app_default):
        _translate = QtCore.QCoreApplication.translate
        app_default.setWindowTitle(_translate("app_default", "BANKING APP"))

    def handle_login(self):
        card_id = self.ui_loginPage.lineEdit.text()
        password = self.ui_loginPage.lineEdit_2.text()
        receive_message = self.processor.process("log_in@"+card_id+"@"+password+"#"+str(self.app_id))
        self.ui_loginPage.lineEdit.clear()
        self.ui_loginPage.lineEdit_2.clear()
        self.ui_loginPage.lineEdit.setFocus()
        # print(receive_message)
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "Login Failed", "Invalid ID or Password")
        else:
            self.stackedWidget.setCurrentWidget(self.selectPage)


    def handle_transfer(self):
        receiver_id = self.ui_transfer.lineEdit.text()
        amount  = self.ui_transfer.lineEdit_2.text()
        if(not amount.isdigit() or (amount.isdigit() and int(amount) == 0)):
            QtWidgets.QMessageBox.warning(None, "transfer Failed", "Invalid amount")
            self.ui_transfer.lineEdit.clear()
            self.ui_transfer.lineEdit_2.clear()
            self.ui_transfer.lineEdit.setFocus()
            self.stackedWidget.setCurrentWidget(self.selectPage)
            return
        receive_message = self.processor.process("transfer_money@"+receiver_id+"@"+amount+"#"+str(self.app_id))
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "transfer Failed", "Invalid receiver or lacking balance")
            self.ui_transfer.lineEdit.clear()
            self.ui_transfer.lineEdit_2.clear()
            self.ui_transfer.lineEdit.setFocus()
            self.stackedWidget.setCurrentWidget(self.selectPage)
        else:
            QtWidgets.QMessageBox.information(None,"transfer succeeded!","SUCCEED")
            self.ui_transfer.lineEdit.clear()
            self.ui_transfer.lineEdit_2.clear()
            self.ui_transfer.lineEdit.setFocus()
            self.stackedWidget.setCurrentWidget(self.selectPage)


    def handle_query(self,results):
        result = results[0]
        # print(results[1])
        # print(self.app_id)
        if results[1] == None or results[1] != str(self.app_id):
            return
        if result:
            result_text = (
                f"Account ID: {result['account_id']}\n"
                f"Balance: {result['balance']} YUAN\n"
                f"Creation Time: {result['creation_time']}"
            )
        else:
            result_text = "Account not found"
        self.ui_query.label_3.setText(result_text)
        self.stackedWidget.setCurrentWidget(self.queryPage)
    
    def handle_changePin(self):
        new_pin = self.ui_changePin.lineEdit.text()
        new_pin2  = self.ui_changePin.lineEdit_2.text()
        if new_pin != new_pin2:
            QtWidgets.QMessageBox.information(None,"inconsistent new pin","you should enter consistent new pins")
            return
        
        receive_message = self.processor.process("change_password@"+new_pin+"#"+str(self.app_id))
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "ChangePin Failed", "Invalid NEW PIN")
            self.ui_changePin.lineEdit.clear()
            self.ui_changePin.lineEdit_2.clear()
            self.ui_changePin.lineEdit.setFocus()
        else:
            QtWidgets.QMessageBox.information(None,"ChangePin succeeded!","SUCCEED")
            self.ui_changePin.lineEdit.clear()
            self.ui_changePin.lineEdit_2.clear()
            self.ui_changePin.lineEdit.setFocus()
            self.stackedWidget.setCurrentWidget(self.selectPage)

    
    def handle_logout(self):
        receive_message = self.processor.process("log_out#"+str(self.app_id))
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "Logout out", "app without login")
        else:
            self.stackedWidget.setCurrentWidget(self.loginPage)


    def back_to_select(self):
        current_widget = self.stackedWidget.currentWidget()
        for line in current_widget.findChildren(QtWidgets.QLineEdit):
            line.clear()
        self.stackedWidget.setCurrentWidget(self.selectPage)

    def compusary_log_out(self,aid):
        if aid == str(self.app_id):
            self.handle_logout()

    def set_app_id(self, app_id):
        self.app_id = app_id

    def handle_close_app(self):
        self.processor.process("close_app#" + str(self.app_id))

    def closeEvent(self, event):
        # print(type(event))
        self.processor.process("close_app#" + str(self.app_id))
        event.accept()