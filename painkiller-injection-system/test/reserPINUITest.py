import sys
sys.path.append("src")
from processor import InjectProcessor
import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication,QDialogButtonBox
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from resetPIN import ResetPINPage

class TestResetPINPage(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.processor = InjectProcessor()
        self.dialog = ResetPINPage(self.processor)
        self.dialog.show()
    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_reset_pin_success(self, mock_information, mock_warning):
        # Simulate entering a valid PIN and confirming

        QTest.keyClicks(self.dialog.lineedit1, "123456")
        QTest.keyClicks(self.dialog.lineedit2, "123456")
        QTest.qWait(1000)
        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
        QTest.qWait(1000)
        # Assert that QMessageBox.information was called
        mock_information.assert_called_once_with(self.dialog, 'Information', 'Reset PIN successfully!')

        # Verify that the processor's resetPIN method was called
        # self.processor.resetPIN.assert_called_once_with("123456")
    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_invalid_pin1(self, mock_warning):
        # Simulate entering an invalid PIN (not 6 digits)
        QTest.keyClicks(self.dialog.lineedit1, "1234a")
        QTest.keyClicks(self.dialog.lineedit2, "12345")
        QTest.qWait(1000)
        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
        QTest.qWait(1000)
        # Assert that QMessageBox.warning was called
        mock_warning.assert_called_once_with(self.dialog, 'Invalid PIN', 'PIN must be 6 digits, please reset!')
    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_pin_mismatch(self, mock_warning):
        # Simulate entering mismatched PINs
        QTest.keyClicks(self.dialog.lineedit1, "123456")
        QTest.keyClicks(self.dialog.lineedit2, "654321")
        QTest.qWait(1000)
        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
        QTest.qWait(1000)
        # Assert that QMessageBox.warning was called
        mock_warning.assert_called_once_with(self.dialog, 'Invalid PIN', 'PINs does not match, please reset!')

    def tearDown(self):
        self.dialog.close()


if __name__ == '__main__':
    unittest.main()
