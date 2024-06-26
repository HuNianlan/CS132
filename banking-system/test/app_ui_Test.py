import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt
sys.path.append("src")
from processor import my_processor,Processor
from DB import reset
# from Development.YourCodeExample.banking_app.app_ui import Ui_APP_UI  
from banking_app.app_ui import Ui_APP_UI  
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtTest import QTest

class TestUi_APP_UI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables"""
        cls.app = QApplication(sys.argv)
    

    
    def setUp(self):
        reset()
        self.processor = Processor()
        self.processor.process("open_app")
        self.ui = Ui_APP_UI(self.processor,self.processor.app_count)
        self.ui.stackedWidget.setCurrentWidget(self.ui.loginPage)
        self.new_id:str = self.processor.process("create_account@222222").split("@")[1]
        #"2023123456 #500"
        self.ui.show()
        

    @patch.object(QMessageBox, 'warning')
    def test_handle_login(self,mock_warning):
        self.ui.ui_loginPage.lineEdit.setText("2023123456")
        self.ui.ui_loginPage.lineEdit_2.setText("111112")
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_loginPage.pushButton_3,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.loginPage)
        mock_warning.assert_called_once_with(None, "Login Failed", "Invalid ID or Password")
        
        self.ui.ui_loginPage.lineEdit.setText("2023123456")
        self.ui.ui_loginPage.lineEdit_2.setText("111111")
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_loginPage.pushButton_3,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.selectPage)
        self.ui.ui_SelectPage.pushButton_4.click()
        
    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_transfer(self, mock_information, mock_warning):        
        
        self.ui.ui_transfer.lineEdit.setText("2023123456")
        self.ui.ui_transfer.lineEdit_2.setText("abc")
        self.ui.ui_SelectPage.pushButton.click()

        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_transfer.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.selectPage)
        mock_warning.assert_called_once_with(None, "transfer Failed", "Invalid amount")

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_transfer_2(self, mock_information, mock_warning):

        self.ui.ui_transfer.lineEdit.setText("2023123456")
        self.ui.ui_transfer.lineEdit_2.setText("1000")
        self.ui.ui_SelectPage.pushButton.click()
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_transfer.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.selectPage)
        mock_warning.assert_called_once_with(None, "transfer Failed", "Invalid receiver or lacking balance")

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_transfer_3(self, mock_information, mock_warning):
        self.processor.log_in("2023123456", "111111", str(self.ui.app_id))
        self.ui.stackedWidget.setCurrentWidget(self.ui.selectPage)
        self.ui.ui_transfer.lineEdit.setText(self.new_id)
        self.ui.ui_transfer.lineEdit_2.setText("100")
        self.ui.ui_SelectPage.pushButton.click()
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_transfer.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.selectPage)
        mock_information.assert_called_once_with(None,"transfer succeeded!","SUCCEED")
        
        

    def test_handle_query(self):
        results = [{'account_id': '2023123456', 'balance': 1000, 'creation_time': '2024-01-01 00:00:00'}, str(self.ui.app_id)]
        self.ui.handle_query(results)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.queryPage)
        
    def test_handle_query2(self):
        results = [None, '1'] 
        self.ui.handle_query(results)
        self.assertEqual(self.ui.ui_query.label_3.text(), "Account not found")
    
    def test_handle_query3(self):
        initialPage = self.ui.stackedWidget.currentWidget()
        results = [{'account_id': '2023123456', 'balance': 1000, 'creation_time': '2024-01-01 00:00:00'}, None]
        self.ui.handle_query(results)
        self.assertEqual(self.ui.stackedWidget.currentWidget(),initialPage)

    @patch.object(QMessageBox, 'warning')
    @patch.object(QMessageBox, 'information')
    def test_handle_changePin(self,mock_warning,mock_information):
        self.processor.log_in("2023123456", "111111", str(self.ui.app_id))
        self.ui.stackedWidget.setCurrentWidget(self.ui.selectPage)
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_SelectPage.pushButton_3,Qt.LeftButton)
        QTest.qWait(500)

        self.ui.ui_changePin.lineEdit.setText("123456")
        self.ui.ui_changePin.lineEdit_2.setText("111111")
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_changePin.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.changePinPage)
        mock_warning.assert_called_once_with(None,"inconsistent new pin","you should enter consistent new pins")

    @patch.object(QMessageBox, 'warning')
    def test_handle_changePin_2(self,mock_warning):
        self.processor.log_in("2023123456", "111111", str(self.ui.app_id))
        self.ui.stackedWidget.setCurrentWidget(self.ui.selectPage)
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_SelectPage.pushButton_3,Qt.LeftButton)
        QTest.qWait(500)

        self.ui.ui_changePin.lineEdit.setText("1234ab")
        self.ui.ui_changePin.lineEdit_2.setText("1234ab")
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_changePin.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.changePinPage)
        mock_warning.assert_called_once_with(None, "ChangePin Failed", "Invalid NEW PIN")

    @patch.object(QMessageBox, 'information')
    def test_handle_changePin_3(self,mock_information):
        self.processor.log_in("2023123456", "111111", str(self.ui.app_id))
        self.ui.stackedWidget.setCurrentWidget(self.ui.selectPage)
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_SelectPage.pushButton_3,Qt.LeftButton)
        QTest.qWait(500)
        self.ui.ui_changePin.lineEdit.setText("123456")
        self.ui.ui_changePin.lineEdit_2.setText("123456")
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_changePin.pushButton,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.selectPage)
        mock_information.assert_called_once_with(None,"ChangePin succeeded!","SUCCEED")

    @patch.object(QMessageBox, 'warning')
    def test_handle_logout(self,mock_warning):
        self.ui.stackedWidget.setCurrentWidget(self.ui.selectPage)
        self.processor.process("open_app")
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_SelectPage.pushButton_4,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.selectPage)
        mock_warning.assert_called_once_with(None, "Logout out", "app without login")

        self.processor.log_in("2023123456", "111111", str(self.ui.app_id))
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_SelectPage.pushButton_4,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.loginPage)

    def test_back_to_select(self):
        self.processor.log_in("2023123456", "111111", str(self.ui.app_id))
        self.ui.stackedWidget.setCurrentWidget(self.ui.selectPage)
        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_SelectPage.pushButton_3,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.changePinPage)

        QTest.qWait(500)
        QTest.mouseClick(self.ui.ui_changePin.pushButton_2,Qt.LeftButton)
        QTest.qWait(500)
        self.assertEqual(self.ui.stackedWidget.currentWidget(), self.ui.selectPage)


    def tearDown(self):
        self.ui.close()
        self.app.quit()

if __name__ == "__main__":
    unittest.main()

