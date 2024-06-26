import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication

import sys
sys.path.append("Development/YourCodeExample")
from processor import SystemProcessor
from elevator import ElevatorState


'''
    TestSystemProcessor class contains unit tests for SystemProcessor class.
    Please run this file under the root path, i.e. Elevator.
'''
class TestSystemProcessor(unittest.TestCase):
    
    def setUp(self):
        # Set up the SystemProcessor instance and its components for testing
        app = QApplication(sys.argv)
        self.system_processor = SystemProcessor()
        self.processor1 = self.system_processor.elevator_processors[0]
        self.processor2 = self.system_processor.elevator_processors[1]


    def test_update(self):
        """Test case for update() method of the SystemProcessor class."""
        self.processor1.update = MagicMock()
        self.processor2.update = MagicMock()
        self.system_processor.update()
        self.processor1.update.assert_called_once()
        self.processor2.update.assert_called_once()


    def test_process_ExternalUI_requests_call_up(self):
        """Test case for process_ExternalUI_requests(ExterUI_MSG) method of the SystemProcessor class."""

        # Test case 1: Floor is already a target floor for any of the processors.
        # Expected result: Call the processor 1.
        self.processor1.target_floor_up[2] = True
        self.processor2.target_floor_up[2] = False
        self.processor1.target_floor_down[2] = False
        self.processor2.target_floor_down[2] = False
        self.system_processor.process_ExternalUI_requests("call_up@2")
        self.assertTrue(self.processor1.target_floor_up[2])
        self.assertFalse(self.processor2.target_floor_up[2])

        # Test case 2: Floor is already a target down floor for one processor.
        # Expected result: Call the processor 2.
        self.processor1.target_floor_up[2] = False
        self.processor2.target_floor_up[2] = False
        self.processor1.target_floor_down[2] = True
        self.processor2.target_floor_down[2] = False
        self.system_processor.process_ExternalUI_requests("call_up@2")
        self.assertFalse(self.processor1.target_floor_up[2])
        self.assertTrue(self.processor2.target_floor_up[2])

        # Test case 3: Calculate arrival times and decide which elevator to assign.
        # Expected result: Call the processor 1.
        self.processor1.target_floor_up[3] = False
        self.processor2.target_floor_up[3] = False
        self.processor1.target_floor_down[3] = False
        self.processor2.target_floor_down[3] = False
        self.system_processor.getUpTime = MagicMock(return_value=(5, 10))
        self.system_processor.process_ExternalUI_requests("call_up@3")
        self.assertTrue(self.processor1.target_floor_up[3])
        self.assertFalse(self.processor2.target_floor_up[3])

        # Test case 4: Call floor number -1.
        # Expected result: Call the processor 1.
        self.processor1.target_floor_up[0] = True
        self.processor2.target_floor_up[0] = False
        self.processor1.target_floor_down[0] = False
        self.processor2.target_floor_down[0] = False
        self.system_processor.process_ExternalUI_requests("call_up@-1")
        self.assertTrue(self.processor1.target_floor_up[0])
        self.assertFalse(self.processor2.target_floor_up[0])

        # Test case 5: Floor is already a target floor for any of the processors.
        # Expected result: Call the processor 1.
        self.processor1.target_floor_down[3] = True
        self.processor2.target_floor_down[3] = False
        self.processor1.target_floor_up[3] = False
        self.processor2.target_floor_up[3] = False
        self.system_processor.process_ExternalUI_requests("call_down@3")
        self.assertTrue(self.processor1.target_floor_down[3])
        self.assertFalse(self.processor2.target_floor_down[3])

        # Test case 6: Floor is already a target up floor for one processor.
        # Expected result: Call the processor 2.
        self.processor1.target_floor_down[3] = False
        self.processor2.target_floor_down[3] = False
        self.processor1.target_floor_up[3] = True
        self.processor2.target_floor_up[3] = False
        self.system_processor.process_ExternalUI_requests("call_down@3")
        self.assertFalse(self.processor1.target_floor_down[3])
        self.assertTrue(self.processor2.target_floor_down[3])

        # Test case 7: Calculate arrival times and decide which elevator to assign.
        # Expected result: Call the processor 1.
        self.processor1.target_floor_down[2] = False
        self.processor2.target_floor_down[2] = False
        self.processor1.target_floor_up[2] = False
        self.processor2.target_floor_up[2] = False
        self.system_processor.getDownTime = MagicMock(return_value=(5, 3))
        self.system_processor.process_ExternalUI_requests("call_down@2")
        self.assertFalse(self.processor1.target_floor_down[2])
        self.assertTrue(self.processor2.target_floor_down[2])

        # Test case 8: Call floor number -1.
        # Expected result: Call the processor 1.
        self.processor1.target_floor_down[0] = True
        self.processor2.target_floor_down[0] = False
        self.processor1.target_floor_up[0] = False
        self.processor2.target_floor_up[0] = False
        self.system_processor.process_ExternalUI_requests("call_down@-1")
        self.assertTrue(self.processor1.target_floor_down[0])
        self.assertFalse(self.processor2.target_floor_down[0])


    def test_receive_eleProcessor_MSG(self):
        """Test case for receive_eleProcessor_MSG(message) method of the SystemProcessor class."""

        # Mock methods to isolate receive_eleProcessor_MSG() functionality.
        self.processor1.checkOpen = MagicMock()
        self.processor1.open_door = MagicMock()
        self.processor2.checkOpen = MagicMock()
        self.processor2.open_door = MagicMock()

        # Test case 1: Up floor arrive message for elevator 1.
        # Expected result: Elevator 1 opens door and sets state to stopped_door_closed.
        self.processor1.checkOpen = MagicMock(return_value=True)
        self.system_processor.receive_eleProcessor_MSG("up_floor_2_arrived#1")
        self.processor1.open_door.assert_called_once()
        self.assertEqual(self.processor1.elevator.current_state, ElevatorState.stopped_door_closed)

        # Reset mock calls for the next test case.
        self.processor1.checkOpen.reset_mock()
        self.processor1.open_door.reset_mock()
        self.processor2.checkOpen.reset_mock()
        self.processor2.open_door.reset_mock()
        
        # Test case 2: Floor arrive message for elevator 2.
        # Expected result: Elevator 2 opens door and sets state to stopped_door_closed.
        self.processor2.checkOpen = MagicMock(return_value=True)
        self.system_processor.receive_eleProcessor_MSG("floor_1_arrived#2")
        self.processor2.open_door.assert_called_once()
        self.assertEqual(self.processor2.elevator.current_state, ElevatorState.stopped_door_closed)
    
    
    def test_getUpTime(self):
        """Test case for getUpTime(floor) method of the SystemProcessor class."""
        self.processor1.compute_callup_time = MagicMock(return_value=5)
        self.processor2.compute_callup_time = MagicMock(return_value=10)
        up_time = self.system_processor.getUpTime(2)
        self.assertEqual(up_time, (5, 10))
        self.processor1.compute_callup_time.assert_called_once_with(2)
        self.processor2.compute_callup_time.assert_called_once_with(2)


    def test_getDownTime(self):
        """Test case for getDownTime(floor) method of the SystemProcessor class."""
        self.processor1.compute_calldown_time = MagicMock(return_value=8)
        self.processor2.compute_calldown_time = MagicMock(return_value=6)
        down_time = self.system_processor.getDownTime(3)
        self.assertEqual(down_time, (8, 6))
        self.processor1.compute_calldown_time.assert_called_once_with(3)
        self.processor2.compute_calldown_time.assert_called_once_with(3)

if __name__ == '__main__':
    unittest.main()
