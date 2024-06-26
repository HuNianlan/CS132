class InjectDatabase():
    '''
    This is a class for Injection Database.

    InjectDatabase class contains the settings of injection processor and corresponding data.
    This class realizes the functions of the painkiller system as well,
    i.e. set/get the baseline/bolus/injection status/painlevel, inject, etc.
    For particular usage, please refer to the functions below.

    Attributes:
        Pin:            A string of the PIN of the processor.
        bolus:          A float number of the dosis injected for a shot.
        baseline:       A float number of the dosis speed, i.e. dosis injected in a minute.
        limit_day:      A float number of the maximum dosis injected in an hour.
        limit_hour:     A float number of the maximum dosis injected in a day.
        remaining:      A float number of the remaining painkiller in the injection processor.
        capacity:       A float number of the maximum capacity of the injection processor.
        status:         A bool of the baseline status, i.e. baseline on/off.
        bolus_history:  A dictionary of the injection history, i.e. the time and bolus.
        event_history:  A dictionary of the event history, i.e. the time and the operation.
    '''
    def __init__(self):
        self.Pin: str = "000000"
        self.bolus: float = 0.0
        self.baseline: float = 0.0
        self.limit_day: float = 3.0
        self.limit_hour: float = 1.0
        self.remaining: float = 10.0
        self.capacity : float = 10.0
        self.status: bool = True
        self.bolus_history: dict = {}
        self.baseline_history : dict = {}
        self.event_history: list = []
    
    def inject(self):
        self.updateRemain(self.getBolus())
    
    def addPainkiller(self):
        self.remaining = self.capacity

    def updateRemain(self, amount):
        self.remaining = self.remaining - amount
    
    def addBolusHistory(self, time):
        self.bolus_history[time] = self.getBolus()
    
    def addBaselineHistory(self, time, amount):
        self.baseline_history[time] = amount
    
    def addEventHistory(self, time, event):
        self.event_history.append([time, event])
    
    def resetPIN(self, Pin):
        self.Pin = Pin

    def setBolus(self, bolus):
        self.bolus = bolus
    
    def setBaseline(self, baseline):
        self.baseline = baseline
    
    def setLimitHour(self, limit_hour):
        self.limit_hour = limit_hour
    
    def setLimitDay(self, limit_day):
        self.limit_day = limit_day
    
    def setStatus(self):
        self.status = not self.status
    
    def getPin(self):
        return self.Pin
    
    def getBolus(self):
        return self.bolus

    def getBaseline(self):
        return self.baseline
    
    def getLimitHour(self):
        return self.limit_hour
    
    def getLimitDay(self):
        return self.limit_day
    
    def getStatus(self):
        return self.status
    
    def getRemain(self):
        return self.remaining
    
    def getCapacity(self):
        return self.capacity
    
    def getBolusHistory(self):
        return self.bolus_history
    
    def getEventHistory(self):
        return self.event_history
    
    def getBaselineHistory(self):
        return self.baseline_history

    def getHourBolus(self, time):
        amount = 0.0
        for time_his, amount_his in self.getBolusHistory().items():
            if time_his.secsTo(time) / 60 <= 60:
                amount += amount_his
        return amount
    
    def getDayBolus(self, time):
        amount = 0
        for time_his, amount_his in self.getBolusHistory().items():
            if time_his.secsTo(time) / 60 <= 1440:
                amount += amount_his
        return amount

    def getHourBaseline(self, time):
        amount = 0.0
        hist = self.baseline_history
        target_time = time
        for time_his in reversed(hist):
            baseline_his = hist[time_his]
            if time_his.secsTo(time) / 60 <= 60:
                amount += baseline_his * (time_his.secsTo(target_time) / 60)
                target_time = time_his
        return amount
    
    def getDayBaseline(self, time):
        amount = 0.0
        hist = self.baseline_history
        target_time = time
        for time_his in reversed(hist):
            baseline_his = hist[time_his]
            if time_his.secsTo(time) / 60 <= 1440:
                amount += baseline_his * (time_his.secsTo(target_time) / 60)
                target_time = time_his
        return amount

    def getHour(self, time):
        return self.getHourBolus(time) + self.getHourBaseline(time)
    
    def getDay(self, time):
        return self.getDayBolus(time) + self.getDayBaseline(time)