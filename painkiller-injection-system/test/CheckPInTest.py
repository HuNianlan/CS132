import sys
sys.path.append("src")
import unittest
from PyQt5.QtWidgets import QApplication, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from processor import InjectProcessor
from checkPIN import CheckPINPage
from PyQt5.QtCore import *
from unittest.mock import patch

class TestCheckPINPage(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.dialog = CheckPINPage(InjectProcessor())
        self.dialog.show()

    def test_correct_pin(self):
        # Simulate entering the correct PIN        
        QTest.qWait(500)
        QTest.keyClicks(self.dialog.checkPIN, "000000")
        QTest.qWait(500)
        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
        QTest.qWait(500)
        self.assertTrue(self.dialog.result())  # Check if dialog was accepted
    
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_wrong_pin_multiple_attempts(self,mock_warning):
        # Simulate entering a wrong PIN multiple times
        self.assertEqual(self.dialog.times, 3)
        QTest.keyClicks(self.dialog.checkPIN, "0000")
        QTest.qWait(500)
        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
        QTest.qWait(500)
        mock_warning.assert_called_once_with(self.dialog, "Wrong PIN", "Please type in correct PIN!")
        self.assertEqual(self.dialog.times, 2)  # Check remaining attempts
        self.assertEqual(self.dialog.label.text(), f"Please enter the PIN (2 times left):")
        self.assertTrue(self.dialog.isVisible())
    
    @patch('PyQt5.QtWidgets.QMessageBox.critical')
    def test_no_attempts_left(self,mock_critical):
        # Simulate entering wrong PIN three times
        self.dialog.times=1
        QTest.keyClicks(self.dialog.checkPIN, "0000")
        QTest.qWait(500)
        QTest.mouseClick(self.dialog.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
        QTest.qWait(500)
        mock_critical.assert_called_once_with(self.dialog, 'Error', 'No attempts left, PIN check failed!')
        self.assertEqual(self.dialog.times, 0)  # Check remaining attempts
        self.assertFalse(self.dialog.isVisible())  # Dialog should be closed after 3 attempts

    def tearDown(self):
        self.dialog.close()

if __name__ == '__main__':
    unittest.main()
