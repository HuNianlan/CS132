from elevator import Elevator, ElevatorState, DirectionState
from externalUI import ExternalUI
from internalUI import InternalUI
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

Elevator1 = Elevator(1)
Elevator2 = Elevator(2)
Elevators = [Elevator1,Elevator2]



## internalUI 直接向ele系统发送信息(有效信息进一步传递到systemprocessor),通过pressbutton连接，exteralUI向systemProcessor 发送信息， systemProcessor 将处理过的信息发送给eleprocessor，进行电梯调度


    # //available user operation

    # "open_door"
    # "close_door"
    # "call_up": ["-1", "1", "2"], //For example, call_up@1 means a user on the first floor presses the button to call the elevator to go upwards.
    # "call_down": ["3", "2", "1"], //For instance, call_down@3 signifies a user on the third floor pressing the button to call the elevator to go downwards.
    # "select_floor": ["-1#1", "-1#2", "1#1", "1#2", "2#1", "2#2", "3#1", "3#2"], //For example, select_floor@2#1 means a user in elevator #1 selects to go to the second floor.
    # "reset": When your elevator system receives a reset signal, it should reset the elevator's state machine to its initial state

    # //available system event

    # "door_opened": ["#1", "#2"], door_opened#1 means the doors of elevator #1 have opened.
    # "door_closed": ["#1", "#2"], door_closed#1 means the doors of elevator #1 have closed.
    # "floor_arrived":["up","down",""],["-1","1","2","3"],["#1", "#2"] //"up_floor_1_arrived#1"， indicating that elevator #1 has arrived at the first floor while moving upwards. "floor_1_arrived#1",indicating that elevator #1 has stopped at the first floor.


