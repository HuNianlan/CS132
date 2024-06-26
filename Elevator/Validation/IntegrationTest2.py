import unittest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
sys.path.append("Development/YourCodeExample")
from processor import SystemProcessor
from elevator import ElevatorState
from internalUI import InternalUI
from externalUI import ExternalUI
from UIsettings import circle_button_style_on


'''
    TestElevatorProcessor_InternalUI_ExternalUI class tests the integration 
    between the elevator processor and its corresponding internal UI and external UI.
    
    Please run this file under the root path, i.e. Elevator.
'''
class TestElevatorProcessor_InternalUI_ExternalUI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables."""
        cls.app = QApplication(sys.argv)

    def setUp(self):
        """Initialization of each test case."""
        self.system_processor = SystemProcessor()
        self.processor1 = self.system_processor.elevator_processors[0]
        self.processor2 = self.system_processor.elevator_processors[1]
        self.externalUIb = ExternalUI(-1, self.system_processor)
        self.externalUI1 = ExternalUI(1, self.system_processor)
        self.externalUI2 = ExternalUI(2, self.system_processor)
        self.externalUI3 = ExternalUI(3, self.system_processor)
        self.internalUI1 = InternalUI(self.processor1)
        self.internalUI2 = InternalUI(self.processor2)
        self.externalUIb.show()
        self.externalUI1.show()
        self.externalUI2.show()
        self.externalUI3.show()
        self.internalUI1.show()
        self.internalUI2.show()

    def tearDown(self):
        """Cleanup after each test case."""
        self.externalUIb.close()
        self.externalUI1.close()
        self.externalUI2.close()
        self.externalUI3.close()
        self.internalUI1.close()
        self.internalUI2.close()

    @classmethod
    def tearDownClass(cls):
        """Cleanup work after all test cases are executed."""
        cls.app.quit()

    def update(self):
        '''Simulate the update of the processor and UI.'''
        self.system_processor.update()
        self.externalUIb.update()
        self.externalUI1.update()
        self.externalUI2.update()
        self.externalUI3.update()
        self.internalUI1.update()
        self.internalUI2.update()

    def test_elevator_integration(self):
        """Test the full integration scenario with detailed steps."""

        # T2.2.1: Press down button outside on floor 2.
        self.externalUI2.down_button.click()
        while self.processor2.elevator.current_floor != 2:
            self.update()
        # T2.2.1. Expected Output: Elevator 2 is called and the door will open when it arrives.
        self.assertEqual(self.processor2.elevator.current_floor, 2)
        self.assertTrue(self.processor2.checkOpen())
        self.assertEqual(self.internalUI2.open_close_state.text(), "<|>")
        self.assertEqual(self.internalUI2.open_close_state.styleSheet(), "color:green;")
        self.assertEqual(self.externalUI2.elevator_2_open_indicator.text(), "<|>")
        self.assertEqual(self.externalUI2.elevator_2_open_indicator.styleSheet(), "color:green;")

        # T2.2.2: When the door of elevator 2 is about to close, press open door button.
        while self.processor2.elevator.current_state != \
               (ElevatorState.stopped_closing_door or ElevatorState.stopped_door_closed):
            self.update()
        self.internalUI2.open_door_button.click()
        self.update()
        # T2.2.2. Expected Output: The door of elevator 2 opens.
        self.assertTrue(self.processor2.checkOpen())
        self.assertEqual(self.internalUI2.open_close_state.text(), "<|>")
        self.assertEqual(self.internalUI2.open_close_state.styleSheet(), "color:green;")
        self.assertEqual(self.externalUI2.elevator_2_open_indicator.text(), "<|>")
        self.assertEqual(self.externalUI2.elevator_2_open_indicator.styleSheet(), "color:green;")

        # T2.2.3: Press floor -1 button in elevator 2, then press floor 3 button.
        self.internalUI2.floor_button_b.click()
        self.update()
        self.internalUI2.floor_button_3.click()
        self.update()
        self.assertEqual(self.internalUI2.floor_button_b.styleSheet(), circle_button_style_on)
        self.assertEqual(self.internalUI2.floor_button_3.styleSheet(), circle_button_style_on)

        # T2.2.3. Expected Output: Elevator 2 moves to floor -1 at first.
        while self.processor2.elevator.current_floor != -1:
            self.update()
        self.assertEqual(self.internalUI2.floor_label.text(), "Floor: -1")
        self.assertEqual(self.externalUIb.elevator_2_floor_label.text(), "Floor -1")
        self.assertEqual(self.externalUI1.elevator_2_floor_label.text(), "Floor -1")
        self.assertEqual(self.externalUI2.elevator_2_floor_label.text(), "Floor -1")
        self.assertEqual(self.externalUI3.elevator_2_floor_label.text(), "Floor -1")

        # T2.2.4: When elevator 2 is on floor -1, press up button outside on floor 2.
        self.externalUI2.up_button.click()

        # T2.2.4. Expected Output: Elevator 1 is called.
        while self.processor1.elevator.current_floor != 2:
            self.update()
        self.assertEqual(self.internalUI1.floor_label.text(), "Floor: 2")
        self.assertEqual(self.externalUIb.elevator_1_floor_label.text(), "Floor 2")
        self.assertEqual(self.externalUI1.elevator_1_floor_label.text(), "Floor 2")
        self.assertEqual(self.externalUI2.elevator_1_floor_label.text(), "Floor 2")
        self.assertEqual(self.externalUI3.elevator_1_floor_label.text(), "Floor 2")

        # T2.2.5: Press close door button of elevator 1 when door is open.
        while not self.processor1.checkOpen():
            self.update()
        self.internalUI1.push_close_door_button()
        self.update()
        # T2.2.5. Expected Output: Elevator 1 closes the door.
        self.assertEqual(self.processor1.elevator.current_state, ElevatorState.stopped_door_closed)
        self.assertEqual(self.internalUI1.open_close_state.text(), ">|<")
        self.assertEqual(self.internalUI1.open_close_state.styleSheet(), "color:black;")
        self.assertEqual(self.externalUI2.elevator_2_open_indicator.text(), ">|<")
        self.assertEqual(self.externalUI2.elevator_2_open_indicator.styleSheet(), "color:black;")

        # T2.2.3. Expected Output: Elevator 1 then moves to floor 3.
        while self.processor2.elevator.current_floor != 3:
            self.update()
        self.assertEqual(self.internalUI2.floor_label.text(), "Floor: 3")
        self.assertEqual(self.externalUIb.elevator_2_floor_label.text(), "Floor 3")
        self.assertEqual(self.externalUI1.elevator_2_floor_label.text(), "Floor 3")
        self.assertEqual(self.externalUI2.elevator_2_floor_label.text(), "Floor 3")
        self.assertEqual(self.externalUI3.elevator_2_floor_label.text(), "Floor 3")

        
if __name__ == "__main__":
    unittest.main()
