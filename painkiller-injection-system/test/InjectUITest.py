import sys
sys.path.append("src")
from processor import InjectProcessor
import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt,QDateTime
from mainborad import Mainboard 
from inject import Inject

class TestInject(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.mainboard = Mainboard(InjectProcessor())
        self.inject = Inject(self.mainboard)
        self.inject.show()
    
    def test_inject_button(self):
        QTest.qWait(1000)
        with patch.object(self.mainboard.getProcessor(), 'inject_request') as mock_inject_request:
            # Simulate button click
            QTest.mouseClick(self.inject.inject_button, Qt.LeftButton)
            
            # Assert that inject_request was called once with the current time
            mock_inject_request.assert_called_once_with(self.mainboard.current_time)

    
    def tearDown(self):
        self.inject.close()

if __name__ == '__main__':
    unittest.main()
