from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from atm.NumberPage import NumberPadWidget
from atm.InsertCardCash import CardInputDialog,CashInputDialog
from atm.selectpage import Ui_SelectPage
from atm.transferpage import Ui_Transfer
from atm.ChangePinPage import Ui_ChangePin
from atm.DepositCash import Ui_DepositCash
from atm.WithdrawCashPage import Ui_WithdrawCash
from atm.querypage import Ui_Query
from atm.CreateAccount import WelcomePage
from atm.atm import ATM
from atm.CheckPINpage import CheckPINPage

class DisplayWidget(QtWidgets.QWidget):
    def __init__(self,number_pad_widget,parent=None,):
        super(DisplayWidget, self).__init__(parent)
        self.initUI()
        self.number_pad_widget = number_pad_widget
    def initUI(self):
        self.stacked_layout = QtWidgets.QStackedLayout(self)

        self.EntryPage = WelcomePage()
        self.stacked_layout.addWidget(self.EntryPage)

        self.setLayout(self.stacked_layout)
    
    def register_focus_events(self):
        current_widget = self.stacked_layout.currentWidget()
        for widget in current_widget.findChildren(QtWidgets.QLineEdit):
            widget.installEventFilter(self)
            # self.number_pad_widget = number_pad_widget

    def eventFilter(self, obj, event):
        if isinstance(obj, QtWidgets.QLineEdit) and event.type() == QtCore.QEvent.FocusIn:
            if not obj.isReadOnly():
                self.number_pad_widget.set_current_line_edit(obj)
        return super().eventFilter(obj, event)



