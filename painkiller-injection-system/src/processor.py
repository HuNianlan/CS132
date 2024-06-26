from database import InjectDatabase
from mainborad import Mainboard
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class InjectProcessor():
    '''
    This is a class for Injection Processor.

    InjectProcessor class contains a database, 
    and all the functions need to interact with database.

    Attributes:
        database:       A Database class to store corresponding information.
        mainboard:      A Mainboard class to create and control the UI interface.
    '''

    def __init__(self):
        super().__init__()
        self.database = InjectDatabase()
        self.txtcases_list = []
        self.mainboard = Mainboard(self)
        
    
    def run(self):
        self.mainboard.run()
    
    def getDatabase(self):
        return self.database
    
    def getMainboard(self):
        return self.mainboard
    
    def getTime(self):
        return self.mainboard.current_time

    '''The functions below are used to calculate and check.'''

    def txtcasesUpload(self, cases):
        self.txtcases_list = cases

    def txtcaseProcess_input(self, case):
        if case == "test_finish":
            sys.exit()
        if case.startswith("set_baseline@"):
            print("Server: " + case)
            self.setBaseline(float(case.split("@")[1].split("m")[0]), self.getTime())
            return True
        elif case.startswith("set_bolus@"):
            print("Server: " + case)
            self.setBolus(float(case.split("@")[1].split("m")[0]))
            return True
        elif case == "baseline_on":
            print("Server: " + case)
            self.setStatusOn(self.getTime())
            return True
        elif case == "baseline_off":
            print("Server: " + case)
            self.setStatusOff(self.getTime())
            return True
        elif case.endswith("request_bolus"):
            minutes = int(case.split("min")[0])
            target_time = self.mainboard.initial_time.addSecs(minutes * 60)
            if (self.getTime().secsTo(target_time) <= 0):
                print("Server: " + case)
                time = self.getTime()
                self.inject_request(time)
                return True
        return False
    
    def checkInject(self, time, amount):
        '''Check the injection request and give corresponding message.'''
        if not self.getRemain() >= amount:
            return False
        if not self.checkHour(time, amount):
            return False
        if not self.checkDay(time, amount):
            return False
        return True

    def checkDay(self, time, amount):
        '''Check whether exceeding the day limit.'''
        return self.getDay(time) + amount <= self.getLimitDay()
    
    def checkHour(self, time, amount):
        '''Check whether exceeding the hour limit.'''
        return self.getHour(time) + amount <= self.getLimitHour()
    
    def checkPIN(self, Pin):
        return Pin ==  self.getPIN()
    
    def inject_request(self, time):
        minutes = int(self.mainboard.initial_time.secsTo(time) / 60)
        if self.checkInject(time, self.getBolus()):
            self.mainboard.last_time = time
            self.inject()
            self.addBolusHistory(time)
            self.addEventHistory(time, "Inject " 
                        + '%.2f'%(self.getBolus()) + " mL painkiller.")
            print(f"Processor: inject@{minutes}min\n")
        else:
            print(f"Processor: no_injection@{minutes}min\n")
        return True
    

    '''The functions below are used to load & update information of the databse.'''
    
    def inject(self):
        self.getDatabase().inject()
    
    def addPainkiller(self):
        self.getDatabase().addPainkiller()
    
    def addBolusHistory(self, time):
        self.getDatabase().addBolusHistory(time)
    
    def addBaselineHistory(self, time, baseline):
        self.getDatabase().addBaselineHistory(time, baseline)
    
    def addEventHistory(self, time, event):
        self.getDatabase().addEventHistory(time, event)
    
    def updateRemain(self, amount):
        self.getDatabase().updateRemain(amount)
    
    def resetPIN(self, Pin):
        self.getDatabase().resetPIN(Pin)
    
    def getPIN(self):
        return self.getDatabase().getPin()
    
    def getBolus(self):
        return self.getDatabase().getBolus()

    def getBaseline(self):
        return self.getDatabase().getBaseline()
    
    def getLimitHour(self):
        return self.getDatabase().getLimitHour()
    
    def getLimitDay(self):
        return self.getDatabase().getLimitDay()
    
    def getHour(self, time):
        return self.getDatabase().getHourBolus(time) + self.getDatabase().getHourBaseline(time)
    
    def getDay(self, time):
        return self.getDatabase().getDayBolus(time) + self.getDatabase().getDayBaseline(time)
    
    def getStatus(self):
        return self.getDatabase().getStatus()
    
    def getRemain(self):
        return self.getDatabase().getRemain()
    
    def getEventHistory(self):
        return self.getDatabase().getEventHistory()
    
    def getBaselineHistory(self):
        return self.getDatabase().getBaselineHistory()
    
    def setStatus(self, time):
        self.getDatabase().setStatus()
        if self.getStatus():
            print("Processor: baseline_on_set\n")
            self.addEventHistory(time, "Baseline on at speed of " 
                            + '%.2f'%(self.getBaseline()) + " mL/min.")
            self.addBaselineHistory(time, self.getBaseline())
        else:
            print("Processor: baseline_off_set\n")
            self.addEventHistory(time, "Baseline off.")
            self.addBaselineHistory(time, 0)
    
    def setStatusOn(self, time):
        self.getDatabase().status = True
        print("Processor: baseline_on_set\n")
        self.addEventHistory(time, "Baseline on at speed of " 
                            + '%.2f'%(self.getBaseline()) + " mL/min.")
        self.addBaselineHistory(time, self.getBaseline())
    
    def setStatusOff(self, time):
        self.getDatabase().status = False
        print("Processor: baseline_off_set\n")
        self.addEventHistory(time, "Baseline off.")
        self.addBaselineHistory(time, 0)
    
    def setBaseline(self, baseline, time):
        print(f"Processor: baseline_set@{baseline}ml/min\n")
        self.getDatabase().setBaseline(baseline)
        if self.getStatus():
            self.addBaselineHistory(time, baseline)
        self.addEventHistory(time, "Set baseline at " 
                        + '%.2f'%(baseline) + " mL/min.")
    
    def setBolus(self, bolus):
        print(f"Processor: bolus_set@{bolus}ml/shot\n")
        self.getDatabase().setBolus(bolus)
        self.addEventHistory(self.getTime(), "Set bolus at " 
                        + '%.2f'%(bolus) + " mL/shot.")
    
    def setLimitHour(self, limit_hour):
        self.getDatabase().setLimitHour(limit_hour)
    
    def setLimitDay(self, limit_day):
        self.getDatabase().setLimitDay(limit_day)
