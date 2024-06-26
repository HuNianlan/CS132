import unittest
import sys
sys.path.append("src")
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDate, QTime, QDateTime
from unittest.mock import patch
from database import InjectDatabase
from processor import InjectProcessor


class TestInjectProcessor(unittest.TestCase):

    def setUp(self):
        app = QApplication(sys.argv)
        self.processor = InjectProcessor()
        self.mainboard = self.processor.mainboard

    def test_get_database(self):
        """Test case for getting the database."""
        self.assertIsInstance(self.processor.getDatabase(), InjectDatabase)


    def test_check_inject(self):
        """Test case for checking injection conditions."""
        date = QDate(2024, 6, 8) 
        time = QTime(12, 00, 00)  
        time = QDateTime(date, time)
        processor = self.processor
        db = processor.database
        db.remaining = 0
        db.limit_hour = 0
        db.limit_day = 0
        self.assertFalse(processor.checkInject(time,0.2))
        db.remaining = 10
        self.assertFalse(processor.checkInject(time,0.2))
        db.limit_hour = 0.2
        self.assertFalse(processor.checkInject(time,0.2))
        db.limit_day = 2
        self.assertTrue(processor.checkInject(time,0.2))



    def test_check_Hour(self):
        """Test case for checking Hour_limit."""
        date = QDate(2024, 6, 8) 
        time = QTime(12, 00, 00)  
        self.processor.database.bolus = 0.2
        self.processor.database.limit_hour = 0.2
        self.assertEqual(self.processor.database.bolus_history, {})
        self.assertEqual(self.processor.checkHour(QDateTime(date, time),0.2), True)

        self.processor.database.bolus = 0.2
        self.processor.database.limit_hour = 0
        self.assertEqual(self.processor.database.bolus_history, {})
        self.assertEqual(self.processor.checkHour(QDateTime(date, time),0.2), False)

    def test_check_Day(self):
        """Test case for checking Day_limit."""
        date = QDate(2024, 6, 8) 
        time = QTime(12, 00, 00)    
        self.processor.database.bolus = 0.2
        self.processor.database.limit_day = 2
        self.assertEqual(self.processor.database.bolus_history, {})
        self.assertEqual(self.processor.checkDay(QDateTime(date, time),0.2), True)

        self.processor.database.bolus = 0.2
        self.processor.database.limit_day = 0
        self.assertEqual(self.processor.database.bolus_history, {})
        self.assertEqual(self.processor.checkDay(QDateTime(date, time),0.2), False)

    def test_check_pin(self):
        """Test case for checking PIN."""
        self.assertEqual(self.processor.getPIN(),"000000")
        self.assertFalse(self.processor.checkPIN("123456"))
        self.assertTrue(self.processor.checkPIN("000000"))


    @patch.object(InjectProcessor, 'checkInject', return_value=True)
    @patch.object(InjectProcessor, 'getBolus', return_value=5.0)
    @patch.object(InjectProcessor, 'inject', return_value=True)
    @patch.object(InjectProcessor, 'addBolusHistory', return_value=None)
    @patch.object(InjectProcessor, 'addEventHistory', return_value=None)
    def test_inject_request_success(self, mock_checkInject, mock_getBolus, mock_inject, mock_addBolusHistory, mock_addEventHistory):
        """Test the inject_request method when injection is successful"""
        initial_time = QDateTime.currentDateTime().addSecs(-3600)  # 1 hour ago
        current_time = QDateTime.currentDateTime()
        self.mainboard.initial_time = initial_time

        result = self.processor.inject_request(current_time)

        self.assertTrue(result)

    
    @patch.object(InjectProcessor, 'checkInject', return_value=False)
    @patch.object(InjectProcessor, 'getBolus', return_value=5.0)
    @patch.object(InjectProcessor, 'inject', return_value=True)
    @patch.object(InjectProcessor, 'addBolusHistory', return_value=None)
    @patch.object(InjectProcessor, 'addEventHistory', return_value=None)
    def test_inject_request_failure(self, mock_checkInject, mock_getBolus, mock_inject, mock_addBolusHistory, mock_addEventHistory):
        """Test the inject_request method when injection is not successful"""
        initial_time = QDateTime.currentDateTime().addSecs(-3600)  # 1 hour ago
        current_time = QDateTime.currentDateTime()
        self.mainboard.initial_time = initial_time

        result = self.processor.inject_request(current_time)

        self.assertTrue(result)




if __name__ == '__main__':
    unittest.main()
