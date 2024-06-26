import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication

import sys
sys.path.append("Development/YourCodeExample")
from processor import SystemProcessor
from elevator import ElevatorState, DirectionState


'''
    TestElevatorProcessor class contains unit tests for ElevatorProcessor class.
    Please run this file under the root path, i.e. Elevator.
'''
class TestElevatorProcessor(unittest.TestCase):

    def setUp(self):
        app = QApplication(sys.argv)
        self.processor = SystemProcessor().elevator_processors[0]


    def test_getStaticDoor(self):
        """Test case for getStaticDoor() method of the ElevatorProcessor class."""
        self.assertEqual(self.processor.getStaticDoor(), 2)


    def test_getStaticTimer(self):
        """Test case for getStaticTimer() method of the ElevatorProcessor class."""
        self.assertEqual(self.processor.getStaticTimer(), 5)


    def test_update(self):
        """Test case for update() method of the ElevatorProcessor class."""
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator

        # Mock methods to isolate update() functionality.
        processor.update_door = MagicMock()
        processor.update_floor = MagicMock()
        processor.update_direction = MagicMock()
        processor.update_state = MagicMock()
        processor.checkArrive = MagicMock()
        processor.smg_to_SystemProcessor = MagicMock()

        # Test case 1: Elevator arrives at a floor with idle direction.
        # Expected result: smg_to_SystemProcessor should be called with the correct message.
        elevator.ele_id = 1
        elevator.current_floor = 2
        elevator.direction = DirectionState.idle
        processor.checkArrive.return_value = True
        processor.update()
        processor.update_door.assert_called_once()
        processor.update_floor.assert_called_once()
        processor.update_direction.assert_called_once()
        processor.update_state.assert_called_once()
        processor.checkArrive.assert_called_once()
        processor.smg_to_SystemProcessor.assert_called_once_with("floor_2_arrived#1")
        
        # Reset mock calls for the next test case.
        processor.update_door.reset_mock()
        processor.update_floor.reset_mock()
        processor.update_direction.reset_mock()
        processor.update_state.reset_mock()
        processor.checkArrive.reset_mock()
        processor.smg_to_SystemProcessor.reset_mock()

        # Test case 2: Elevator arrives at a floor with up direction.
        # Expected result: smg_to_SystemProcessor should be called with the correct message.
        elevator.ele_id = 1
        elevator.current_floor = 3
        elevator.direction = DirectionState.up
        processor.checkArrive.return_value = True
        processor.update()
        processor.update_door.assert_called_once()
        processor.update_floor.assert_called_once()
        processor.update_direction.assert_called_once()
        processor.update_state.assert_called_once()
        processor.checkArrive.assert_called_once()
        processor.smg_to_SystemProcessor.assert_called_once_with("up_floor_3_arrived#1")
        
        # Reset mock calls for the next test case.
        processor.update_door.reset_mock()
        processor.update_floor.reset_mock()
        processor.update_direction.reset_mock()
        processor.update_state.reset_mock()
        processor.checkArrive.reset_mock()
        processor.smg_to_SystemProcessor.reset_mock()

        # Test case 3: Elevator arrives at a floor with down direction.
        # Expected result: smg_to_SystemProcessor should be called with the correct message.
        elevator.ele_id = 1
        elevator.current_floor = 1
        elevator.direction = DirectionState.down
        processor.checkArrive.return_value = True
        processor.update()
        processor.update_door.assert_called_once()
        processor.update_floor.assert_called_once()
        processor.update_direction.assert_called_once()
        processor.update_state.assert_called_once()
        processor.checkArrive.assert_called_once()
        processor.smg_to_SystemProcessor.assert_called_once_with("down_floor_1_arrived#1")
        
        # Reset mock calls for the next test case.
        processor.update_door.reset_mock()
        processor.update_floor.reset_mock()
        processor.update_direction.reset_mock()
        processor.update_state.reset_mock()
        processor.checkArrive.reset_mock()
        processor.smg_to_SystemProcessor.reset_mock()

        # Test case 4: Elevator does not arrive at a floor.
        # Expected result: smg_to_SystemProcessor should not be called.
        elevator.ele_id = 1
        elevator.current_floor = 1
        elevator.direction = DirectionState.up
        processor.checkArrive.return_value = False
        processor.update()
        processor.update_door.assert_called_once()
        processor.update_floor.assert_called_once()
        processor.update_direction.assert_called_once()
        processor.update_state.assert_called_once()
        processor.checkArrive.assert_called_once()
        processor.smg_to_SystemProcessor.assert_not_called()


    def test_update_floor(self):
        """Test case for update_floor() method of the ElevatorProcessor class."""
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator

        # Test case 1: Elevator moving up from floor 1.
        # Expected result: Elevator should move to floor 2.
        elevator.current_floor = 1
        elevator.direction = DirectionState.up
        elevator.current_state = ElevatorState.up
        processor.update_floor()
        self.assertEqual(elevator.current_floor, 2)

        # Test case 2: Elevator moving up from floor -1.
        # Expected result: Elevator should move to floor 1.
        elevator.current_floor = -1
        elevator.direction = DirectionState.up
        elevator.current_state = ElevatorState.up
        processor.update_floor()
        self.assertEqual(elevator.current_floor, 1)

        # Test case 3: Elevator moving down from floor 1.
        # Expected result: Elevator should move to floor -1.
        elevator.current_floor = 1
        elevator.direction = DirectionState.down
        elevator.current_state = ElevatorState.down
        processor.update_floor()
        self.assertEqual(elevator.current_floor, -1)

        # Test case 4: Elevator moving down from floor 2.
        # Expected result: Elevator should move to floor -1.
        elevator.current_floor = 2
        elevator.direction = DirectionState.down
        elevator.current_state = ElevatorState.down
        processor.update_floor()
        self.assertEqual(elevator.current_floor, 1)

        # Test case 5: Elevator idle at floor 1.
        # Expected result: Elevator should remain at floor 1.
        elevator.current_floor = 1
        elevator.direction = DirectionState.idle
        elevator.current_state = ElevatorState.stopped_door_closed
        processor.update_floor()
        self.assertEqual(elevator.current_floor, 1)


    def test_update_door(self):
        """Test case for update_door() method of the ElevatorProcessor class."""
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator

        # Test case 1: Elevator state is stopped_opening_door and door_outside_length is 0.
        # Expected result: Elevator state should be stopped_door_opened, open_timer should be set.
        elevator.current_state = ElevatorState.stopped_opening_door
        processor.door_outside_length = 0
        processor.update_door()
        self.assertEqual(elevator.current_state, ElevatorState.stopped_door_opened)
        self.assertEqual(processor.open_timer, processor.getStaticTimer())

        # Test case 2: Elevator state is stopped_opening_door and door_outside_length is not 0.
        # Expected result: door_outside_length should decrement by 1.
        elevator.current_state = ElevatorState.stopped_opening_door
        processor.door_outside_length = 1
        processor.update_door()
        self.assertEqual(processor.door_outside_length, 0)

        # Test case 3: Elevator state is stopped_closing_door and door_outside_length equals getStaticDoor().
        # Expected result: Elevator state should be stopped_door_closed.
        elevator.current_state = ElevatorState.stopped_closing_door
        processor.door_outside_length = processor.getStaticDoor()
        processor.update_door()
        self.assertEqual(elevator.current_state, ElevatorState.stopped_door_closed)

        # Test case 4: Elevator state is stopped_closing_door and door_outside_length is less than getStaticDoor().
        # Expected result: door_outside_length should increment by 1.
        elevator.current_state = ElevatorState.stopped_closing_door
        processor.door_outside_length = 1
        processor.update_door()
        self.assertEqual(processor.door_outside_length, 2)

        # Test case 5: Elevator state is stopped_door_opened and open_timer is 0.
        # Expected result: Elevator state should be stopped_closing_door.
        elevator.current_state = ElevatorState.stopped_door_opened
        processor.open_timer = 0
        processor.update_door()
        self.assertEqual(elevator.current_state, ElevatorState.stopped_closing_door)

        # Test case 6: Elevator state is stopped_door_opened and open_timer is greater than 0.
        # Expected result: open_timer should decrement by 1.
        elevator.current_state = ElevatorState.stopped_door_opened
        processor.open_timer = 3
        processor.update_door()
        self.assertEqual(processor.open_timer, 2)


    def test_update_direction(self):
        """Test case for update_direction() method of the ElevatorProcessor class."""
        processor = self.processor
        elevator = processor.elevator

        # Test case 1: Elevator direction is idle and there are targets above.
        elevator.current_floor = 1
        elevator.direction = DirectionState.idle
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, True, False]
        processor.target_floor_down = [False, False, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.up)

        # Test case 2: Elevator direction is idle and there are targets below.
        elevator.current_floor = 2
        elevator.direction = DirectionState.idle
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, True, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.down)

        # Test case 3: Elevator direction is idle and targets are on both sides, closer target is above.
        elevator.current_floor = 1
        elevator.direction = DirectionState.idle
        processor.target_floor = [False, True, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, True, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.up)

        # Test case 4: Elevator direction is idle and targets are on both sides, closer target is below.
        elevator.current_floor = 3
        elevator.direction = DirectionState.idle
        processor.target_floor = [False, False, True, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, True, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.down)

        # Test case 5: Elevator direction is up and there are targets above.
        elevator.current_floor = 1
        elevator.direction = DirectionState.up
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, True, False]
        processor.target_floor_down = [False, False, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.up)

        # Test case 6: Elevator direction is up and there are targets below.
        elevator.current_floor = 2
        elevator.direction = DirectionState.up
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, True, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.down)

        # Test case 7: Elevator direction is down and there are targets below.
        elevator.current_floor = 1
        elevator.direction = DirectionState.down
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, True, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.down)

        # Test case 8: Elevator direction is down and there are targets above.
        elevator.current_floor = 1
        elevator.direction = DirectionState.down
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, True, False]
        processor.target_floor_down = [False, False, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.up)

        # Test case 9: Elevator direction is up and no targets are found.
        elevator.current_floor = 1
        elevator.direction = DirectionState.up
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.idle)

        # Test case 10: Elevator direction is down and no targets are found.
        elevator.current_floor = 1
        elevator.direction = DirectionState.down
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, False, False]
        processor.update_direction()
        self.assertEqual(elevator.direction, DirectionState.idle)


    def test_update_state(self):
        """Test case for update_state() method of the ElevatorProcessor class."""
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator

        # Test case 1: Elevator door is closed and direction is up.
        elevator.current_state = ElevatorState.stopped_door_closed
        elevator.direction = DirectionState.up
        processor.update_state()
        self.assertEqual(elevator.current_state, ElevatorState.up)

        # Test case 2: Elevator door is closed and direction is down.
        elevator.current_state = ElevatorState.stopped_door_closed
        elevator.direction = DirectionState.down
        processor.update_state()
        self.assertEqual(elevator.current_state, ElevatorState.down)

        # Test case 3: Elevator door is opened and direction is up.
        elevator.current_state = ElevatorState.stopped_door_opened
        elevator.direction = DirectionState.up
        processor.update_state()
        self.assertEqual(elevator.current_state, ElevatorState.stopped_door_opened)


    def test_process_InternalUI_requests(self):
        """Test case for process_InternalUI_requests(InterUI_MSG) method of the ElevatorProcessor class."""

        # Set up the system processor and get the first elevator processor.
        processor = self.processor

        # Mock methods to isolate process_InternalUI_requests() functionality.
        processor.open_door = MagicMock()
        processor.close_door = MagicMock()

        # Test case 1: Internal UI request to open the door.
        # Expected result: open_door() should be called.
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, False, False]
        processor.process_InternalUI_requests("open_door")
        processor.open_door.assert_called_once()
        processor.close_door.assert_not_called()

        # Reset mock calls for the next test case.
        processor.open_door.reset_mock()
        processor.close_door.reset_mock()

        # Test case 2: Internal UI request to close the door.
        # Expected result: close_door() should be called.
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, False, False]
        processor.process_InternalUI_requests("close_door")
        processor.close_door.assert_called_once()
        processor.open_door.assert_not_called()

        # Test case 3: Internal UI request to select floor 2.
        # Expected result: target_floor[2] should be set to True.
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, False, False]
        processor.process_InternalUI_requests("select_floor@2#1")
        self.assertTrue(processor.target_floor[2])

        # Test case 4: Internal UI request to select floor -1.
        # Expected result: target_floor[0] should be set to True.
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, False, False]
        processor.process_InternalUI_requests("select_floor@-1#1")
        self.assertTrue(processor.target_floor[0])


    def test_open_door(self):
        """Test case for open_door() method of the ElevatorProcessor class."""
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator
        
        # Test case 1: Elevator state is stopped_door_closed.
        # Expected result: The state of elevator should be ElevatorState.stopped_opening_door.
        elevator.current_state = ElevatorState.stopped_door_closed
        self.assertTrue(processor.open_door())
        self.assertEqual(elevator.current_state, ElevatorState.stopped_opening_door)
        
        # Test case 2: Elevator state is stopped_closing_door.
        # Expected result: The state of elevator should be ElevatorState.stopped_opening_door.
        elevator.current_state = ElevatorState.stopped_closing_door
        self.assertTrue(processor.open_door())
        self.assertEqual(elevator.current_state, ElevatorState.stopped_opening_door)
        
        
        # Test case 3: Elevator state is not stopped_door_closed or stopped_closing_door.
        # Expected result: The state of elevator should not change to be ElevatorState.stopped_opening_door.
        elevator.current_state = ElevatorState.up
        self.assertFalse(processor.open_door())
        self.assertEqual(elevator.current_state, ElevatorState.up)
        

    def test_close_door(self):
        """Test case for close_door() method of the ElevatorProcessor class."""
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator
        
        # Test case 1: Elevator state is stopped_door_opened.
        # Expected result: The state of elevator should be ElevatorState.stopped_door_closed.
        elevator.current_state = ElevatorState.stopped_door_opened
        self.assertTrue(processor.close_door())
        self.assertEqual(elevator.current_state, ElevatorState.stopped_door_closed)
        
        # Test case 2: Elevator state is stopped_opening_door.
        # Expected result: The state of elevator should be ElevatorState.stopped_door_closed.
        elevator.current_state = ElevatorState.stopped_opening_door
        self.assertTrue(processor.close_door())
        self.assertEqual(elevator.current_state, ElevatorState.stopped_door_closed)
        
        # Test case 3: Elevator state is not stopped_door_opened or stopped_opening_door.
        # Expected result: The state of elevator should not change to be ElevatorState.stopped_door_closed.
        elevator.current_state = ElevatorState.up
        self.assertFalse(processor.close_door())
        self.assertEqual(elevator.current_state, ElevatorState.up)


    def test_checkOpen(self):
        """Test case for checkOpen() method of the ElevatorProcessor class."""
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator

        # Test case 1: Elevator state is stopped with the door closed.
        # Expected result: checkOpen() should return False.
        elevator.current_state = ElevatorState.stopped_door_closed
        self.assertEqual(processor.checkOpen(), False)

        # Test case 2: Elevator state is stopped with the door opened.
        # Expected result: checkOpen() should return True.
        elevator.current_state = ElevatorState.stopped_door_opened
        self.assertEqual(processor.checkOpen(), True)

    
    def test_checkArrive(self):
        """Test case for checkArrive() method of the ElevatorProcessor class."""
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator

        # Test case 1: Elevator at floor 1, direction idle, no target floors.
        # Expected result: checkArrive() should return False.
        elevator.floor = 1
        elevator.direction = DirectionState.idle
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, False, False]
        self.assertEqual(processor.checkArrive(), False)

        # Test case 2: Elevator at floor 1, direction idle, target floor 1.
        # Expected result: checkArrive() should return True.
        elevator.floor = 1
        elevator.direction = DirectionState.idle
        processor.target_floor = [False, True, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, False, False, False]
        self.assertEqual(processor.checkArrive(), True)

        # Test case 3: Elevator at floor 1, direction up, target floor up at 1.
        # Expected result: checkArrive() should return True.
        elevator.floor = 1
        elevator.direction = DirectionState.up
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, True, False, False]
        processor.target_floor_down = [False, False, False, False]
        self.assertEqual(processor.checkArrive(), True)

        # Test case 4: Elevator at floor 1, direction down, target floor down at 1.
        # Expected result: checkArrive() should return True.
        elevator.floor = 1
        elevator.direction = DirectionState.down
        processor.target_floor = [False, False, False, False]
        processor.target_floor_up = [False, False, False, False]
        processor.target_floor_down = [False, True, False, False]
        self.assertEqual(processor.checkArrive(), True)


    def test_compute_callup_time(self):
        '''Test case for compute_callup_time(floor) method of the ElevatorProcessor class.'''
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator

        # Test case 1: Elevator is idle at floor 1 with no target floors.
        # Expected result: compute_callup_time(2) should return 1.
        elevator.direction = DirectionState.idle
        elevator.current_floor = 1
        processor.target_floor = [False, False, False, False]
        self.assertEqual(processor.compute_callup_time(2), 1)

        # Test case 2: Elevator is going down at floor 2 with a target floor at 0.
        # Expected result: compute_callup_time(3) should return 5.
        elevator.direction = DirectionState.down
        elevator.current_floor = 2
        processor.target_floor = [True, False, False, False]
        self.assertEqual(processor.compute_callup_time(3), 5)

        # Test case 3: Elevator is going up at floor 1 with a target floor at 0.
        # Expected result: compute_callup_time(2) should return 1.
        elevator.direction = DirectionState.up
        elevator.current_floor = 1
        processor.target_floor = [True, False, False, False]
        self.assertEqual(processor.compute_callup_time(2), 1)

        # Test case 4: Elevator is going up at floor 1 with a target floor at 3.
        # Expected result: compute_callup_time(-1) should return 5.
        elevator.direction = DirectionState.up
        elevator.current_floor = 1
        processor.target_floor = [False, False, False, True]
        self.assertEqual(processor.compute_callup_time(-1), 5)


    def test_compute_calldown_time(self):
        '''Test case for compute_calldown_time(floor) method of the ElevatorProcessor class.'''
        # Set up the system processor and get the first elevator processor.
        processor = self.processor
        elevator = processor.elevator

        # Test case 1: Elevator is idle at floor 1 with no target floors.
        # Expected result: compute_calldown_time(2) should return 1.
        elevator.direction = DirectionState.idle
        elevator.current_floor = 1
        processor.target_floor = [False, False, False, False]
        self.assertEqual(processor.compute_calldown_time(2), 1)

        # Test case 2: Elevator is going down at floor 2 with a target floor at 0.
        # Expected result: compute_calldown_time(3) should return 5.
        elevator.direction = DirectionState.down
        elevator.current_floor = 2
        processor.target_floor = [True, False, False, False]
        self.assertEqual(processor.compute_calldown_time(3), 5)

        # Test case 3: Elevator is going down at floor 2 with a target floor at 0.
        # Expected result: compute_calldown_time(1) should return 1.
        elevator.direction = DirectionState.down
        elevator.current_floor = 2
        processor.target_floor = [True, False, False, False]
        self.assertEqual(processor.compute_calldown_time(1), 1)

        # Test case 4: Elevator is going up at floor 1 with a target floor at 3.
        # Expected result: compute_calldown_time(-1) should return 5.
        elevator.direction = DirectionState.up
        elevator.current_floor = 1
        processor.target_floor = [False, False, False, True]
        self.assertEqual(processor.compute_calldown_time(-1), 5)


if __name__ == '__main__':
    unittest.main()
