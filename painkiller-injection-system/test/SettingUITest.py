import sys
sys.path.append("src")
from processor import InjectProcessor
import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication, QDialogButtonBox,QDialog
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from setting import SettingPage

class TestSettingPage(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.processor = InjectProcessor()
        self.dialog = SettingPage(self.processor)
        self.dialog.show()
    
    @patch('checkPIN.CheckPINPage.exec_', return_value= QDialog.Accepted)
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_update_database_success(self, mock_warning, mock_checkPINPage):
        # Simulate entering valid values
        QTest.qWait(100)
        self.dialog.line_edits["Baseline (mL/min)"].setFocus()
        self.dialog.line_edits["Baseline (mL/min)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Baseline (mL/min)"], "0.05")
        QTest.qWait(100)
        self.dialog.line_edits["Bolus (mL/shot)"].setFocus()
        self.dialog.line_edits["Bolus (mL/shot)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Bolus (mL/shot)"], "0.30")
        QTest.qWait(100)
        self.dialog.line_edits["Limit per hour (mL)"].setFocus()
        self.dialog.line_edits["Limit per hour (mL)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Limit per hour (mL)"], "0.70")
        QTest.qWait(100)
        self.dialog.line_edits["Limit per day (mL)"].setFocus()
        self.dialog.line_edits["Limit per day (mL)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Limit per day (mL)"], "1.50")

        QTest.qWait(1000)
        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)

        # Assert that QMessageBox.warning was not called
        mock_warning.assert_not_called()

        self.assertEqual(self.processor.getBaseline(),0.05)
        self.assertEqual(self.processor.getBolus(),0.3)
        self.assertEqual(self.processor.getLimitHour(),0.7)
        self.assertEqual(self.processor.getLimitDay(),1.5)
 

    @patch('checkPIN.CheckPINPage.exec_', return_value=QDialog.Rejected)
    def test_pin_rejection(self, mock_checkPINPage):
        # Simulate entering valid values
        QTest.qWait(100)
        self.dialog.line_edits["Baseline (mL/min)"].setFocus()
        self.dialog.line_edits["Baseline (mL/min)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Baseline (mL/min)"], "0.05")
        QTest.qWait(100)
        self.dialog.line_edits["Bolus (mL/shot)"].setFocus()
        self.dialog.line_edits["Bolus (mL/shot)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Bolus (mL/shot)"], "0.30")
        QTest.qWait(100)
        self.dialog.line_edits["Limit per hour (mL)"].setFocus()
        self.dialog.line_edits["Limit per hour (mL)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Limit per hour (mL)"], "0.70")
        QTest.qWait(100)
        self.dialog.line_edits["Limit per day (mL)"].setFocus()
        self.dialog.line_edits["Limit per day (mL)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Limit per day (mL)"], "1.50")

        QTest.qWait(1000)
        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
        self.assertEqual(self.processor.getBaseline(),0.0)
        self.assertEqual(self.processor.getBolus(),0.0)
        self.assertEqual(self.processor.getLimitHour(),1.0)
        self.assertEqual(self.processor.getLimitDay(),3.0)


    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_invalid_parameter(self, mock_warning):
        # Simulate entering invalid values        
        QTest.qWait(100)
        self.dialog.line_edits["Baseline (mL/min)"].setFocus()
        self.dialog.line_edits["Baseline (mL/min)"].clear()
        QTest.keyClicks(self.dialog.line_edits["Baseline (mL/min)"], "0.2")
        QTest.qWait(1000)

        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
        # Assert that QMessageBox.warning was called
        mock_warning.assert_called_once_with(self.dialog, "Invalid Parameter", "Invalid input for Baseline (mL/min)!")
        self.assertEqual(self.processor.getBaseline(),0.0)
        self.assertEqual(self.processor.getBolus(),0.0)
        self.assertEqual(self.processor.getLimitHour(),1.0)
        self.assertEqual(self.processor.getLimitDay(),3.0)

    def tearDown(self):
        self.dialog.close()

if __name__ == '__main__':
    unittest.main()
