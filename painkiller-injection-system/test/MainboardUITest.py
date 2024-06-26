import sys
sys.path.append("src")
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from mainborad import Mainboard 
from processor import InjectProcessor
from setting import SettingPage
from history import HistoryPage
from unittest.mock import patch
from PyQt5.QtCore import QDate, QTime, QDateTime
    
class TestMainboardUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables"""
        cls.app = QApplication(sys.argv)


    def setUp(self):
        """Initialization of each test case"""
        self.mainboard = Mainboard(InjectProcessor())
        self.mainboard.show()

    
    def get_last_dialog(self):
        """Get the last dialog that was shown"""
        return self.dialog_filter.dialog

    def wait_for_dialog(self, dialog_class, timeout=5000):
        """Wait for a dialog of a specific class to appear within a timeout"""
        for _ in range(timeout // 100):
            for widget in QApplication.instance().topLevelWidgets():
                if isinstance(widget, dialog_class):
                    if widget.isVisible():
                        return widget
            QTest.qWait(100)
        return None
    
    def test_setting_click(self):
        """Test the Settings button click functionality"""
        QTest.qWait(1000)
        QTest.mouseClick(self.mainboard.setting_button, Qt.LeftButton)
        QTest.qWait(1000)
        setting_page = self.app.activeWindow()
        self.assertIsInstance(setting_page, SettingPage)
        QTest.qWait(1000)
        setting_page.close()

    @patch.object(Mainboard, 'checkPIN', return_value=True)
    def test_status_click_checkPIN_true(self, mock_checkPIN):
        """Test the Status button click functionality when checkPIN returns True"""
        self.assertTrue(self.mainboard.getStatus())
        QTest.qWait(1000)
        QTest.mouseClick(self.mainboard.status_button, Qt.LeftButton)
        QTest.qWait(1000)
        mock_checkPIN.assert_called_once()
        self.assertFalse(self.mainboard.getStatus())

    @patch.object(Mainboard, 'checkPIN', return_value=False)
    def test_status_click_checkPIN_false(self, mock_checkPIN):
        """Test the Status button click functionality when checkPIN returns True"""
        self.assertTrue(self.mainboard.getStatus())
        QTest.qWait(1000)
        QTest.mouseClick(self.mainboard.status_button, Qt.LeftButton)
        QTest.qWait(1000)
        mock_checkPIN.assert_called_once()
        self.assertTrue(self.mainboard.getStatus())
    
    def test_history_click(self):
        """Test the History button click functionality"""
        QTest.qWait(500)
        QTest.mouseClick(self.mainboard.history_button, Qt.LeftButton)
        QTest.qWait(500)
        history_page = self.app.activeWindow()
        self.assertIsInstance(history_page, HistoryPage)
        self.assertTrue(history_page.isVisible())
        history_page.close()
    
    @patch.object(Mainboard, 'checkPIN', return_value=True)
    def test_reset_pin_click_checkPIN_true(self,mock_checkPIN):
        """Test the Reset PIN button click functionality"""
        QTest.mouseClick(self.mainboard.reset_button, Qt.LeftButton)
        QTest.qWait(500)
        self.assertTrue(hasattr(self.mainboard, 'reset_page'))

        self.assertTrue(self.mainboard.reset_page.isVisible())
    
    @patch.object(Mainboard, 'checkPIN', return_value=False)
    def test_reset_pin_click_checkPIN_false(self,mock_checkPIN):
        """Test the Reset PIN button click functionality"""
        QTest.mouseClick(self.mainboard.reset_button, Qt.LeftButton)
        QTest.qWait(500)
        self.assertFalse(hasattr(self.mainboard, 'reset_page'))
    

    @patch.object(InjectProcessor, 'addPainkiller')  # Patching the method to track its calls
    def test_add_painkiller_click(self, mock_addPainkiller):
        """Test if addPainkiller method is called"""
        QTest.mouseClick(self.mainboard.add_button, Qt.LeftButton)
        mock_addPainkiller.assert_called_once() 

    def test_ui_update_time_unchanged(self):
        """Test the update time functionality"""
        self.mainboard.getProcessor().database.remaining = 0
        self.mainboard.getProcessor().database.status = False
        self.mainboard.last_time = None
        QTest.qWait(2000)
        self.assertEqual(self.mainboard.last_time_label.text(),"Last injection: No injection yet!")
        self.assertEqual(self.mainboard.painkiller_remind.text(),"Running out, please add painkiller!")
        self.assertEqual(self.mainboard.bolus_hour_label.text(),"Last 1 Hour\t0.00 / 1.00 mL")
        self.assertEqual(self.mainboard.bolus_day_label.text(),"Last 1 Day\t0.00 / 3.00 mL")

    def test_ui_update_time_changed(self):
        """Test the update time functionality"""
        self.mainboard.getProcessor().database.remaining = 10
        self.mainboard.getProcessor().database.baseline = 0.05
        self.mainboard.getProcessor().database.status = True
        date = QDate(2024, 6, 8) 
        time = QTime(12, 00, 00) 
        self.mainboard.last_time = QDateTime(date, time)
        QTest.qWait(5700)
        self.assertEqual(self.mainboard.last_time_label.text(),"Last injection: 2024-06-08 12:00:00")
        self.assertEqual(self.mainboard.painkiller_remind.text(),"")
        self.assertEqual(self.mainboard.bolus_hour_label.text(),"Last 1 Hour\t0.40 / 1.00 mL")
        self.assertEqual(self.mainboard.bolus_day_label.text(),"Last 1 Day\t0.40 / 3.00 mL")

        
    
    def tearDown(self):
        """Cleanup after each test case"""
        self.mainboard.close()

    @classmethod
    def tearDownClass(cls):
        """Cleanup work after all test cases are executed"""
        cls.app.quit()

if __name__ == "__main__":
    unittest.main()
