from PyQt5.QtWidgets import *

class Inject(QWidget):
    def __init__(self, mainboard):
        super().__init__()
        self.mainboard = mainboard
        self.initUI()
    
    def initUI(self):
        self.setGeometry(100, 750, 400, 400)
        self.setWindowTitle('Patient UI')

        self.inject_button = QPushButton("Inject", self)
        self.inject_button.setStyleSheet("background-color: #FF8888;")
        self.inject_button.clicked.connect(self.requestInject)
        self.inject_button.setGeometry(100, 100, 200, 200)
    
    def closeEvent(self, event):
        self.getMainboard().close()
        self.getMainboard().speed_slider.close()
        event.accept()
    
    def requestInject(self):
        processor = self.getProcessor()
        time = self.getCurrentTime()
        processor.inject_request(time)

    def getMainboard(self):
        return self.mainboard

    def getProcessor(self):
        return self.getMainboard().getProcessor()

    def getCurrentTime(self):
        return self.getMainboard().current_time
    
    def getBolus(self):
        return self.getMainboard().getBolus()
    
    def setLastTime(self, time):
        self.getMainboard().last_time = time