class ElevatorProcessor:
    def __init__(self, elevator):# elevator is an object of the elevator class
        self.elevator =  elevator
        self.system_processor = None
        self.target_floor = [False, False, False, False]
        self.target_floor_up = [False, False, False, False]
        self.target_floor_down = [False, False, False, False]
        self.door_outside_length = self.getStaticDoor()
        self.open_timer = self.getStaticTimer()
        self.elevator.setProcessor(self)
    
    def getStaticDoor(self):
        return 2
    
    def getStaticTimer(self):
        return 5
    
    def set_system_processor(self, system_processor): #link systemProcessor
        self.system_processor = system_processor
        self.internal = InternalUI(self)
    
    def update(self):
        self.update_door()
        self.update_floor()
        self.update_direction()
        self.update_state()
        if self.checkArrive():
            arrive_floor = self.elevator.current_floor
            moving_direction = self.elevator.direction
            if moving_direction == DirectionState.idle:
                moving_direction = ""
            elif moving_direction == DirectionState.up:
                moving_direction = "up_"
            elif moving_direction == DirectionState.down:
                moving_direction = "down_"
            if self.system_processor:
                self.smg_to_SystemProcessor(f"{moving_direction}floor_{arrive_floor}_arrived#{self.elevator.ele_id}")
    
    def update_floor(self):
        state = self.elevator.current_state
        direction = self.elevator.direction
        if state == ElevatorState.up or state == ElevatorState.down:
            if direction == DirectionState.up and self.elevator.current_floor < 3:
                if self.elevator.current_floor == -1:
                    self.elevator.current_floor = 1
                else:
                    self.elevator.current_floor = self.elevator.current_floor + 1
            elif direction == DirectionState.down and self.elevator.current_floor > -1:
                if self.elevator.current_floor == 1:
                    self.elevator.current_floor = -1
                else:
                    self.elevator.current_floor = self.elevator.current_floor - 1

    def update_door(self):
        state = self.elevator.current_state
        if state == ElevatorState.stopped_opening_door:
            if self.door_outside_length == 0:
                self.elevator.current_state = ElevatorState.stopped_door_opened
                self.open_timer = self.getStaticTimer()
            else:
                self.door_outside_length = self.door_outside_length - 1
        elif state == ElevatorState.stopped_closing_door:
            if self.door_outside_length == self.getStaticDoor():
                self.elevator.current_state = ElevatorState.stopped_door_closed
            else:
                self.door_outside_length = self.door_outside_length + 1
        elif state == ElevatorState.stopped_door_opened:
            if self.open_timer == 0:
                self.elevator.current_state = ElevatorState.stopped_closing_door
            else:
                self.open_timer = self.open_timer - 1

    def update_direction(self):
        floor = self.elevator.current_floor
        targets = self.target_floor
        targets_up = self.target_floor_up
        targets_down = self.target_floor_down
        direction = self.elevator.direction
        if direction == DirectionState.idle:
            for i in range(floor, 4):
                if targets_up[i] or targets_down[i]:
                    self.elevator.direction = DirectionState.up
                    return
            for i in range(floor, -1, -1):
                if targets_up[i] or targets_down[i]:
                    self.elevator.direction = DirectionState.down
                    return
            next_floor = floor
            distance = 10
            for i in range(4):
                if targets[i] and abs(i - floor) < distance:
                    distance = abs(i - floor)
                    next_floor = i
            if next_floor < floor:
                self.elevator.direction = DirectionState.down
            elif next_floor > floor:
                self.elevator.direction = DirectionState.up
        elif direction == DirectionState.up:
            for i in range(floor, 4):
                if targets[i] or targets_up[i] or targets_down[i]:
                    return
            for i in range(floor, -1, -1):
                if targets[i] or targets_up[i] or targets_down[i]:
                    self.elevator.direction = DirectionState.down
                    return
            self.elevator.direction = DirectionState.idle
        elif direction == DirectionState.down:
            for i in range(floor, -1, -1):
                if targets[i] or targets_up[i] or targets_down[i]:
                    return
            for i in range(floor, 4):
                if targets[i] or targets_up[i] or targets_down[i]:
                    self.elevator.direction = DirectionState.up
                    return
            self.elevator.direction = DirectionState.idle
    
    def update_state(self):
        direction = self.elevator.direction
        if not self.checkOpen():
            if direction == DirectionState.up:
                self.elevator.current_state = ElevatorState.up
            elif direction == DirectionState.down:
                self.elevator.current_state = ElevatorState.down
    
    def process_InternalUI_requests(self, InterUI_MSG = ""):
        if InterUI_MSG == "open_door": 
            self.open_door()
        elif InterUI_MSG == "close_door": 
            self.close_door()
        elif InterUI_MSG.startswith("select_floor"):
            select_floor = int(InterUI_MSG.split("@")[1].split("#")[0])
            select_floor = 0 if (select_floor == -1) else select_floor
            self.target_floor[select_floor] = True

    def open_door(self):
        state = self.elevator.current_state
        if state == ElevatorState.stopped_door_closed:
            self.elevator.current_state = ElevatorState.stopped_opening_door
            return True
        elif state == ElevatorState.stopped_closing_door:
            self.elevator.current_state = ElevatorState.stopped_opening_door
            return True
        else:
            return False
        
    def close_door(self):
        state = self.elevator.current_state
        if state == ElevatorState.stopped_door_opened:
            self.elevator.current_state = ElevatorState.stopped_door_closed
            return True
        elif state == ElevatorState.stopped_opening_door:
            self.elevator.current_state = ElevatorState.stopped_door_closed
            return True
        else:
            return False

    def smg_to_SystemProcessor(self,MSG):
        if self.system_processor:
            self.system_processor.receive_eleProcessor_MSG(MSG)
    
    def checkOpen(self):
        open1 = self.elevator.current_state == ElevatorState.stopped_opening_door
        open2 = self.elevator.current_state == ElevatorState.stopped_door_opened
        return open1 or open2
    
    def checkArrive(self):
        floor = self.elevator.current_floor
        floor = 0 if (floor == -1) else floor
        floors = self.target_floor
        floors_up = self.target_floor_up
        floors_down = self.target_floor_down
        flag = floors[floor]
        floors[floor] = False
        if floors_up[floor]:
            flag = True
            floors_up[floor] = False
        elif floors_down[floor]:
            flag = True
            floors_down[floor] = False
        return flag
    
    def compute_callup_time(self, floor):
        curr_floor = self.elevator.current_floor
        direction = self.elevator.direction
        floor = 0 if (floor == -1) else floor
        curr_floor = 0 if (curr_floor == -1) else curr_floor
        if direction == DirectionState.idle:
            return abs(curr_floor - floor)
        elif direction == DirectionState.down:
            min_floor = curr_floor
            for i in range(curr_floor):
                if self.target_floor[i] or self.target_floor_down[i] or self.target_floor_up[i]:
                    min_floor = i
                    break
            return abs(floor - min_floor) + (curr_floor - min_floor)
        elif direction == DirectionState.up:
            if floor >= curr_floor:
                return floor - curr_floor
            else:
                max_floor = curr_floor
                for i in range(curr_floor, 4):
                    if self.target_floor[i] or self.target_floor_down[i] or self.target_floor_up[i]:
                        max_floor = i
                return (max_floor - curr_floor) + (max_floor - floor)
    
    def compute_calldown_time(self, floor):
        curr_floor = self.elevator.current_floor
        direction = self.elevator.direction
        floor = 0 if (floor == -1) else floor
        curr_floor = 0 if (curr_floor == -1) else curr_floor
        if direction == DirectionState.idle:
            return abs(curr_floor - floor)
        elif direction == DirectionState.down:
            if floor <= curr_floor:
                return curr_floor - floor
            else:
                min_floor = curr_floor
                for i in range(curr_floor):
                    if self.target_floor[i] or self.target_floor_down[i] or self.target_floor_up[i]:
                        min_floor = i
                        break
                return abs(floor - min_floor) + (curr_floor - min_floor)
        elif direction == DirectionState.up:
            max_floor = curr_floor
            for i in range(curr_floor, 4):
                    if self.target_floor[i] or self.target_floor_down[i] or self.target_floor_up[i]:
                        max_floor = i
            return (max_floor - curr_floor) + abs(max_floor - floor)


