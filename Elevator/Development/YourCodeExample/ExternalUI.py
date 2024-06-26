from UIsettings import on, off, circle_button_style, indicator_style_off, circle_button_style_on
from elevator import ElevatorState, DirectionState
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ExternalUI(QWidget):
    def __init__(self, floor, processor):
        super().__init__()
        self.floor = floor
        self.processor = processor
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Floor {self.floor}')
        self.setGeometry(0, 0, 100, 150)
        self.up_button = QPushButton('↑')
        self.down_button = QPushButton('↓')
        self.floor_label = QLabel(f'Floor: {self.floor}')
        self.time_label = QLabel('Time:')
        self.elevator_1_floor_label = QLabel('Elevator1: Floor')
        self.elevator_1_up_indicator = QLabel('↑')
        self.elevator_1_down_indicator = QLabel('↓')
        self.elevator_1_open_indicator = QLabel('>|<')
        self.elevator_2_floor_label = QLabel('Elevator2: Floor')
        self.elevator_2_up_indicator = QLabel('↑')
        self.elevator_2_down_indicator = QLabel('↓')
        self.elevator_2_open_indicator = QLabel('>|<')
        

        # Set floor label alignment
        self.floor_label.setAlignment(Qt.AlignCenter)
        self.time_label.setAlignment(Qt.AlignCenter)

        # Make buttons circular
        self.up_button.setStyleSheet(circle_button_style)
        self.down_button.setStyleSheet(circle_button_style)
                
        # Make indicators circular and set initial color
        self.elevator_1_up_indicator.setStyleSheet(indicator_style_off)
        self.elevator_1_down_indicator.setStyleSheet(indicator_style_off)
        self.elevator_2_up_indicator.setStyleSheet(indicator_style_off)
        self.elevator_2_down_indicator.setStyleSheet(indicator_style_off)

        # Layouts
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()        
        elevator_1_layout = QVBoxLayout()
        elevator_2_layout = QVBoxLayout()
        indicators_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        top_layout.addWidget(self.time_label, alignment=Qt.AlignCenter)

        elevator_1_layout.addWidget(self.elevator_1_floor_label, alignment=Qt.AlignLeft)
        elevator_1_layout.addWidget(self.elevator_1_up_indicator, alignment=Qt.AlignLeft)
        elevator_1_layout.addWidget(self.elevator_1_down_indicator, alignment=Qt.AlignLeft)
        elevator_1_layout.addWidget(self.elevator_1_open_indicator, alignment=Qt.AlignLeft)

        elevator_2_layout.addWidget(self.elevator_2_floor_label, alignment=Qt.AlignRight)
        elevator_2_layout.addWidget(self.elevator_2_up_indicator, alignment=Qt.AlignRight)
        elevator_2_layout.addWidget(self.elevator_2_down_indicator, alignment=Qt.AlignRight)
        elevator_2_layout.addWidget(self.elevator_2_open_indicator, alignment=Qt.AlignRight)

        indicators_layout.addLayout(elevator_1_layout)
        indicators_layout.addLayout(elevator_2_layout)
        
        if self.floor != 3:
            button_layout.addWidget(self.up_button, alignment=Qt.AlignCenter)
        if self.floor != -1:
            button_layout.addWidget(self.down_button, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.floor_label)
        main_layout.addLayout(indicators_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

        self.up_button.clicked.connect(self.push_up_button)
        self.down_button.clicked.connect(self.push_down_button)

        self.timer = self.processor.timer
        self.timer.timeout.connect(self.update)
    
    def closeEvent(self, event):
        system_processor = self.processor
        for elevator in range(2):
            system_processor.elevator_processors[elevator].internal.close()
        for floor in range(4):
            system_processor.externalUIs[floor].close()
        event.accept()
    
    def update(self):
        self.update_time()
        self.update_floor()
        self.update_state()
        self.update_direction()
        self.update_button()
    
    def update_time(self):
        current_time = QDateTime.currentDateTime().toString('hh:mm:ss')
        self.time_label.setText(f'Time: {current_time}')
    
    def update_state(self):
        ele_processors = self.processor.elevator_processors
        if self.checkOpen(ele_processors[0]):
            self.elevator_1_open_indicator.setText("<|>")
            self.elevator_1_open_indicator.setStyleSheet("color:green;")
        else:
            self.elevator_1_open_indicator.setText(">|<")
            self.elevator_1_open_indicator.setStyleSheet("color:black;")

        if self.checkOpen(ele_processors[1]):
            self.elevator_2_open_indicator.setText("<|>")
            self.elevator_2_open_indicator.setStyleSheet("color:green;")
        else:
            self.elevator_2_open_indicator.setText(">|<")
            self.elevator_2_open_indicator.setStyleSheet("color:black;")
    
    def update_floor(self):
        ele_processors = self.processor.elevator_processors
        self.elevator_1_floor_label.setText(f'Floor {ele_processors[0].elevator.current_floor}')
        self.elevator_2_floor_label.setText(f'Floor {ele_processors[1].elevator.current_floor}')
    
    def update_direction(self):
        ele_processors = self.processor.elevator_processors
        direction1 = ele_processors[0].elevator.direction
        if direction1 == DirectionState.up:
            self.elevator_1_up_indicator.setStyleSheet(on)
            self.elevator_1_down_indicator.setStyleSheet(off)
        elif direction1 == DirectionState.down:
            self.elevator_1_up_indicator.setStyleSheet(off)
            self.elevator_1_down_indicator.setStyleSheet(on)
        elif direction1 == DirectionState.idle:
            self.elevator_1_up_indicator.setStyleSheet(off)
            self.elevator_1_down_indicator.setStyleSheet(off)

        direction2 = ele_processors[1].elevator.direction
        if direction2 == DirectionState.up:
            self.elevator_2_up_indicator.setStyleSheet(on)
            self.elevator_2_down_indicator.setStyleSheet(off)
        elif direction2 == DirectionState.down:
            self.elevator_2_up_indicator.setStyleSheet(off)
            self.elevator_2_down_indicator.setStyleSheet(on)
        elif direction2 == DirectionState.idle:
            self.elevator_2_up_indicator.setStyleSheet(off)
            self.elevator_2_down_indicator.setStyleSheet(off)
    
    def update_button(self):
        if self.checkTargetUp(self.floor):
            self.up_button.setStyleSheet(circle_button_style_on)
        else:
            self.up_button.setStyleSheet(circle_button_style)
        
        if self.checkTargetDown(self.floor):
            self.down_button.setStyleSheet(circle_button_style_on)
        else:
            self.down_button.setStyleSheet(circle_button_style)

    def push_up_button(self):
        self.processor.process_ExternalUI_requests(f"call_up@{self.floor}")
        self.up_button.setStyleSheet(circle_button_style_on)

    def push_down_button(self):
        self.processor.process_ExternalUI_requests(f"call_down@{self.floor}")
        self.down_button.setStyleSheet(circle_button_style_on)

    def checkOpen(self, processor):
        state = processor.elevator.current_state
        door_open = state == ElevatorState.stopped_door_opened or state == ElevatorState.stopped_opening_door
        same_floor = processor.elevator.current_floor == self.floor
        return door_open and same_floor
    
    def checkTargetUp(self, floor):
        floor = 0 if (floor == -1) else floor
        ele_processors = self.processor.elevator_processors
        return ele_processors[0].target_floor_up[floor] or ele_processors[1].target_floor_up[floor]
    
    def checkTargetDown(self, floor):
        floor = 0 if (floor == -1) else floor
        ele_processors = self.processor.elevator_processors
        return ele_processors[0].target_floor_down[floor] or ele_processors[1].target_floor_down[floor]
