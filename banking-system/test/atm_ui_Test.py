import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
sys.path.append("src")
from processor import Processor
from atm.atm_ui import Ui_ATM
from DB import reset
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QMessageBox

class TestUi_ATM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables"""
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        reset()
        self.ui = QMainWindow()
        self.processor = Processor()
        self.atm_ui = Ui_ATM(self.ui,self.processor)
        self.new_id:str = self.processor.process("create_account@222222").split("@")[1]
        self.ui.show()
    
    #@patch('atm.CheckPINpage.CheckPINPage.exec_',return_value = QDialog.Accepted)
    #def test_handle_insert_card(self,mock_checkPINPage):
    #    QTest.qWait(500)
    #    QTest.mouseClick(self.toolButton,Qt.LeftButton)
    #    QTest.qWait(500)

   
    @patch.object(QMessageBox, 'warning')
    def test_insert_card(self,mock_warning):
        card_id="0000000000"
        self.atm_ui.insert_card(card_id)
        mock_warning.assert_called_once_with(None, "Card Insert Failed", "Invalid ID")
        
        card_id="2023123456"
        self.atm_ui.insert_card(card_id)
        self.assertEqual(self.atm_ui.account_id,card_id)
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)
         

    def test_handle_return_card(self):
        self.atm_ui.create_account("111111")
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_SelectPage.ReturnCard,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.display_widget.EntryPage)
        

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_change_pin(self, mock_warning,mocking_information):
        self.atm_ui.ui_change_pin.lineEdit.setText("123456")
        self.atm_ui.ui_change_pin.lineEdit_2.setText("111111")
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_change_pin.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mock_warning.assert_called_once_with(None,"inconsistent new pin","you should enter consistent new pins")
        
    @patch.object(QMessageBox, 'warning')
    def test_handle_change_pin_2(self,mock_warning):
        self.atm_ui.ui_change_pin.lineEdit.setText("1234")
        self.atm_ui.ui_change_pin.lineEdit_2.setText("1234")
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_change_pin.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mock_warning.assert_called_once_with(None, "ChangePin Failed", "Invalid NEW PIN")

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_change_pin(self,mocking_warning,mocking_information):
        self.atm_ui.create_account("111111")
        self.atm_ui.ui_change_pin.lineEdit.setText("123456")
        self.atm_ui.ui_change_pin.lineEdit_2.setText("123456")
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_change_pin.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        # mocking_information.assert_called_once_with(None,"ChangePin succeeded!","SUCCEED")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)



    def test_handle_query(self):
        results = [{'account_id': '2023123456', 'balance': 1000, 'creation_time': '2024-01-01 00:00:00'},None]
        self.atm_ui.handle_query(results)
        QTest.qWait(500)
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.queryPage)
    
    def test_handle_query_2(self):
        results = [None,None]
        self.atm_ui.handle_query(results)
        QTest.qWait(500)
        self.assertEqual(self.atm_ui.ui_query.label_3.text(), "Account not found")

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_transfer(self, mocking_information, mocking_warning):
        self.atm_ui.insert_card("2023123456")
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        self.atm_ui.ui_transfer.lineEdit.setText(self.new_id)
        self.atm_ui.ui_transfer.lineEdit_2.setText("abc")
        self.atm_ui.ui_SelectPage.transfer.click()
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_transfer.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mocking_warning.assert_called_once_with(None, "transfer Failed", "Invalid amount")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)
  
    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_transfer_2(self, mocking_information, mocking_warning):
        self.atm_ui.insert_card(self.new_id)
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        self.atm_ui.ui_transfer.lineEdit.setText("2023123456")
        self.atm_ui.ui_transfer.lineEdit_2.setText("100")
        self.atm_ui.ui_SelectPage.transfer.click()
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_transfer.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mocking_warning.assert_called_once_with(None, "transfer Failed", "Invalid receiver or lacking balane")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)
    
    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_transfer_3(self, mocking_information, mocking_warning):
        self.atm_ui.insert_card("2023123456")
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        self.atm_ui.ui_transfer.lineEdit.setText(self.new_id)
        self.atm_ui.ui_transfer.lineEdit_2.setText("100")
        self.atm_ui.ui_SelectPage.transfer.click()
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_transfer.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mocking_information.assert_called_once_with(None,"transfer succeeded!","SUCCEED")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)
  


    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_deposit_cash(self, mocking_information, mocking_warning):
        self.atm_ui.my_ATM.deposit_amount="10"
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        self.atm_ui.ui_SelectPage.DepositCash.click()
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_deposit_cash.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        #mocking_warning.assert_called_once_with(self, "deposit Failed", "Invalid amount")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_deposit_cash_2(self, mocking_information, mocking_warning):
        self.atm_ui.insert_card(self.new_id)
        self.atm_ui.my_ATM.deposit_amount="100000"
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        self.atm_ui.ui_SelectPage.DepositCash.click()
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_deposit_cash.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mocking_information.assert_called_once_with(None,"deposit succeeded!","SUCCEED")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)

   

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_withdraw_cash(self, mocking_information, mocking_warning):
        self.atm_ui.ui_withdraw_cash.lineEdit.setText("abc")
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        self.atm_ui.ui_SelectPage.WithdrawCash.click()
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_withdraw_cash.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mocking_warning.assert_called_once_with(None, "Invalid amount", "You should enter correct amount!")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_withdraw_cash_2(self, mocking_information, mocking_warning):
        self.atm_ui.ui_withdraw_cash.lineEdit.setText("")
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        self.atm_ui.ui_SelectPage.WithdrawCash.click()
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_withdraw_cash.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mocking_warning.assert_called_once_with(None, "Invalid amount", "You should enter correct amount!")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_withdraw_cash_3(self, mocking_information, mocking_warning):
        self.atm_ui.my_ATM.cash=500
        self.atm_ui.ui_withdraw_cash.lineEdit.setText("10000")
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.selectPage)
        self.atm_ui.ui_SelectPage.WithdrawCash.click()
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_withdraw_cash.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        mocking_warning.assert_called_once_with(None, "ATM Out of Money", "Sorry! ATM is out of money.")
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_withdraw_cash(self, mocking_information, mocking_warning):
        self.atm_ui.insert_card("2023123456")
        amount="100"
        password="000000"
        self.atm_ui.withdraw_cash(amount,password)
        mocking_warning.assert_called_once_with(None, "Withdraw Failed", "Invalid password or not enough balance")

        amount="100"
        password="111111"
        self.atm_ui.withdraw_cash(amount,password)
        mocking_information.assert_called_once_with(None,"Withdraw succeeded!","SUCCEED")



    @patch.object(QMessageBox, 'warning')
    def test_create_account(self, mocking_warning):
        password="1234"
        self.atm_ui.create_account(password)
        mocking_warning.assert_called_once_with(None, "Invalid password", "Your password should be 6 digits")

    @patch.object(QMessageBox, 'warning')
    def test_create_account(self, mocking_warning): 
        password="123456"
        self.atm_ui.create_account(password)
        #mocking_warning.assert_called_once_with(None, "Accound Created", "Your account id is "+card_id)
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)
        

    def test_go_to_selectPage(self):
        self.atm_ui.display_widget.stacked_layout.setCurrentWidget(self.atm_ui.transferPage)
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_transfer.pushButton_2,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.atm_ui.display_widget.stacked_layout.currentWidget(), self.atm_ui.selectPage)

        
    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    @patch.object(QMessageBox, 'warning')
    def test_handle_close_account(self, mocking_warning,mock_question):
        self.atm_ui.insert_card("2023123456")
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_SelectPage.closeaccount,Qt.LeftButton)
        QTest.qWait(500)
        mocking_warning.assert_called_once_with(self.atm_ui.display_widget,"Close Account failed","Account still has money.")
    
    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    @patch.object(QMessageBox, 'information')
    def test_handle_close_account_2(self, mocking_information,mock_question):
        self.atm_ui.insert_card(self.new_id)
        QTest.qWait(500)
        QTest.mouseClick(self.atm_ui.ui_SelectPage.closeaccount,Qt.LeftButton)
        QTest.qWait(500)
        mocking_information.assert_called_once_with(self.atm_ui.display_widget,"Close Account","Succeed!")
 

    def test_ATM_cashupdate(self):
        initial_cash = self.atm_ui.my_ATM.cash
        amount=100
        self.atm_ui.ATM_cashupdate(amount)
        self.assertEqual(self.atm_ui.my_ATM.cash,amount+initial_cash)
    
    
    def tearDown(self):
        self.ui.close()
        self.app.quit()             

if __name__ == "__main__":
    unittest.main()
