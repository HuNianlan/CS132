# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *

# class TimeSlider(QWidget):
#     def __init__(self, mainboard):
#         super().__init__()
#         self.mainboard = mainboard
#         self.initUI()
    
#     def initUI(self):
#         self.setGeometry(1500, 150, 400, 500)
#         self.setWindowTitle('Time Slider')

#         layout = QHBoxLayout(self)

#         # Vertical layout for slider and labels
#         slider_layout = QVBoxLayout()

#         self.speed_slider = QSlider(Qt.Vertical, self)
#         self.speed_slider.setMinimum(0)
#         self.speed_slider.setMaximum(240)
#         self.speed_slider.setValue(120)
#         self.speed_slider.setTickPosition(QSlider.TicksRight)
#         self.speed_slider.setTickInterval(40)
#         self.speed_slider.setGeometry(100, 50, 50, 400)

#         slider_layout.addWidget(self.speed_slider)

#         # Vertical layout for number labels
#         labels_layout = QVBoxLayout()

#         # Add labels for slider values
#         self.labels = []
#         for i in range(self.speed_slider.minimum(), self.speed_slider.maximum() + 1, self.speed_slider.tickInterval()):
#             label = QLabel(str(240 - i), self)
#             label.setAlignment(Qt.AlignCenter)
#             self.labels.append(label)
#             labels_layout.addWidget(label)

#         layout.addLayout(labels_layout)
#         layout.addLayout(slider_layout)

#         # self.fast_label = QLabel("Fast", self)
#         # self.fast_label.setGeometry(150, 50, 100, 50)
#         # self.fast_label.setStyleSheet("font-size: 36px;")

#         # self.slow_label = QLabel("Slow", self)
#         # self.slow_label.setGeometry(150, 400, 100, 50)
#         # self.slow_label.setStyleSheet("font-size: 36px;")

#         # layout.addWidget(self.fast_label)
#         # layout.addWidget(self.slow_label)
    
#     def closeEvent(self, event):
#         self.mainboard.close()
#         self.mainboard.patient_button.close()
#         event.accept()



from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TimeSlider(QWidget):
    def __init__(self, mainboard):
        super().__init__()
        self.mainboard = mainboard
        self.initUI()
    
    def initUI(self):
        self.setGeometry(1500, 150, 400, 500)
        self.setWindowTitle('Time Slider')

        self.speed_slider = QSlider(Qt.Vertical, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(3600)
        self.speed_slider.setValue(120)
        self.speed_slider.setTickPosition(QSlider.TicksRight)
        self.speed_slider.setTickInterval(120)
        self.speed_slider.setGeometry(100, 50, 20, 400)

        self.fast_label = QLabel("1 h/s", self)
        self.fast_label.setGeometry(150, 30, 200, 50)
        self.fast_label.setStyleSheet("font-size: 36px;")

        self.center_label = QLabel("30 min/s", self)
        self.center_label.setGeometry(150, 220, 200, 50)
        self.center_label.setStyleSheet("font-size: 36px;")

        self.slow_label = QLabel("0 min/s", self)
        self.slow_label.setGeometry(150, 410, 200, 50)
        self.slow_label.setStyleSheet("font-size: 36px;")
    
    def closeEvent(self, event):
        self.mainboard.close()
        self.mainboard.patient_button.close()
        event.accept()
