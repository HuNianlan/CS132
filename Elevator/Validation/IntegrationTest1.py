import unittest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
sys.path.append("Development/YourCodeExample")
from processor import SystemProcessor
from elevator import ElevatorState
from internalUI import InternalUI
from UIsettings import circle_button_style, circle_button_style_on


'''
    TestElevatorProcessor_InternalUI class tests the integration 
    between the elevator processor and its corresponding internal UI.
    
    Please run this file under the root path, i.e. Elevator.
'''
class TestElevatorProcessor_InternalUI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables."""
        cls.app = QApplication(sys.argv)


    def setUp(self):
        """Initialization of each test case."""
        self.processor = SystemProcessor().elevator_processors[0]
        self.internalUI = InternalUI(self.processor)
        self.internalUI.show()


    def tearDown(self):
        """Cleanup after each test case."""
        self.internalUI.close()


    @classmethod
    def tearDownClass(cls):
        """Cleanup work after all test cases are executed."""
        cls.app.quit()


    """The codes for T2.1.1 are as follows."""

    def test_open_door_button(self):
        """Test the internal open door button of Elevator 1."""
        self.processor.elevator.current_state = ElevatorState.stopped_door_closed
        self.internalUI.open_door_button.click()
        self.processor.update()
        self.internalUI.update()
        self.assertTrue(self.processor.checkOpen())
        self.assertEqual(self.internalUI.open_close_state.text(), "<|>")
        self.assertEqual(self.internalUI.open_close_state.styleSheet(), "color:green;")
        QTimer.singleShot(2500, self.verify_door_closed)

    def verify_door_closed(self):
        self.assertEqual(self.processor.elevator.current_state, ElevatorState.stopped_door_closed)
        self.assertEqual(self.internalUI.open_close_state.text(), ">|<")
        self.assertEqual(self.internalUI.open_close_state.styleSheet(), "color:black;")
    

    """The codes for T2.1.2 are as follows."""

    def test_close_door_button(self):
        """Test the internal close door button of Elevator 1."""
        self.processor.elevator.current_state = ElevatorState.stopped_door_opened
        self.internalUI.close_door_button.click()
        self.assertEqual(self.processor.elevator.current_state, ElevatorState.stopped_door_closed)
        self.assertEqual(self.internalUI.open_close_state.text(), ">|<")


    """The codes for T2.1.3 are as follows."""

    def test_floor_buttons(self):
        """Test the floor buttons of Elevator 1."""
        self.processor.elevator.current_floor = 1
        self.internalUI.floor_button_3.click()
        self.assertEqual(self.internalUI.floor_button_3.styleSheet(), circle_button_style_on)
        self.internalUI.floor_button_1.click()
        self.assertEqual(self.internalUI.floor_button_1.styleSheet(), circle_button_style_on)
        QTimer.singleShot(2500, self.verify_floor)

    def verify_floor(self):
        self.assertEqual(self.processor.elevator.current_floor, 3)
        self.assertEqual(self.internalUI.floor_label.text(), "Floor: 3")
        self.assertEqual(self.internalUI.floor_button_3.styleSheet(), circle_button_style)
        self.assertEqual(self.internalUI.floor_button_1.styleSheet(), circle_button_style)

        
if __name__ == "__main__":
    unittest.main()
