from setting import SettingPage
from history import HistoryPage
from checkPIN import CheckPINPage
from resetPIN import ResetPINPage
from timeslider import TimeSlider
from inject import Inject
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

indicator_style_off = """
QLabel {
    background-color: grey;
    border-radius: 15px;
    padding: 1px;
    color: white;
    min-width: 30px;
    min-height: 30px;
    max-width: 30px;
    max-height: 30px;
}
"""
indicator_style_on = """
QLabel {
    background-color: green;
    border-radius: 15px;
    padding: 1px;
    color: white;
    min-width: 30px;
    min-height: 30px;
    max-width: 30px;
    max-height: 30px;
}
"""

class Mainboard(QMainWindow):
    '''
    This is a class for Injection Processor.

    InjectProcessor class contains a database, 
    and all the functions need to interact with database.

    Attributes:
        processor:   A InjectProcessor class to process all the functions.
    '''

    time_updated = pyqtSignal(QDateTime)

    def __init__(self, processor):
        super().__init__()
        self.processor = processor
        self.initUI()
    

    '''The functions below are used to control the interfaces.'''

    def initUI(self):
        self.setGeometry(100, 100, 1200, 500)
        self.setWindowTitle('Injection Processor')

        self.setting_button = QPushButton("Settings", self)
        self.setting_button.clicked.connect(self.setSettings)
        self.setting_button.setGeometry(800, 350, 150, 50)

        self.status_button = QPushButton("On / Off", self)
        self.status_button.clicked.connect(self.setStatus)
        self.status_button.setGeometry(625, 250, 150, 50)

        self.status_light = QLabel(self)
        self.status_light.setGeometry(QRect(825, 265, 40, 40))
        self.status_light.setStyleSheet(indicator_style_on)

        self.bolus_label = QLabel(self)
        self.bolus_label.setText("Bolus")
        self.bolus_label.setStyleSheet("font-size: 36px;")
        self.bolus_label.setGeometry(15, 60, 300, 50)

        self.bolus_value = QLabel(self)
        self.bolus_value.setStyleSheet("font-size: 36px;")
        self.bolus_value.setGeometry(50, 110, 300, 50)

        self.last_time = None
        self.last_time_label = QLabel(self)
        self.last_time_label.setGeometry(30, 160, 1000, 50)

        self.baseline_label = QLabel(self)
        self.baseline_label.setText("Baseline speed")
        self.baseline_label.setStyleSheet("font-size: 36px;")
        self.baseline_label.setGeometry(15, 210, 300, 50)

        self.baseline_value = QLabel(self)
        self.baseline_value.setStyleSheet("font-size: 36px;")
        self.baseline_value.setGeometry(50, 260, 300, 50)

        self.painkiller_label = QLabel(self)
        self.painkiller_label.setText("Painkiller left")
        self.painkiller_label.setStyleSheet("font-size: 36px;")
        self.painkiller_label.setGeometry(15, 310, 300, 50)

        self.painkiller_value = QLabel(self)
        self.painkiller_value.setStyleSheet("font-size: 36px;")
        self.painkiller_value.setGeometry(50, 360, 300, 50)

        self.painkiller_remind = QLabel(self)
        self.painkiller_remind.setStyleSheet("color: red;")
        self.painkiller_remind.setGeometry(QRect(30, 400, 500, 50))

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.addPainkiller)
        self.add_button.setGeometry(450, 350, 150, 50)

        self.history_button = QPushButton("History", self)
        self.history_button.clicked.connect(self.query)
        self.history_button.setGeometry(625, 350, 150, 50)

        self.reset_button = QPushButton("Reset PIN", self)
        self.reset_button.clicked.connect(self.resetPIN)
        self.reset_button.setGeometry(450, 250, 150, 50)

        self.bolus_hour_label = QLabel(self)
        self.bolus_hour_label.setStyleSheet("font-size: 36px;")
        self.bolus_hour_label.setGeometry(450, 110, 1000, 50)

        self.bolus_day_label = QLabel(self)
        self.bolus_day_label.setStyleSheet("font-size: 36px;")
        self.bolus_day_label.setGeometry(450, 160, 1000, 50)

        self.speed_slider = TimeSlider(self)

        self.patient_button = Inject(self)

        self.setting_button.setEnabled(True)
        self.status_button.setEnabled(True)

        self.time_label = QLabel(self)
        self.time_label.setStyleSheet("font-size: 36px;")
        self.time_label.setGeometry(450, 60, 1000, 50)

        
        self.current_time = QDateTime.currentDateTime()
        self.initial_time = self.current_time
        self.getProcessor().database.status = True
        self.updateBaselineHistory(self.current_time, self.getBaseline())

        self.timer_interval = 1000
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(self.timer_interval)
    
    def run(self):
        self.move(100, 100)
        self.show()
        self.speed_slider.show()
        self.patient_button.show()

    def paintEvent(self, event):
        '''Draw the grids to separate different parts.'''
        bolus_painter = QPainter(self)
        bolus_painter.setPen(QColor(128, 128, 128))
        bolus_painter.drawRect(5, 65, 420, 140)

        baseline_painter = QPainter(self)
        baseline_painter.setPen(QColor(128, 128, 128))
        baseline_painter.drawRect(5, 210, 420, 95)

        remain_painter = QPainter(self)
        remain_painter.setPen(QColor(128, 128, 128))
        remain_painter.drawRect(5, 310, 420, 140)
    
    def closeEvent(self, event):
        self.speed_slider.close()
        self.patient_button.close()
        event.accept()

    def getSpeedSlider(self):
        return self.speed_slider.speed_slider

    def txtcaseSend(self):
        while (True):
            if len(self.getProcessor().txtcases_list):
                if self.getProcessor().txtcaseProcess_input(self.getProcessor().txtcases_list[0]):
                    self.getProcessor().txtcases_list.pop(0)
                else:
                    return
            else:
                return
    
    def update_time(self):
        '''Update the interfaces as time flowing.'''
        sec = self.getSpeedSlider().value()
        self.current_time = self.current_time.addSecs(sec)
        self.time_updated.emit(self.current_time)
        hist = self.getBaselineHistory()
        baseline = hist.get(list(hist.keys())[-1]) * sec / 60
        
        self.txtcaseSend()

        if self.getStatus():
            self.status_light.setStyleSheet(indicator_style_on)
            if self.checkInject(self.current_time, baseline):
                self.getProcessor().updateRemain(baseline)
                self.updateBaselineHistory(self.current_time, self.getBaseline())
            else:
                self.updateBaselineHistory(self.current_time.addSecs(-sec), 0)
        else:
            self.status_light.setStyleSheet(indicator_style_off)
        
        self.bolus_value.setText('%.2f'%(self.getBolus()) + " mL")
        self.baseline_value.setText('%.2f'%(self.getBaseline()) + " mL/min")
        self.painkiller_value.setText('%.2f'%(self.getRemain()) + " mL")
        
        self.bolus_hour_label.setText("Last 1 Hour\t" 
                                      + '%.2f'%(self.getHour(self.current_time))
                                      + " / " + '%.2f'%(self.getLimitHour()) + " mL")
        
        self.bolus_day_label.setText("Last 1 Day\t" 
                                     + '%.2f'%(self.getDay(self.current_time))
                                     + " / " + '%.2f'%(self.getLimitDay()) + " mL")

        
        if self.getRemain() <= 1:
            self.painkiller_remind.setText("Running out, please add painkiller!")
        else:
            self.painkiller_remind.setText("")

        if self.last_time:
            self.last_time_label.setText("Last injection: " 
                                         + self.last_time.toString('yyyy-MM-dd HH:mm:ss'))
        else:
            self.last_time_label.setText("Last injection: No injection yet!")
        self.time_label.setText("Current time: " 
                                + self.current_time.toString('yyyy-MM-dd HH:mm:ss'))

    def on_operations_start(self):
        '''Disable the buttons when operating with sub-windows.'''
        self.setting_button.setEnabled(False)
        self.status_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.history_button.setEnabled(False)

    def on_operations_finished(self):
        '''Enable the button when the operation in sub-window finished.'''
        self.setting_button.setEnabled(True)
        self.status_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.history_button.setEnabled(True)


    '''The functions below are used to interact with the user.'''

    def setSettings(self):
        '''Call the settings page to set the parameters if the inject processor.'''
        self.on_operations_start()
        self.setting_page = SettingPage(self.getProcessor())
        self.setting_page.show()
        self.setting_page.finished.connect(self.on_operations_finished)
    
    def setStatus(self):
        '''Set baseline on/off.'''
        if self.checkPIN():
            self.on_operations_start()
            self.getProcessor().setStatus(self.current_time)
        self.on_operations_finished()

    def query(self):
        '''Query for the operation history.'''
        self.on_operations_start()
        self.history_page = HistoryPage(self.getEventHistory())
        self.history_page.show()
        self.history_page.finished.connect(self.on_operations_finished)
    
    def checkPIN(self):
        '''Call out the checkPIN page to ensure security.'''
        self.check_page = CheckPINPage(self.getProcessor())
        result = self.check_page.exec_()
        return result == QDialog.Accepted
    
    def resetPIN(self):
        '''Call out the resetPIN page.'''
        if self.checkPIN():
            self.on_operations_start()
            self.reset_page = ResetPINPage(self.getProcessor())
            self.reset_page.show()
            self.reset_page.finished.connect(self.on_operations_finished)


    '''The functions below are used to interact with the processor.'''

    def getProcessor(self):
        return self.processor

    def addPainkiller(self):
        self.getProcessor().addPainkiller()
    
    def inject(self):
        self.getProcessor().inject()
    
    def updateBolusHistory(self, time):
        self.getProcessor().addBolusHistory(time)
    
    def updateBaselineHistory(self, time, baseline):
        self.getProcessor().addBaselineHistory(time, baseline)

    def updateEventHistory(self, time, event):
        self.getProcessor().addEventHistory(time, event)
    
    def checkInject(self, time, amount):
        return self.getProcessor().checkInject(time, amount)
    
    def getBolus(self):
        return self.getProcessor().getBolus()

    def getBaseline(self):
        return self.getProcessor().getBaseline()
    
    def getLimitHour(self):
        return self.getProcessor().getLimitHour()
    
    def getLimitDay(self):
        return self.getProcessor().getLimitDay()
    
    def getHour(self, time):
        return self.getProcessor().getHour(time)
    
    def getDay(self, time):
        return self.getProcessor().getDay(time)
    
    def getStatus(self):
        return self.getProcessor().getStatus()
    
    def getRemain(self):
        return self.getProcessor().getRemain()
    
    def getEventHistory(self):
        return self.getProcessor().getEventHistory()
    
    def getBaselineHistory(self):
        return self.getProcessor().getBaselineHistory()