class SystemProcessor(QMainWindow):
    return_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.elevator_processors = [ElevatorProcessor(Elevator1),ElevatorProcessor(Elevator2)]
        self.elevator_processors[0].set_system_processor(self)
        self.elevator_processors[1].set_system_processor(self)
        self.externalUIs = [
            ExternalUI(-1, self),
            ExternalUI(1, self),
            ExternalUI(2, self),
            ExternalUI(3, self)]
        self.uprequest = [False,False,False,False]
        self.downrequest = [False,False,False,False]
        self.timer.timeout.connect(self.update)

    def run(self):
        for elevator in range(2):
            self.elevator_processors[elevator].internal.move(100 + elevator * 450, 100)
            self.elevator_processors[elevator].internal.show()
        for floor in range(4):
            self.externalUIs[floor].move(100 + floor * 450, 750)
            self.externalUIs[floor].show()
    
    def update(self):
        self.elevator_processors[0].update()
        self.elevator_processors[1].update()

    def process_ExternalUI_requests(self, ExterUI_MSG = ""):
        ele_processors = self.elevator_processors
        call_floor = int(ExterUI_MSG.split("@")[1])
        call_floor = 0 if (call_floor == -1) else call_floor
        if ExterUI_MSG.startswith("call_up"):
            if ele_processors[0].target_floor_up[call_floor] or ele_processors[1].target_floor_up[call_floor]:
                return
            if ele_processors[0].target_floor_down[call_floor]:
                ele_processors[1].target_floor_up[call_floor] = True
                return
            elif ele_processors[1].target_floor_down[call_floor]:
                ele_processors[0].target_floor_up[call_floor] = True
                return
            arrive_time1, arrive_time2 = self.getUpTime(call_floor)
            if arrive_time1 < arrive_time2:
                ele_id = 0
            else:
                ele_id = 1
            ele_processors[ele_id].target_floor_up[call_floor] = True        
        elif ExterUI_MSG.startswith("call_down"):
            if ele_processors[0].target_floor_down[call_floor] or ele_processors[1].target_floor_down[call_floor]:
                return
            if ele_processors[0].target_floor_up[call_floor]:
                ele_processors[1].target_floor_down[call_floor] = True
                return
            elif ele_processors[1].target_floor_up[call_floor]:
                ele_processors[0].target_floor_down[call_floor] = True
                return
            arrive_time1, arrive_time2 = self.getDownTime(call_floor)
            if arrive_time1 < arrive_time2:
                ele_id = 0
            else:
                ele_id = 1
            ele_processors[ele_id].target_floor_down[call_floor] = True
    
    
    def receive_eleProcessor_MSG(self, message):
        #如果电梯有了可以载客的楼层，（接受到arrive信号且电梯状态是door opened）判断上行电梯还是下行电梯去update 对行的request
        ######################
        # 把对应方向的request设置成false,注意对idle的特殊处理
        ######################
        print(f"System Processor received update: {message}")
        '''Deal with f"{moving_direction}_floor_{arrive_floor}_arrived#{self.elevator.ele_id}"'''
        ele_processor = self.elevator_processors
        if message.startswith("up_floor") or message.startswith("down_floor"):
            ele_id = int(message.split("#")[1])
            ele_processor[ele_id - 1].elevator.current_state = ElevatorState.stopped_door_closed
            ele_processor[ele_id - 1].open_door()
        elif message.startswith("floor_"):
            ele_id = int(message.split("#")[1])
            ele_processor[ele_id - 1].elevator.current_state = ElevatorState.stopped_door_closed
            ele_processor[ele_id - 1].open_door()
        for ele_processor in ele_processor:
            if(ele_processor.checkOpen()):
                print(f"System Processor received update: door_opened#{ele_processor.elevator.ele_id}")

    
    def getUpTime(self, floor):
        ele_processors = self.elevator_processors
        return ele_processors[0].compute_callup_time(floor), ele_processors[1].compute_callup_time(floor)
    
    def getDownTime(self, floor):
        ele_processors = self.elevator_processors
        return ele_processors[0].compute_calldown_time(floor), ele_processors[1].compute_calldown_time(floor)
    