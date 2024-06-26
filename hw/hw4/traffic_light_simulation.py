import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,QMessageBox,QLineEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIntValidator

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Control Panel')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()

        self.red_label = QLabel('Red Light Duration (seconds):', self)
        self.red_duration = QLineEdit(self.red_label)
        self.red_duration.setValidator(QIntValidator(1, 999))
        layout.addWidget(self.red_label)
        layout.addWidget(self.red_duration)

        self.yellow_label = QLabel('Yellow Light Duration (seconds):', self)
        self.yellow_duration = QLineEdit(self.yellow_label)
        self.yellow_duration.setValidator(QIntValidator(1, 999))
        layout.addWidget(self.yellow_label)
        layout.addWidget(self.yellow_duration)
        
        self.green_label = QLabel('Green Light Duration (seconds):', self)
        self.green_duration = QLineEdit(self.green_label)
        self.green_duration.setValidator(QIntValidator(1, 999))
        layout.addWidget(self.green_label)
        layout.addWidget(self.green_duration)
        
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_simulation)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)
        
        self.setLayout(layout)
        
    def start_simulation(self):
        red_time = int(self.red_duration.text())
        yellow_time = int(self.yellow_duration.text())
        green_time = int(self.green_duration.text())

        if yellow_time > red_time or yellow_time > green_time:
            QMessageBox.warning(self, 'Invalid Duration', 'Yellow duration must not exceed Red or Green duration.')
            return
        
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # 禁用持续时间微调器
        self.red_duration.setEnabled(False)
        self.yellow_duration.setEnabled(False)
        self.green_duration.setEnabled(False)
        
        self.traffic_light_window = TrafficLightDisplay(red_time, yellow_time, green_time)
        self.traffic_light_window.show()
        
    def stop_simulation(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # 启用持续时间微调器
        self.red_duration.setEnabled(True)
        self.yellow_duration.setEnabled(True)
        self.green_duration.setEnabled(True)
        
        if hasattr(self, 'traffic_light_window'):
            self.traffic_light_window.enter_flashing_mode()

class TrafficLightDisplay(QWidget):
    def __init__(self, red_time, yellow_time, green_time):
        super().__init__()
        self.red_time = red_time
        self.yellow_time = yellow_time
        self.green_time = green_time
        self.current_light = 'red'
        self.time_left = red_time
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Traffic Light')
        self.setGeometry(500, 100, 200, 400)
        
        self.layout = QVBoxLayout()
        
        self.red_light = QLabel('', self)
        self.red_light.setStyleSheet('background-color: red')
        self.red_light.setFixedSize(100, 100)
        self.layout.addWidget(self.red_light, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.yellow_light = QLabel('', self)
        self.yellow_light.setStyleSheet('background-color: black')
        self.yellow_light.setFixedSize(100, 100)
        self.layout.addWidget(self.yellow_light, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.green_light = QLabel('', self)
        self.green_light.setStyleSheet('background-color: black')
        self.green_light.setFixedSize(100, 100)
        self.layout.addWidget(self.green_light, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.timer_label = QLabel('', self)
        self.layout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(self.layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        
        self.update_display()
        
    def update_timer(self):
        self.time_left -= 1
        if self.time_left == 0:
            if self.current_light == 'red':
                self.current_light = 'green'
                self.time_left = self.green_time
            elif self.current_light == 'green':
                self.current_light = 'yellow'
                self.time_left = self.yellow_time
            elif self.current_light == 'yellow':
                self.current_light = 'red'
                self.time_left = self.red_time
        
        self.update_display()
        
    def update_display(self):
        if self.current_light == 'red':
            self.red_light.setStyleSheet('background-color: red')
            self.yellow_light.setStyleSheet('background-color: black')
            self.green_light.setStyleSheet('background-color: black')
        elif self.current_light == 'yellow':
            self.red_light.setStyleSheet('background-color: black')
            self.yellow_light.setStyleSheet('background-color: yellow')
            self.green_light.setStyleSheet('background-color: black')
        elif self.current_light == 'green':
            self.red_light.setStyleSheet('background-color: black')
            self.yellow_light.setStyleSheet('background-color: black')
            self.green_light.setStyleSheet('background-color: green')
            
        self.timer_label.setText(f'Time left: {self.time_left} seconds')
        
    def enter_flashing_mode(self):
        self.timer.stop()
        self.timer_label.setText('')
        self.current_light = 'flashing'
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self.flash_yellow)
        self.flash_timer.start(500)
        
    def flash_yellow(self):
        self.red_light.setStyleSheet('background-color: black')
        self.green_light.setStyleSheet('background-color: black')
        if self.yellow_light.styleSheet() == 'background-color: yellow':
            self.yellow_light.setStyleSheet('background-color: black')
        else:
            self.yellow_light.setStyleSheet('background-color: yellow')

def main():
    app = QApplication(sys.argv)
    control_panel = ControlPanel()
    control_panel.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
