from checkPIN import CheckPINPage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SettingPage(QDialog):
    '''
    This is a class for setting page.

    SettingPage class create a window to set the parameters of the processor,
    check whether the parameters are valid and save them in the database, that is to update.

    Attributes:
        processor:      A InjectProcessor class to process all the functions.
        time_counter:   An int of the remaining time to set the parameters.
    '''

    def __init__(self, processor):
        super().__init__()
        self.processor = processor
        self.time_counter = 60
        self.initUI()
    
    def initUI(self):
        self.setGeometry(200, 200, 580, 350)
        self.setWindowTitle('Settings')

        self.time_label = QLabel(self)
        self.time_label.setGeometry(350, 10, 250, 50)
        self.time_label.setText("Countdown: " + str(self.time_counter) + "s")

        processor = self.getProcessor()
        self.setting_value = {
            "Baseline (mL/min)": [processor.getBaseline(), 0.01, 0.1],
            "Bolus (mL/shot)": [processor.getBolus(), 0.2, 0.5],
            "Limit per hour (mL)": [processor.getLimitHour(), 0.0, 1.0],
            "Limit per day (mL)": [processor.getLimitDay(), 0.0, 3.0]
        }

        index = 0
        self.line_edits = {}
        for tag, value in self.setting_value.items():
            y_start = 60 + 50 * index
            self.label = QLabel(tag, self)
            self.label.setGeometry(10, y_start, 250, 50)
            self.line_edit = QLineEdit(self)
            self.line_edit.setGeometry(300, y_start, 100, 50)
            self.line_edit.setText('%.2f'%(value[0]))
            self.interval = QLabel("[" + '%.2f'%(value[1]) + ", " + '%.2f'%(value[2]) + "]", self)
            self.interval.setGeometry(410, y_start, 250, 50)

            validator = QDoubleValidator(self.setting_value[tag][1], 
                                            self.setting_value[tag][2], 2, self.line_edit)
            validator.setNotation(QDoubleValidator.StandardNotation)
            
            self.line_edit.setValidator(validator)
            self.line_edits[tag] = self.line_edit
            index = index + 1

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.button(QDialogButtonBox.Ok).setText("Confirm")
        self.button_box.accepted.connect(self.updateDatabase)
        self.button_box.rejected.connect(self.reject)
        self.button_box.setGeometry(10, 280, 400, 50)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    def update_time(self):
        '''Update the interfaces as time flowing.'''
        self.time_counter = self.time_counter - 1
        self.time_label.setText("Countdown: " + str(self.time_counter) + "s")
        if self.time_counter == 0:
            self.reject()
        
    def updateDatabase(self):
        for tag, line_edit in self.line_edits.items():
            if not line_edit.hasAcceptableInput():
                # Show an error message or handle invalid input as needed
                QMessageBox.warning(self, "Invalid Parameter", f"Invalid input for {tag}!")
                self.time_counter = 61
                self.update_time()
                return
            
        if self.checkPIN():
            new_baseline = float(self.line_edits["Baseline (mL/min)"].text())
            new_bolus = float(self.line_edits["Bolus (mL/shot)"].text())
            new_limit_hour = float(self.line_edits["Limit per hour (mL)"].text())
            new_limit_day = float(self.line_edits["Limit per day (mL)"].text())

            processor = self.getProcessor()
            processor.setBaseline(new_baseline, self.getProcessor().getTime())
            processor.setBolus(new_bolus)
            processor.setLimitHour(new_limit_hour)
            processor.setLimitDay(new_limit_day)

            self.accept()
        else:
            self.reject()

    def getProcessor(self):
        return self.processor
    
    def checkPIN(self):
        '''Call out the checkPIN page to ensure security.'''
        self.check_page = CheckPINPage(self.getProcessor())
        result = self.check_page.exec_()
        return result == QDialog.Accepted
