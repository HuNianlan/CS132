import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
sys.path.append("Development/YourCodeExample")
from processor import SystemProcessor
from elevator import DirectionState
from internalUI import InternalUI
from UIsettings import on, off, circle_button_style, circle_button_style_on


'''
    TestInternalUI class contains unit tests for InternalUI class.
    Please run this file under the root path, i.e. Elevator.
'''
class TestInternalUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test environment and set class-level variables"""
        cls.app = QApplication(sys.argv)

    def setUp(self):
        """Initialization of each test case"""
        self.ui = InternalUI(SystemProcessor().elevator_processors[0])
        self.ui.show()

    def tearDown(self):
        """Cleanup after each test case"""
        self.ui.close()

    @classmethod
    def tearDownClass(cls):
        """Cleanup work after all test cases are executed"""
        cls.app.quit()
    

    def test_update(self):
        """Test case for update() method of the InternalUI class."""

        # Mock methods to isolate update() functionality.
        self.ui.update_time = MagicMock()
        self.ui.update_state = MagicMock()
        self.ui.update_floor = MagicMock()
        self.ui.update_direction = MagicMock()
        self.ui.update_floor_button = MagicMock()

        self.ui.update()
        self.ui.update_time.assert_called_once()
        self.ui.update_state.assert_called_once()
        self.ui.update_floor.assert_called_once()
        self.ui.update_direction.assert_called_once()
        self.ui.update_floor_button.assert_called_once()


    def test_update_time(self):
        """Test case for update_time() method of the InternalUI class."""
        self.ui.update_time()
        current_time = QDateTime.currentDateTime().toString('hh:mm:ss')
        expected_text = f'Time: {current_time}'
        self.assertEqual(self.ui.time_label.text(), expected_text)


    def test_update_state(self):
        """Test update_state() method of the InternalUI class."""
        
        # Mock methods to isolate update() functionality.
        self.ui.processor.checkOpen = MagicMock()

        # Test case 1: Elevator door is open.
        self.ui.processor.checkOpen.return_value = True
        self.ui.update_state()
        self.assertEqual(self.ui.open_close_state.text(), "<|>")
        self.assertEqual(self.ui.open_close_state.styleSheet(), "color:green;")

        # Reset mock calls for the next test case.
        self.ui.processor.checkOpen.reset_mock()
    
        # Test case 2: Elevator door is closed.
        self.ui.processor.checkOpen.return_value = False
        self.ui.update_state()
        self.assertEqual(self.ui.open_close_state.text(), ">|<")
        self.assertEqual(self.ui.open_close_state.styleSheet(), "color:black;")


    def test_update_floor(self):
        """Test the update_floor() method of the InternalUI class."""
        self.ui.update_floor()
        self.assertEqual(self.ui.floor_label.text(), f'Floor: {self.ui.processor.elevator.current_floor}')


    def test_update_floor_button(self):
        """Test the update_floor_button() method of the InternalUI class."""
        # Test case 1: No target.
        self.ui.processor.target_floor = [False, False, False, False]
        self.ui.update_floor_button()
        self.assertEqual(self.ui.floor_button_b.styleSheet(), circle_button_style)
        self.assertEqual(self.ui.floor_button_1.styleSheet(), circle_button_style)
        self.assertEqual(self.ui.floor_button_2.styleSheet(), circle_button_style)
        self.assertEqual(self.ui.floor_button_3.styleSheet(), circle_button_style)

        # Test case 2: With target.
        self.ui.processor.target_floor = [True, True, True, True]
        self.ui.update_floor_button()
        self.assertEqual(self.ui.floor_button_b.styleSheet(), circle_button_style_on)
        self.assertEqual(self.ui.floor_button_1.styleSheet(), circle_button_style_on)
        self.assertEqual(self.ui.floor_button_2.styleSheet(), circle_button_style_on)
        self.assertEqual(self.ui.floor_button_3.styleSheet(), circle_button_style_on)


    def test_update_direction(self):
        """Test the update_direction() method of the InternalUI class."""

        # Test case 1: Elevator is idle.
        self.ui.processor.elevator.direction = DirectionState.idle
        self.ui.update_direction()
        self.assertEqual(self.ui.direction_label_up.styleSheet(), off)
        self.assertEqual(self.ui.direction_label_down.styleSheet(), off)

        # Test case 2: Elevator is up.
        self.ui.processor.elevator.direction = DirectionState.up
        self.ui.update_direction()
        self.assertEqual(self.ui.direction_label_up.styleSheet(), on)
        self.assertEqual(self.ui.direction_label_down.styleSheet(), off)

        # Test case 3: Elevator is down.
        self.ui.processor.elevator.direction = DirectionState.down
        self.ui.update_direction()
        self.assertEqual(self.ui.direction_label_up.styleSheet(), off)
        self.assertEqual(self.ui.direction_label_down.styleSheet(), on)


    def test_push_open_door_button(self):
        """Test the push_open_door_button() method of the InternalUI class."""
        with patch.object(self.ui.processor, 'process_InternalUI_requests') as mock_process:
            self.ui.push_open_door_button()
            mock_process.assert_called_once_with("open_door")


    def test_push_close_door_button(self):
        """Test the push_close_door_button() method of the InternalUI class."""
        with patch.object(self.ui.processor, 'process_InternalUI_requests') as mock_process:
            self.ui.push_close_door_button()
            mock_process.assert_called_once_with("close_door")


    def test_push_floor_button_b(self):
        """Test the push_floor_button_b() method of the InternalUI class."""
        with patch.object(self.ui.processor, 'process_InternalUI_requests') as mock_process:
            self.ui.push_floor_button_b()
            mock_process.assert_called_once_with(f"select_floor@-1#{self.ui.processor.elevator.ele_id}")
            self.assertEqual(self.ui.floor_button_b.styleSheet(), circle_button_style_on)
    

    def test_push_floor_button_1(self):
        """Test the push_floor_button_1() method of the InternalUI class."""
        with patch.object(self.ui.processor, 'process_InternalUI_requests') as mock_process:
            self.ui.push_floor_button_1()
            mock_process.assert_called_once_with(f"select_floor@1#{self.ui.processor.elevator.ele_id}")
            self.assertEqual(self.ui.floor_button_1.styleSheet(), circle_button_style_on)


    def test_push_floor_button_2(self):
        """Test the push_floor_button_2() method of the InternalUI class."""
        with patch.object(self.ui.processor, 'process_InternalUI_requests') as mock_process:
            self.ui.push_floor_button_2()
            mock_process.assert_called_once_with(f"select_floor@2#{self.ui.processor.elevator.ele_id}")
            self.assertEqual(self.ui.floor_button_2.styleSheet(), circle_button_style_on)


    def test_push_floor_button_3(self):
        """Test the push_floor_button_3() method of the InternalUI class."""
        with patch.object(self.ui.processor, 'process_InternalUI_requests') as mock_process:
            self.ui.push_floor_button_3()
            mock_process.assert_called_once_with(f"select_floor@3#{self.ui.processor.elevator.ele_id}")
            self.assertEqual(self.ui.floor_button_3.styleSheet(), circle_button_style_on)


if __name__ == "__main__":
    unittest.main()