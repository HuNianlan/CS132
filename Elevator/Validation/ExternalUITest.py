import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
sys.path.append("Development/YourCodeExample")
from processor import SystemProcessor
from elevator import ElevatorState, DirectionState
from externalUI import ExternalUI
from UIsettings import on, off, circle_button_style, circle_button_style_on


'''
    TestExternalUI class contains unit tests for ExternalUI class.
    Please run this file under the root path, i.e. Elevator.
'''
class TestExternalUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables"""
        cls.app = QApplication(sys.argv)

    def setUp(self):
        """Initialization of each test case"""
        self.ui = ExternalUI(2, SystemProcessor())
        self.ui.show()

    def tearDown(self):
        """Cleanup after each test case"""
        self.ui.close()

    @classmethod
    def tearDownClass(cls):
        """Cleanup work after all test cases are executed"""
        cls.app.quit()


    def test_update(self):
        """Test case for update() method of the ExternalUI class."""

        # Mock methods to isolate update() functionality.
        self.ui.update_time = MagicMock()
        self.ui.update_floor = MagicMock()
        self.ui.update_state = MagicMock()
        self.ui.update_direction = MagicMock()
        self.ui.update_button = MagicMock()

        self.ui.update()
        self.ui.update_time.assert_called_once()
        self.ui.update_floor.assert_called_once()
        self.ui.update_state.assert_called_once()
        self.ui.update_direction.assert_called_once()
        self.ui.update_button.assert_called_once()


    def test_update_time(self):
        """Test case for update_time() method of the ExternalUI class."""
        self.ui.update_time()
        current_time = QDateTime.currentDateTime().toString('hh:mm:ss')
        expected_text = f'Time: {current_time}'
        self.assertEqual(self.ui.time_label.text(), expected_text)


    def test_update_state(self):
        """Test update_state() method of the ExternalUI class."""
        # Mock methods to isolate update_state() functionality.
        self.ui.checkOpen = MagicMock()

        # Test case 1: Elevator door is open.
        self.ui.checkOpen.return_value = True
        self.ui.update_state()
        self.assertEqual(self.ui.elevator_1_open_indicator.text(), "<|>")
        self.assertEqual(self.ui.elevator_2_open_indicator.text(), "<|>")
        self.assertEqual(self.ui.elevator_1_open_indicator.styleSheet(), "color:green;")
        self.assertEqual(self.ui.elevator_2_open_indicator.styleSheet(), "color:green;")
    
        # Reset mock calls for the next test case.
        self.ui.checkOpen.reset_mock()

        # Test case 2: Elevator door is closed.
        self.ui.checkOpen.return_value = False
        self.ui.update_state()
        self.assertEqual(self.ui.elevator_1_open_indicator.text(), ">|<")
        self.assertEqual(self.ui.elevator_2_open_indicator.text(), ">|<")
        self.assertEqual(self.ui.elevator_1_open_indicator.styleSheet(), "color:black;")
        self.assertEqual(self.ui.elevator_2_open_indicator.styleSheet(), "color:black;")


    def test_update_floor(self):
        """Test the update_floor() method of the ExternalUI class."""
        self.ui.processor.elevator_processors[0].elevator.current_floor = 3
        self.ui.processor.elevator_processors[1].elevator.current_floor = 1
        self.ui.update_floor()
        self.assertEqual(self.ui.elevator_1_floor_label.text(), 'Floor 3')
        self.assertEqual(self.ui.elevator_2_floor_label.text(), 'Floor 1')


    def test_update_direction(self):
        """Test the update_direction() method of the ExternalUI class."""
        # Test case 1: Elevator is idle.
        self.ui.processor.elevator_processors[0].elevator.direction = DirectionState.idle
        self.ui.processor.elevator_processors[1].elevator.direction = DirectionState.idle
        self.ui.update_direction()
        self.assertEqual(self.ui.elevator_1_up_indicator.styleSheet(), off)
        self.assertEqual(self.ui.elevator_1_down_indicator.styleSheet(), off)
        self.assertEqual(self.ui.elevator_2_up_indicator.styleSheet(), off)
        self.assertEqual(self.ui.elevator_2_down_indicator.styleSheet(), off)

        # Test case 2: Elevator is up.
        self.ui.processor.elevator_processors[0].elevator.direction = DirectionState.up
        self.ui.processor.elevator_processors[1].elevator.direction = DirectionState.up
        self.ui.update_direction()
        self.assertEqual(self.ui.elevator_1_up_indicator.styleSheet(), on)
        self.assertEqual(self.ui.elevator_1_down_indicator.styleSheet(), off)
        self.assertEqual(self.ui.elevator_2_up_indicator.styleSheet(), on)
        self.assertEqual(self.ui.elevator_2_down_indicator.styleSheet(), off)

        # Test case 3: Elevator is down.
        self.ui.processor.elevator_processors[0].elevator.direction = DirectionState.down
        self.ui.processor.elevator_processors[1].elevator.direction = DirectionState.down
        self.ui.update_direction()
        self.assertEqual(self.ui.elevator_1_up_indicator.styleSheet(), off)
        self.assertEqual(self.ui.elevator_1_down_indicator.styleSheet(), on)
        self.assertEqual(self.ui.elevator_2_up_indicator.styleSheet(), off)
        self.assertEqual(self.ui.elevator_2_down_indicator.styleSheet(), on)


    def test_update_button(self):
        """Test the update_button() method of the ExternalUI class."""
        # Mock methods to isolate update_state() functionality.
        self.ui.checkTargetUp = MagicMock()
        self.ui.checkTargetDown = MagicMock()

        # Test case 1: No target.
        self.ui.checkTargetUp.return_value = False
        self.ui.checkTargetDown.return_value = False
        self.ui.update_button()
        self.assertEqual(self.ui.up_button.styleSheet(), circle_button_style)
        self.assertEqual(self.ui.down_button.styleSheet(), circle_button_style)

        # Test case 2: With target.
        self.ui.checkTargetUp.return_value = True
        self.ui.checkTargetDown.return_value = True
        self.ui.update_button()
        self.assertEqual(self.ui.up_button.styleSheet(), circle_button_style_on)
        self.assertEqual(self.ui.down_button.styleSheet(), circle_button_style_on)


    def test_push_up_button(self):
        """Test the push_up_button() method of the ExternalUI class."""
        with patch.object(self.ui.processor, 'process_ExternalUI_requests') as mock_process:
            self.ui.push_up_button()
            mock_process.assert_called_once_with(f"call_up@{self.ui.floor}")
            self.assertEqual(self.ui.up_button.styleSheet(), circle_button_style_on)


    def test_push_down_button(self):
        """Test the push_down_button() method of the ExternalUI class."""
        with patch.object(self.ui.processor, 'process_ExternalUI_requests') as mock_process:
            self.ui.push_down_button()
            mock_process.assert_called_once_with(f"call_down@{self.ui.floor}")
            self.assertEqual(self.ui.down_button.styleSheet(), circle_button_style_on)
    

    def test_checkOpen(self):
        """Test the checkOpen(processor) method of the ExternalUI class."""
        # Choose the elevator processor for elevator 1 as an example.
        processor = self.ui.processor.elevator_processors[0]

        # Test case 1: The elevator door is open and on the same floor.
        processor.elevator.current_floor = 2
        processor.elevator.current_state = ElevatorState.stopped_door_opened
        self.assertTrue(self.ui.checkOpen(processor))

        # Test case 2: The elevator door is closed and on a different floor.
        processor.elevator.current_floor = 2
        processor.elevator.current_state = ElevatorState.stopped_door_closed
        self.assertFalse(self.ui.checkOpen(processor))


    def test_checkTargetUp(self):
        """Test the checkTargetUp(floor) method of the ExternalUI class."""
        # Set up the system processor.
        processor = self.ui.processor

        # Test case 1: Any one of the elevator has the target floor set.
        processor.elevator_processors[0].target_floor_up = [False, True, False, False]
        processor.elevator_processors[1].target_floor_up = [False, False, False, False]
        self.assertTrue(self.ui.checkTargetUp(1))

        # Test case 2: Neither elevator has the target floor set.
        processor.elevator_processors[0].target_floor_up = [False, False, False, False]
        processor.elevator_processors[1].target_floor_up = [False, False, False, False]
        self.assertFalse(self.ui.checkTargetUp(1))

        # Test case 3: The floor is -1 (should be adjusted to 0)
        processor.elevator_processors[0].target_floor_up = [False, False, False, False]
        processor.elevator_processors[1].target_floor_up = [True, False, False, False]
        self.assertTrue(self.ui.checkTargetUp(-1))
    

    def test_checkTargetDown(self):
        """Test the checkTargetDown(floor) method of the ExternalUI class."""
        # Set up the system processor.
        processor = self.ui.processor

        # Test case 1: Any one of the elevator has the target floor set.
        processor.elevator_processors[0].target_floor_down = [False, True, False, False]
        processor.elevator_processors[1].target_floor_down = [False, False, False, False]
        self.assertTrue(self.ui.checkTargetDown(1))

        # Test case 2: Neither elevator has the target floor set.
        processor.elevator_processors[0].target_floor_down = [False, False, False, False]
        processor.elevator_processors[1].target_floor_down = [False, False, False, False]
        self.assertFalse(self.ui.checkTargetDown(1))

        # Test case 3: The floor is -1 (should be adjusted to 0)
        processor.elevator_processors[0].target_floor_down = [False, False, False, False]
        processor.elevator_processors[1].target_floor_down = [True, False, False, False]
        self.assertTrue(self.ui.checkTargetDown(-1))


if __name__ == "__main__":
    unittest.main()
