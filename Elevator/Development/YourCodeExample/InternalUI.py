from UIsettings import on, off, circle_button_style, indicator_style_off, circle_button_style_on
from elevator import DirectionState
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class InternalUI(QWidget):
    def __init__(self, processor):
        super().__init__()
        self.processor = processor
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(f'Elevator {self.processor.elevator.ele_id}')
        self.setGeometry(0, 0, 400, 500)
        self.elevator_id_label = QLabel(f'ID: {self.processor.elevator.ele_id}')
        self.floor_label = QLabel('Floor:')
        self.time_label = QLabel('Time:')
        self.direction_label_up = QLabel('↑')
        self.direction_label_down = QLabel('↓')
        self.floor_button_3 = QPushButton('3')
        self.floor_button_2 = QPushButton('2')
        self.floor_button_1 = QPushButton('1')
        self.floor_button_b = QPushButton('-1')
        self.open_door_button = QPushButton('<>')
        self.close_door_button = QPushButton('><')
        self.open_close_state = QLabel('>|<')

        self.floor_button_b.setStyleSheet(circle_button_style)
        self.floor_button_1.setStyleSheet(circle_button_style)
        self.floor_button_2.setStyleSheet(circle_button_style)
        self.floor_button_3.setStyleSheet(circle_button_style)
        self.close_door_button.setStyleSheet(circle_button_style)
        self.open_door_button.setStyleSheet(circle_button_style)
        
        self.direction_label_up.setStyleSheet(indicator_style_off)
        self.direction_label_down.setStyleSheet(indicator_style_off)

        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        button_layout = QGridLayout()
        indicator_layout = QHBoxLayout()

        top_layout.addWidget(self.elevator_id_label, alignment=Qt.AlignLeft)
        top_layout.addStretch()
        top_layout.addWidget(self.time_label, alignment=Qt.AlignRight)
        
        indicator_layout.addWidget(self.direction_label_up)
        indicator_layout.addWidget(self.direction_label_down)
        
        button_layout.addWidget(self.floor_button_3, 1, 0, 1, 2, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.floor_button_2, 2, 0, 1, 2, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.floor_button_1, 3, 0, 1, 2, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.floor_button_b, 4, 0, 1, 2, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.open_door_button, 5, 0)
        button_layout.addWidget(self.close_door_button, 5, 1)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.open_close_state, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.floor_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(indicator_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.open_door_button.clicked.connect(self.push_open_door_button)
        self.close_door_button.clicked.connect(self.push_close_door_button)
        self.floor_button_b.clicked.connect(self.push_floor_button_b)
        self.floor_button_1.clicked.connect(self.push_floor_button_1)
        self.floor_button_2.clicked.connect(self.push_floor_button_2)
        self.floor_button_3.clicked.connect(self.push_floor_button_3)

        self.timer = self.processor.system_processor.timer
        self.timer.timeout.connect(self.update)
    
    def closeEvent(self, event):
        system_processor = self.processor.system_processor
        for elevator in range(2):
            system_processor.elevator_processors[elevator].internal.close()
        for floor in range(4):
            system_processor.externalUIs[floor].close()
        event.accept()
    
    def update(self):
        self.update_time()
        self.update_state()
        self.update_floor()
        self.update_direction()
        self.update_floor_button()
    
    def update_time(self):
        current_time = QDateTime.currentDateTime().toString('hh:mm:ss')
        self.time_label.setText(f"Time: {current_time}")
        
    def update_state(self):
        if self.processor.checkOpen():
            self.open_close_state.setText("<|>")
            self.open_close_state.setStyleSheet("color:green;")
        else:
            self.open_close_state.setText(">|<")
            self.open_close_state.setStyleSheet("color:black;")
            
    def update_floor(self):
        self.floor_label.setText(f"Floor: {self.processor.elevator.current_floor}")
    
    def update_floor_button(self):
        if self.processor.target_floor[0]:
            self.floor_button_b.setStyleSheet(circle_button_style_on)
        else:
            self.floor_button_b.setStyleSheet(circle_button_style)

        if self.processor.target_floor[1]:
            self.floor_button_1.setStyleSheet(circle_button_style_on)
        else:
            self.floor_button_1.setStyleSheet(circle_button_style)

        if self.processor.target_floor[2]:
            self.floor_button_2.setStyleSheet(circle_button_style_on)
        else:
            self.floor_button_2.setStyleSheet(circle_button_style)
        
        if self.processor.target_floor[3]:
            self.floor_button_3.setStyleSheet(circle_button_style_on)
        else:
            self.floor_button_3.setStyleSheet(circle_button_style)
    
    def update_direction(self):
        direction = self.processor.elevator.direction
        if direction == DirectionState.up:
            self.direction_label_up.setStyleSheet(on)
            self.direction_label_down.setStyleSheet(off)
        elif direction == DirectionState.down:
            self.direction_label_up.setStyleSheet(off)
            self.direction_label_down.setStyleSheet(on)
        elif direction == DirectionState.idle:
            self.direction_label_up.setStyleSheet(off)
            self.direction_label_down.setStyleSheet(off)

    def push_open_door_button(self):
        self.processor.process_InternalUI_requests("open_door")

    def push_close_door_button(self):
        self.processor.process_InternalUI_requests("close_door")
    
    def push_floor_button_b(self):
        self.processor.process_InternalUI_requests(f"select_floor@-1#{self.processor.elevator.ele_id}")
        self.floor_button_b.setStyleSheet(circle_button_style_on)

    def push_floor_button_1(self):
        self.processor.process_InternalUI_requests(f"select_floor@1#{self.processor.elevator.ele_id}")
        self.floor_button_1.setStyleSheet(circle_button_style_on)

    def push_floor_button_2(self):
        self.processor.process_InternalUI_requests(f"select_floor@2#{self.processor.elevator.ele_id}")
        self.floor_button_2.setStyleSheet(circle_button_style_on)

    def push_floor_button_3(self):
        self.processor.process_InternalUI_requests(f"select_floor@3#{self.processor.elevator.ele_id}")
        self.floor_button_3.setStyleSheet(circle_button_style_on)
