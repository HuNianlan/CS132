import sys
from PyQt5 import QtWidgets
from banking_app.app_ui import Ui_APP_UI
from atm.atm_ui import Ui_ATM
from processor import my_processor
from DB import reset
import time
from typing import Dict
from unittest.mock import patch
from PyQt5.QtWidgets import *
from PyQt5.QtTest import QTest
# requests  = ["create_account@222222",
#             #    "deposit_cash@1320",
#                "deposit_cash@1500",
#                 "open_app",
#                 "open_app",
#                 "log_in@2023123456@111111#1"]



class Simulator():
    def __init__(self,MainWindow, processor = my_processor):
        reset()
        self.processor = my_processor
        self.ui_atm = Ui_ATM(MainWindow, my_processor)
        self.applist:Dict[str,Ui_APP_UI] = {}
    
    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    def simulate(self, serverMessage,mock_info, mock_warning,mock_question):
        if serverMessage.startswith("create_account@"):
            return self.create_account(serverMessage.split("@")[1])
        if serverMessage == "close_account":
            return self.close_account()
        if serverMessage.startswith("deposit_cash@"):
            return self.deposit_cash(serverMessage.split("@")[1])
        if serverMessage.startswith("withdraw_cash@"):
            return self.withdraw_cash(serverMessage.split("@")[1], serverMessage.split("@")[2])
        if serverMessage == "open_app":
            return self.open_app()
        if serverMessage.startswith("close_app#"):
            # print(self.close_app(serverMessage.split("#")[1]))
            return self.close_app(serverMessage.split("#")[1])
        if serverMessage.startswith("log_in@"):
            return self.log_in(serverMessage.split("@")[1], serverMessage.split("@")[2].split("#")[0], serverMessage.split("#")[1])
        if serverMessage.startswith("log_out#"):
            return self.log_out(serverMessage.split("#")[1])
        if serverMessage.startswith("transfer_money@"):
            return self.transfer_money(serverMessage.split("@")[1], serverMessage.split("@")[2].split("#")[0], serverMessage.split("#")[1] if "#" in serverMessage else None)
        if serverMessage.startswith("change_password@"):
            return self.change_password(serverMessage.split("@")[1].split("#")[0], serverMessage.split("#")[1] if "#" in serverMessage else None)
        if serverMessage.startswith("query"):
            return self.query(serverMessage.split("#")[1] if "#" in serverMessage else None)
        if serverMessage == "return_card":
            return self.return_card()
        if serverMessage.startswith("insert_card@"):
            return self.insert_card(serverMessage.split("@")[1])
        
        return "failed@invalid_command"
    
    def open_app(self):
        self.processor.process("open_app")
        # new_app_name = f"App {my_processor.app_count}"
        self.applist[self.processor.app_count] = Ui_APP_UI(self.processor,self.processor.app_count)
        self.applist[self.processor.app_count].show()
    

    def create_account(self,password):
        if self.ui_atm.display_widget.stacked_layout.currentWidget() ==  self.ui_atm.display_widget.EntryPage:
            self.ui_atm.create_account(password)
        else:
            return("failed")
    

    def close_account(self):
        if self.ui_atm.display_widget.stacked_layout.currentWidget() == self.ui_atm.selectPage:
            self.ui_atm.ui_SelectPage.closeaccount.click()
            return("success")
        else:
            return("failed")

    def deposit_cash(self,amount):
        if self.ui_atm.display_widget.stacked_layout.currentWidget() == self.ui_atm.selectPage:
            if(amount.isdigit()):
                self.ui_atm.my_ATM.deposit_amount = int(amount)
                self.ui_atm.ui_deposit_cash.label_2.setText(f"Deposit Amount: {amount}")
            else:
                return
            self.ui_atm.ui_SelectPage.DepositCash.click()
            # self.ui_atm.my_ATM.deposit_amount = amount
            QTest.qWait(1000)
            self.ui_atm.ui_deposit_cash.pushButton.click()
            QTest.qWait(1000)
            # if self.ui_atm.display_widget.stacked_layout.currentWidget() == self.ui_atm.depositCashPage:
            #     self.ui_atm.ui_deposit_cash.pushButton_2.click()

    def withdraw_cash(self,amount,password):
        if self.ui_atm.display_widget.stacked_layout.currentWidget() == self.ui_atm.selectPage:
            if(amount.isdigit()):
                self.ui_atm.ui_withdraw_cash.lineEdit.setText(amount)
            else:
                return
            self.ui_atm.ui_SelectPage.WithdrawCash.click()
            QTest.qWait(1000)            
            self.ui_atm.withdraw_cash(amount,password)
            self.ui_atm.ui_withdraw_cash.pushButton.click()
            return("success")
        else:
            return("failed")
        
        
    def close_app(self,id):
        self.applist[int(id)].close()

    def log_in(self, account_id, password, app_id):
        if self.applist[int(app_id)].stackedWidget.currentWidget() == self.applist[int(app_id)].loginPage:
            self.applist[int(app_id)].ui_loginPage.lineEdit.setText(account_id)
            self.applist[int(app_id)].ui_loginPage.lineEdit_2.setText(password)
            QTest.qWait(1000)
            self.applist[int(app_id)].ui_loginPage.pushButton_3.click()
            QTest.qWait(1000)
            return("success")
        else:
            return("failed@log_in#"+app_id)

    def log_out(self,app_id):
        if self.applist[int(app_id)].stackedWidget.currentWidget() == self.applist[int(app_id)].selectPage:
            self.applist[int(app_id)].ui_SelectPage.pushButton_4.click()
            return("success")
        else:
            return("failed@log_out#"+app_id)

    
    def transfer_money(self, receiver_id, transfer_amount, app_id=None):
        # print(app_id)
        if app_id == None:
            if self.ui_atm.display_widget.stacked_layout.currentWidget() == self.ui_atm.selectPage:
                self.ui_atm.ui_transfer.lineEdit.setText(receiver_id)
                self.ui_atm.ui_transfer.lineEdit_2.setText(transfer_amount)
                self.ui_atm.ui_SelectPage.transfer.click()
                QTest.qWait(1000)
                self.ui_atm.ui_transfer.pushButton.click()
                QTest.qWait(1000)
                return("success")
            else:
                return("failed@transfer_money")
        else:
            # print(type(self.applist[int(app_id)].stackedWidget.currentWidget()))
            if self.applist[int(app_id)].stackedWidget.currentWidget() == self.applist[int(app_id)].selectPage:
                self.applist[int(app_id)].ui_transfer.lineEdit.setText(receiver_id)
                self.applist[int(app_id)].ui_transfer.lineEdit_2.setText(transfer_amount)
                self.applist[int(app_id)].ui_SelectPage.pushButton.click()
                QTest.qWait(1000)
                self.applist[int(app_id)].ui_transfer.pushButton.click()
                QTest.qWait(1000)
                return("success")
            else:
                return("failed@transfer_money#"+app_id)
       
    def change_password(self,new_password, app_id):
        if app_id == None:
            if self.ui_atm.display_widget.stacked_layout.currentWidget() == self.ui_atm.selectPage:
                self.ui_atm.ui_change_pin.lineEdit.setText(new_password)
                self.ui_atm.ui_change_pin.lineEdit_2.setText(new_password)
                self.ui_atm.ui_SelectPage.changepin.click()
                QTest.qWait(1000)
                self.ui_atm.ui_change_pin.pushButton.click()
                QTest.qWait(1000)
                return("success")
            else:
                return("failed@change_password")
        else:
            if self.applist[int(app_id)].stackedWidget.currentWidget() == self.applist[int(app_id)].selectPage:
                self.applist[int(app_id)].ui_changePin.lineEdit.setText(new_password)
                self.applist[int(app_id)].ui_changePin.lineEdit_2.setText(new_password)
                self.applist[int(app_id)].ui_SelectPage.pushButton_3.click()
                QTest.qWait(1000)
                self.applist[int(app_id)].ui_changePin.pushButton.click()
                QTest.qWait(1000)
                return("success")
            else:
                return("failed@change_password#"+app_id)
    
    
    def query(self,app_id):
        if app_id == None:
            if self.ui_atm.display_widget.stacked_layout.currentWidget() == self.ui_atm.selectPage:
                self.ui_atm.ui_SelectPage.query.click()
                QTest.qWait(1000)
                self.ui_atm.ui_query.pushButton_2.click()
                return("success")
            else:
                return("failed@query")
        else:
            if self.applist[int(app_id)].stackedWidget.currentWidget() == self.applist[int(app_id)].selectPage:
                self.applist[int(app_id)].ui_SelectPage.pushButton_2.click()
                QTest.qWait(1000)
                self.applist[int(app_id)].ui_query.pushButton_2.click()
                return("success")
            else:
                return("failed@transfer_money#"+app_id)

    
    def return_card(self):
        if self.ui_atm.display_widget.stacked_layout.currentWidget() == self.ui_atm.selectPage:
            self.ui_atm.ui_SelectPage.ReturnCard.click()
            return("success")
        else:
            return("failed@return_card")
        
    def insert_card(self,account_id):
        if self.ui_atm.toolButton.isEnabled():
            self.ui_atm.insert_card(account_id)
            return("success")
        else:
            return("failed@insert_card")
        

def autotest(STRING_LIST):
    reset()

    app = QtWidgets.QApplication(sys.argv)

    # Create ATM window
    MainWindow = QtWidgets.QMainWindow()
    sim = Simulator(MainWindow)
    MainWindow.show()

    for request in STRING_LIST:
        sim.simulate(request)

    app.lastWindowClosed.connect(app.quit)
    sys.exit(app.exec_())



# if __name__=='__main__':
#     initial()