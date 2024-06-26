import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QInputDialog, QMessageBox, QSlider
from PyQt5.QtCore import QTimer, QDateTime, pyqtSignal, QObject

class InjectProcessor(QObject):
    def __init__(self, mainboard):
        super().__init__()
        self.mainboard = mainboard
        self.mainboard.time_updated.connect(self.handle_time_update)
        self.current_time = mainboard.current_time

    def handle_time_update(self, current_time):
        self.current_time = current_time

    def process_input(self, cases):
        for case in cases:
            if case == "test_finish":
                sys.exit()
            print("Server: " + case)
            if case.startswith("set_baseline@"):
                self.set_baseline(float(case.split("@")[1].split("m")[0]), self.current_time)
            elif case.startswith("set_bolus@"):
                self.set_bolus(float(case.split("@")[1].split("m")[0]))
            elif case == "baseline_on":
                self.set_status_on(self.current_time)
            elif case == "baseline_off":
                self.set_status_off(self.current_time)
            elif case.endswith("request_bolus"):
                minutes = int(case.split("min")[0])
                target_time = self.mainboard.initial_time.addSecs(minutes * 60)
                inject_thread = threading.Thread(target=self.wait_and_inject, args=(target_time,))
                inject_thread.start()
                inject_thread.join()  # Wait for the injection to complete before proceeding

    def wait_and_inject(self, target_time):
        remaining_seconds = self.current_time.secsTo(target_time)
        while remaining_seconds > 0:
            time.sleep(1)
            remaining_seconds -= 1
        if self.check_inject(self.current_time, self.get_bolus()):
            self.inject()
            print("Inject successfully.\n")
        else:
            print("No injection.\n")

    def set_baseline(self, value, time):
        print(f"Baseline set to {value} at {time.toString()}")

    def set_bolus(self, value):
        print(f"Bolus set to {value}")

    def set_status_on(self, time):
        print(f"Status set to ON at {time.toString()}")

    def set_status_off(self, time):
        print(f"Status set to OFF at {time.toString()}")

    def get_bolus(self):
        return 0.2

    def check_inject(self, current_time, bolus):
        return True

    def inject(self):
        print("Injection performed")

class Mainboard(QMainWindow):
    time_updated = pyqtSignal(QDateTime)

    def __init__(self):
        super().__init__()
        self.current_time = QDateTime.currentDateTime()
        self.initial_time = self.current_time
        self.processor = InjectProcessor(self)
        self.timer_interval = 1000

        self.initUI()
        self.start_timer()

    def initUI(self):
        self.setWindowTitle('Painkiller Injection System')
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Label to display current time
        self.time_label = QLabel()
        layout.addWidget(self.time_label)
        self.time_updated.connect(self.update_time_label)

        # Speed slider
        self.speed_slider = QSlider()
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(60)
        self.speed_slider.setValue(1)
        layout.addWidget(self.speed_slider)
        
        # Button to prompt password input
        self.status_button = QPushButton("On / Off")
        self.status_button.setCheckable(True)
        self.status_button.clicked.connect(self.set_status)
        layout.addWidget(self.status_button)

        central_widget.setLayout(layout)

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(self.timer_interval)

    def update_time(self):
        sec = self.speed_slider.value()
        self.current_time = self.current_time.addSecs(sec)
        self.time_updated.emit(self.current_time)

    def update_time_label(self, current_time):
        self.time_label.setText(current_time.toString('yyyy-MM-dd HH:mm:ss'))

    def set_status(self):
        if self.check_PIN():
            inject_status = self.status_button.isChecked()
            self.processor.getDatabase().setStatus(inject_status)
            if inject_status:
                print("baseline_on_set")
            else:
                print("baseline_off_set")

    def check_PIN(self):
        # Implement actual PIN check logic here
        return True

    def getDatabase(self):
        class DummyDatabase:
            def setStatus(self, status):
                print(f"Database status set to: {'on' if status else 'off'}")
        return DummyDatabase()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainboard = Mainboard()
    mainboard.resize(300, 200)
    mainboard.show()
    sys.exit(app.exec_())
