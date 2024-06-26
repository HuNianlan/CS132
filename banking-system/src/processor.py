from PyQt5 import QtCore
from DB import create_account, check_account_exist, update_balance, check_password, check_is_valid, change_password, reset, check_enough_balance,query,close_account
import random

class Processor(QtCore.QObject):
    return_signal = QtCore.pyqtSignal(str)
    query_result_signal = QtCore.pyqtSignal(list)  
    log_out_signal = QtCore.pyqtSignal(str)  
    close_app_signal = QtCore.pyqtSignal(str)  
    def __init__(self):
        super().__init__()
        self.current_account = None
        self.account_available = False
        self.apps_account = {}
        self.apps_state = {}
        self.app_count = 0

    # def sendMessage_to_UI(self,message):
    #     self.return_signal.emit(self.process(message))

    def process(self, serverMessage):
        if serverMessage.startswith("create_account@"):
            rmsg = self.create_account(serverMessage.split("@")[1])
        elif serverMessage == "close_account":
            rmsg = self.close_account()
        elif serverMessage.startswith("deposit_cash@"):
            rmsg = self.deposit_cash(serverMessage.split("@")[1])
        elif serverMessage.startswith("withdraw_cash@"):
            rmsg = self.withdraw_cash(serverMessage.split("@")[1], serverMessage.split("@")[2])
        elif serverMessage == "open_app":
            rmsg = self.open_app()
        elif serverMessage.startswith("close_app#"):
            rmsg = self.close_app(serverMessage.split("#")[1])
        elif serverMessage.startswith("log_in@"):
            rmsg = self.log_in(serverMessage.split("@")[1], serverMessage.split("@")[2].split("#")[0], serverMessage.split("#")[1])
        elif serverMessage.startswith("log_out#"):
            rmsg = self.log_out(serverMessage.split("#")[1])
        elif serverMessage.startswith("transfer_money@"):
            rmsg = self.transfer_money(serverMessage.split("@")[1], serverMessage.split("@")[2].split("#")[0], serverMessage.split("#")[1] if "#" in serverMessage else None)
        elif serverMessage.startswith("change_password@"):
            rmsg = self.change_password(serverMessage.split("@")[1].split("#")[0], serverMessage.split("#")[1] if "#" in serverMessage else None)
        elif serverMessage.startswith("query"):
            rmsg = self.query(serverMessage.split("#")[1] if "#" in serverMessage else None)
        elif serverMessage == "return_card":
            rmsg = self.return_card()
        elif serverMessage.startswith("insert_card@"):
            rmsg = self.insert_card(serverMessage.split("@")[1])
        else:
            rmsg = "failed@invalid_command"
        
        self.return_signal.emit(rmsg)
        return rmsg

    # def process(self, serverMessage):
    #     if serverMessage.startswith("create_account@"):
    #         return self.create_account(serverMessage.split("@")[1])
    #     if serverMessage == "close_account":
    #         return self.close_account()
    #     if serverMessage.startswith("deposit_cash@"):
    #         return self.deposit_cash(serverMessage.split("@")[1])
    #     if serverMessage.startswith("withdraw_cash@"):
    #         return self.withdraw_cash(serverMessage.split("@")[1], serverMessage.split("@")[2])
    #     if serverMessage == "open_app":
    #         return self.open_app()
    #     if serverMessage.startswith("close_app#"):
    #         return self.close_app(serverMessage.split("#")[1])
    #     if serverMessage.startswith("log_in@"):
    #         return self.log_in(serverMessage.split("@")[1], serverMessage.split("@")[2].split("#")[0], serverMessage.split("#")[1])
    #     if serverMessage.startswith("log_out#"):
    #         return self.log_out(serverMessage.split("#")[1])
    #     if serverMessage.startswith("transfer_money@"):
    #         return self.transfer_money(serverMessage.split("@")[1], serverMessage.split("@")[2].split("#")[0], serverMessage.split("#")[1] if "#" in serverMessage else None)
    #     if serverMessage.startswith("change_password@"):
    #         return self.change_password(serverMessage.split("@")[1].split("#")[0], serverMessage.split("#")[1] if "#" in serverMessage else None)
    #     if serverMessage.startswith("query"):
    #         return self.query(serverMessage.split("#")[1] if "#" in serverMessage else None)
    #     if serverMessage == "return_card":
    #         return self.return_card()
    #     if serverMessage.startswith("insert_card@"):
    #         return self.insert_card(serverMessage.split("@")[1])
        
    #     return "failed@invalid_command"



    def process_print(self,servermsg):
        rmsg = self.process(servermsg)
        self.return_signal.emit(rmsg)
        return rmsg

    def create_account(self, password):
        if len(password)!= 6:
            return "failed@create_account"
        account_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        while check_account_exist(account_id):
            account_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        create_account(account_id, password)
        self.current_account = account_id
        self.account_available = True
        return "account_created@" + account_id

    def close_account(self):
        if self.account_available == False:
            return "failed@close_account"
        result = query(self.current_account)
        if result['balance'] != 0:
            return "failed@close_account"
        close_account(self.current_account)
        self.account_available = False
        return "account_closed@" + self.current_account

    def deposit_cash(self, deposit_amount):
        if self.account_available and deposit_amount.isdigit():
            update_balance(self.current_account, int(deposit_amount))
            return "cash_deposited@" + deposit_amount
        return "failed@deposit_cash"

    def withdraw_cash(self, withdraw_amount, password):
        if self.account_available and withdraw_amount.isdigit() and check_password(self.current_account, password) and check_enough_balance(self.current_account, int(withdraw_amount)):
            update_balance(self.current_account, -int(withdraw_amount))
            return "cash_withdrawn@" + withdraw_amount
        return "failed@withdraw_cash"

    def open_app(self):
        self.app_count += 1
        app_id = str(self.app_count)
        self.apps_account[app_id] = None
        self.apps_state[app_id] = "open"
        return "app_opened#" + app_id

    def close_app(self, app_id):
        if app_id in self.apps_account and self.apps_state.get(app_id) != "close":
            self.apps_state[app_id] = "close"
            self.close_app_signal.emit(app_id)
            return "app_closed#" + app_id
        return "failed@close_app#" + app_id

    def log_in(self, account_id, password, app_id):
        if not check_password(account_id, password) or not app_id.isdigit() or app_id not in self.apps_account:
            return "failed@log_in#" + app_id
        if self.apps_state[app_id] == "open":
            self.apps_account[app_id] = account_id
            self.apps_state[app_id] = "log_in"
            for aid,v in self.apps_account.items():
                if v == account_id and aid != app_id:
                    self.log_out_signal.emit(aid)
            return "logged_in@" + account_id + "#" + app_id
        return "failed@log_in#" + app_id

    def log_out(self, app_id):
        account_id = self.apps_account.get(app_id)
        if not app_id.isdigit() or not account_id or self.apps_state.get(app_id) != "log_in":
            return "failed@log_out#" + app_id
        self.apps_state[app_id] = "open"
        return "logged_out@" + account_id + "#" + app_id

    def transfer_money(self, receiver_id, transfer_amount, app_id=None):
        account_id = self.current_account if app_id is None else self.apps_account.get(app_id)
        if not check_is_valid(receiver_id) or not check_enough_balance(account_id, int(transfer_amount)) or account_id == receiver_id:
            return "failed@transfer_money#" + (app_id if app_id else "")
        update_balance(account_id, -int(transfer_amount))
        update_balance(receiver_id, int(transfer_amount))
        return "money_transfered@" + transfer_amount + (f"#{app_id}" if app_id else "")

    def change_password(self, new_password, app_id=None):
        account_id = self.current_account if app_id is None else self.apps_account.get(app_id)
        if app_id and (not app_id.isdigit() or not account_id or self.apps_state.get(app_id) != "log_in"):
            return "failed@change_password#" + app_id
        if not self.account_available and not app_id:
            return "failed@change_password"
        if (not new_password.isdigit()) or new_password == "" or len(new_password)!=6:
            return "failed@change_password"
        change_password(account_id, new_password)
        return "password_changed@" + (app_id if app_id else "")

    def query(self,app_id = None):
        account_id = self.current_account if app_id is None else self.apps_account.get(app_id)
        result = query(account_id)
        results =  [result,app_id]
        self.query_result_signal.emit(results)
        if(result== None):
            if app_id == None:
                return "failed@query"
            else:
                return "failed@query#" + app_id
        if app_id == None:
            return "query_showed"
        else:
            return ("query_showed#" + app_id)

    def return_card(self):
        rmessage = "card_returned@" + self.current_account
        self.current_account = None
        return rmessage
    
    def insert_card(self,account_id):
        if not check_is_valid(account_id):
            return "failed@insert_card"
        self.current_account = account_id
        self.account_available = True
        return "card_inserted@" + account_id
    

    def check_password(self,account_id,password):
        return check_password(account_id, password)
    
    
my_processor = Processor()