import sys
sys.path.append("Development/YourCodeExample")
from processor import SystemProcessor
from PyQt5.QtWidgets import QApplication

'''
    This is the starter for all the functional tests.
    Please run this file before testing any of the cases.
    Please run this file under the root path, i.e. Elevator.
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    processor = SystemProcessor()
    processor.elevator_processors[0].elevator.current_floor = -1
    processor.elevator_processors[1].elevator.current_floor = 3
    processor.run()
    sys.exit(app.exec_())
