from enum import IntEnum

class ElevatorState(IntEnum):
    up = 0
    down = 1
    stopped_door_closed = 2
    stopped_door_opened = 3
    stopped_opening_door = 4
    stopped_closing_door = 5

class DirectionState(IntEnum):
    up = 0
    down = 1
    idle = 2

class Elevator: 
    def __init__(self, ele_id):
        self.ele_id = ele_id
        self.current_floor = 1
        self.current_state = ElevatorState.stopped_door_closed
        self.direction = DirectionState.idle
        self.ele_processor = None
    
    def setProcessor(self, processor):
        self.ele_processor = processor
    
    def reset(self):
        self.current_floor = 1
        self.current_state = ElevatorState.stopped_door_closed
        self.ele_processor.target_floor = [False, False, False, False]
        self.ele_processor.target_floor_up = [False, False, False, False]
        self.ele_processor.target_floor_down = [False, False, False, False]
    