class Ui_ATM(QtWidgets.QWidget):
    def __init__(self,MainWindow, processor,atm_cash = 800000):
        super().__init__()
        self.setupUi(MainWindow,processor)
        self.processor.query_result_signal.connect(self.handle_query)
        self.display_widget.stacked_layout.setCurrentWidget(self.display_widget.EntryPage)
        self.my_ATM = ATM(atm_cash)
        self.ui_deposit_cash.label_2.setText(f"Deposit Amount: {self.my_ATM.deposit_amount}")
        self.account_id = None
    
    def setupUi(self,MainWindow,processor):
        MainWindow.setObjectName("ATM")
        MainWindow.resize(842, 981)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(480, 500, 351, 41))
        self.toolButton.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.toolButton.setText("Insert Card")
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.handle_insert_card)
        
        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setGeometry(QtCore.QRect(10, 500, 441, 41))
        self.toolButton_2.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.toolButton_2.setMouseTracking(False)
        self.toolButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.toolButton_2.setText("Cash Box for deposit")
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_2.clicked.connect(self.collectCash)

        
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(0, 0, 841, 491))
        self.listView.setObjectName("listView")
        
        self.listView_2 = QtWidgets.QListView(self.centralwidget)
        self.listView_2.setGeometry(QtCore.QRect(200, 550, 350, 360))
        self.listView_2.setObjectName("listView_2")



        # Add NumberPadWidget at the position of listView_2
        self.number_pad_widget = NumberPadWidget(self.centralwidget)
        self.number_pad_widget.setGeometry(QtCore.QRect(200, 550, 500, 600))
        


        # Add DisplayWidget at the position of listView
        self.display_widget = DisplayWidget(self.number_pad_widget,self.centralwidget)
        self.display_widget.setGeometry(QtCore.QRect(0, 0, 841, 491))

        # self.display_widget.register_focus_events()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 842, 37))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.selectPage = QtWidgets.QWidget()
        self.ui_SelectPage = Ui_SelectPage()
        self.ui_SelectPage.setupUi(self.selectPage)
        self.display_widget.stacked_layout.addWidget(self.selectPage)

        self.transferPage = QtWidgets.QWidget()
        self.transferPage.setObjectName("transferPage")
        self.ui_transfer = Ui_Transfer()
        self.ui_transfer.setupUi(self.transferPage)
        self.display_widget.stacked_layout.addWidget(self.transferPage)


        self.changePinPage = QtWidgets.QWidget()
        self.ui_change_pin = Ui_ChangePin()
        self.ui_change_pin.setupUi(self.changePinPage)
        self.display_widget.stacked_layout.addWidget(self.changePinPage)

        self.depositCashPage = QtWidgets.QWidget()
        self.ui_deposit_cash = Ui_DepositCash()
        self.ui_deposit_cash.setupUi(self.depositCashPage)
        self.display_widget.stacked_layout.addWidget(self.depositCashPage)


        self.withdrawCashPage = QtWidgets.QWidget()
        self.ui_withdraw_cash = Ui_WithdrawCash()
        self.ui_withdraw_cash.setupUi(self.withdrawCashPage)
        self.display_widget.stacked_layout.addWidget(self.withdrawCashPage)

        self.queryPage = QtWidgets.QWidget()
        self.ui_query = Ui_Query()
        self.ui_query.setupUi(self.queryPage)
        self.display_widget.stacked_layout.addWidget(self.queryPage)
        
        # self.checkPINPage = QtWidgets.QWidget()
        # self.ui_check_pin = Ui_CheckPINPage()
        # self.ui_check_pin.setupUi(self.checkPINPage)
        # self.display_widget.stacked_layout.addWidget(self.checkPINPage)

        self.display_widget.EntryPage.create_account_button.clicked.connect(self.handle_create_account)


        # 点击切换相应的页面
        self.ui_SelectPage.transfer.clicked.connect(lambda: self.display_widget.stacked_layout.setCurrentWidget(self.transferPage))
        self.ui_SelectPage.transfer.clicked.connect(lambda:self.display_widget.register_focus_events())

        self.ui_SelectPage.DepositCash.clicked.connect(lambda: self.display_widget.stacked_layout.setCurrentWidget(self.depositCashPage))
        self.ui_SelectPage.DepositCash.clicked.connect(lambda:self.display_widget.register_focus_events())

        self.ui_SelectPage.WithdrawCash.clicked.connect(lambda: self.display_widget.stacked_layout.setCurrentWidget(self.withdrawCashPage))
        self.ui_SelectPage.WithdrawCash.clicked.connect(lambda:self.display_widget.register_focus_events())

        self.ui_SelectPage.changepin.clicked.connect(lambda: self.display_widget.stacked_layout.setCurrentWidget(self.changePinPage))
        self.ui_SelectPage.changepin.clicked.connect(lambda:self.display_widget.register_focus_events())

        self.ui_SelectPage.query.clicked.connect(lambda:self.processor.process("query"))
        self.ui_SelectPage.ReturnCard.clicked.connect(self.handle_return_card)

        self.ui_SelectPage.closeaccount.clicked.connect(self.handle_close_account)
        
        
        #back button
        self.ui_transfer.pushButton_2.clicked.connect(self.go_to_selectPage)
        self.ui_change_pin.pushButton_2.clicked.connect(self.go_to_selectPage)
        self.ui_query.pushButton_2.clicked.connect(lambda:self.display_widget.stacked_layout.setCurrentWidget(self.selectPage))
        self.ui_deposit_cash.pushButton_2.clicked.connect(self.go_to_selectPage)
        self.ui_withdraw_cash.pushButton_2.clicked.connect(self.go_to_selectPage)


        self.ui_transfer.pushButton.clicked.connect(self.handle_transfer)
        self.ui_change_pin.pushButton.clicked.connect(self.handle_change_pin)
        self.ui_deposit_cash.pushButton.clicked.connect(self.handle_deposit_cash)
        self.ui_withdraw_cash.pushButton.clicked.connect(self.handle_withdraw_cash)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.ui_check_pin.backButton.clicked.connect(self.handle_back_button)
        # self.ui_check_pin.confirmButton.clicked.connect(self.handle_confirm_button)

        self.ui_deposit_cash.label_2.setReadOnly(True)
        self.processor = processor

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("ATM", "ATM"))


    def checkPIN(self,card_id = None):
        '''Call out the checkPIN page to ensure security.'''
        if card_id == None:
            card_id = self.account_id
        self.check_page = CheckPINPage(self.processor,card_id)
        result = self.check_page.exec_()
        return result == QDialog.Accepted
    
    def handle_insert_card(self):
        dialog = CardInputDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            card_id = dialog.get_card_id()
            if not self.checkPIN(card_id):
                return
            self.insert_card(card_id)


    def insert_card(self,card_id):
        receive_message = self.processor.process("insert_card@"+card_id)
        # self.display_widget.update_display(f"Card Number: {card_number}")
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "Card Insert Failed", "Invalid ID")
        else:
            # self.display_widget.enable_eject_button()
            self.account_id = card_id
            self.toolButton.setEnabled(False)
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)

    def handle_return_card(self):
        receive_message = self.processor.process("return_card")
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "Return Failed", "Error")
        else:
            self.account_id = None
            self.toolButton.setEnabled(True)
            self.display_widget.stacked_layout.setCurrentWidget(self.display_widget.EntryPage)


    def handle_change_pin(self):
        new_pin = self.ui_change_pin.lineEdit.text()
        new_pin2  = self.ui_change_pin.lineEdit_2.text()
        if new_pin != new_pin2:
            QtWidgets.QMessageBox.information(None,"inconsistent new pin","you should enter consistent new pins")
            return
        
        receive_message = self.processor.process("change_password@"+new_pin)
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "ChangePin Failed", "Invalid NEW PIN")
            self.ui_change_pin.lineEdit.clear()
            self.ui_change_pin.lineEdit_2.clear()
            self.ui_change_pin.lineEdit.setFocus()
            # self.stackedWidget.setCurrentWidget(self.selectPage)
        else:
            QtWidgets.QMessageBox.information(None,"ChangePin succeeded!","SUCCEED")
            self.ui_change_pin.lineEdit.clear()
            self.ui_change_pin.lineEdit_2.clear()
            self.ui_change_pin.lineEdit.setFocus()
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)


    def handle_query(self,results):
        result = results[0]
        if results[1] != None:
            return
        if result:
            result_text = (
                f"Account ID: {result['account_id']}\n"
                f"Balance: {result['balance']}\n"
                f"Creation Time: {result['creation_time']}"
            )
        else:
            result_text = "Account not found"
        self.ui_query.label_3.setText(result_text)
        self.display_widget.stacked_layout.setCurrentWidget(self.queryPage)

    def handle_transfer(self):
        receiver_id = self.ui_transfer.lineEdit.text()
        amount  = self.ui_transfer.lineEdit_2.text()
        if(not amount.isdigit() or (amount.isdigit() and int(amount) == 0)):
            QtWidgets.QMessageBox.warning(None, "transfer Failed", "Invalid amount")
            self.ui_transfer.lineEdit.clear()
            self.ui_transfer.lineEdit_2.clear()
            self.ui_transfer.lineEdit.setFocus()
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
            return
        receive_message = self.processor.process("transfer_money@"+receiver_id+"@"+amount)
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "transfer Failed", "Invalid receiver or lacking balane")
            self.ui_transfer.lineEdit.clear()
            self.ui_transfer.lineEdit_2.clear()
            self.ui_transfer.lineEdit.setFocus()
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
        else:
            QtWidgets.QMessageBox.information(None,"transfer succeeded!","SUCCEED")
            self.ui_transfer.lineEdit.clear()
            self.ui_transfer.lineEdit_2.clear()
            self.ui_transfer.lineEdit.setFocus()
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)

    def handle_deposit_cash(self):
        amount = str(self.my_ATM.deposit_amount)
        if int(amount) % 100 != 0 or int(amount) == 0:
            QtWidgets.QMessageBox.warning(self, "deposit Failed", "Invalid amount")
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
            return

        self.ui_deposit_cash.label_2.setText(f"Deposit Amount: {amount}")
        receive_message = self.processor.process("deposit_cash@"+amount)
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "deposit Failed", "Invalid amount")
        else:
            QtWidgets.QMessageBox.information(None,"deposit succeeded!","SUCCEED")
            self.ATM_cashupdate(int(amount))
            self.my_ATM.deposit_amount = 0

            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
            self.ui_deposit_cash.label_2.setText(f"Deposit Amount: {self.my_ATM.deposit_amount}")


    def handle_withdraw_cash(self):         
        amount = self.ui_withdraw_cash.lineEdit.text()
        if not amount.isdigit():
            self.ui_withdraw_cash.lineEdit.clear()
            self.ui_withdraw_cash.lineEdit.setFocus()
            QtWidgets.QMessageBox.warning(None, "Invalid amount", "You should enter correct amount!")
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
            return
        if amount == "" or int(amount) == 0:
            self.ui_withdraw_cash.lineEdit.clear()
            self.ui_withdraw_cash.lineEdit.setFocus()
            QtWidgets.QMessageBox.warning(None, "Invalid amount", "You should enter correct amount!")
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
            return
        #Error! Sorry!ATM is out of money.
        if int(amount) > self.my_ATM.cash:
            QtWidgets.QMessageBox.warning(None, "ATM Out of Money", "Sorry! ATM is out of money.")
            self.ui_withdraw_cash.lineEdit.clear()
            self.ui_withdraw_cash.lineEdit.setFocus()
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
            return

        password, ok = QtWidgets.QInputDialog.getText(None, "Enter Password", "Please enter your password:", QtWidgets.QLineEdit.Password)
    
        if not ok:
            return
        self.withdraw_cash(amount,password)
        
    def withdraw_cash(self,amount,password):
        receive_message = self.processor.process("withdraw_cash@"+amount+"@"+password)
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "Withdraw Failed", "Invalid password or not enough balance")
            self.ui_withdraw_cash.lineEdit.clear()
            self.ui_withdraw_cash.lineEdit.setFocus()
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
        else:
            QtWidgets.QMessageBox.information(None,"Withdraw succeeded!","SUCCEED")
            self.ATM_cashupdate(-int(amount))
            self.ui_withdraw_cash.lineEdit.clear()
            self.ui_withdraw_cash.lineEdit.setFocus()
            self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
    
    
    def handle_create_account(self):
        password, ok = QtWidgets.QInputDialog.getText(None, "Set Password", "Please set your password:", QtWidgets.QLineEdit.Password)
        
        if not ok:
            return
        else:
            self.create_account(password)
        
    
    def create_account(self,password):
        receive_message = self.processor.process("create_account@"+password)
        if receive_message.startswith("fail"):
            QtWidgets.QMessageBox.warning(None, "Invalid password", "Your password should be 6 digits")
            return
        card_id = receive_message.split("@")[1]
        QtWidgets.QMessageBox.warning(None, "Accound Created", "Your account id is "+card_id)
        self.toolButton.setEnabled(False)
        self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
    

    def go_to_selectPage(self):
        current_widget = self.display_widget.stacked_layout.currentWidget()
        for line in current_widget.findChildren(QtWidgets.QLineEdit):
            if(not line.isReadOnly()):
                line.clear()
        self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)




    def handle_close_account(self):
        if self.confirm_close_account(3):
            ms:str = self.processor.process("close_account")
            # If all confirmations are successful, perform the account closure logic
            if ms.startswith("failed"):
                QtWidgets.QMessageBox.warning(self.display_widget,"Close Account failed","Account still has money.")
            else:
                self.display_widget.stacked_layout.setCurrentWidget(self.display_widget.EntryPage)
                QtWidgets.QMessageBox.information(self.display_widget,"Close Account","Succeed!")
                self.toolButton.setEnabled(True)

        else:
            QtWidgets.QMessageBox.information(self.display_widget,"Close Account","Account closure cancelled.")



    def confirm_close_account(self, count):
        # return True
        if count == 0:
            return True

        reply = QtWidgets.QMessageBox.question(None, 'Confirm Close Account',
                                               f'Are you sure you want to close your account? ({3 - count + 1}/3)',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            return self.confirm_close_account(count - 1)
        else:
            return False
        
    def collectCash(self):
        dialog = CashInputDialog()
        dialog.check_cash(str(self.my_ATM.deposit_amount))
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            if(not dialog.get_cash().isdigit()):
                return
            self.my_ATM.deposit_amount = int(dialog.get_cash())
            self.ui_deposit_cash.label_2.setText(f"Deposit Amount: {self.my_ATM.deposit_amount}")

    def ATM_cashupdate(self,amount):
        self.my_ATM.cash+=amount

    # def checkPIN(self):
    #     self.previous_page = self.display_widget.stacked_layout.currentWidget()
    #     self.display_widget.stacked_layout.setCurrentWidget(self.checkPINPage)

    # def handle_back_button(self):
    #     if self.previous_page:
    #         self.display_widget.stacked_layout.setCurrentWidget(self.previous_page)

    # def handle_confirm_button(self):
    #     entered_pin = self.ui_check_pin.pinEdit.text()
    #     if self.processor.check_password(self.account_id,entered_pin):
    #         self.display_widget.stacked_layout.setCurrentWidget(self.selectPage)
    #     else:
    #         QtWidgets.QMessageBox.warning(self, "Error", "Invalid PIN")

