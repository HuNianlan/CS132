import sys
from PyQt5 import QtWidgets
from banking_app.app_ui import Ui_APP_UI
from atm.atm_ui import Ui_ATM
from processor import my_processor
from DB import reset
from PyQt5.QtWidgets import QMainWindow, QPushButton

class Open_APP(QMainWindow):
    def __init__(self,processor = my_processor):
        super().__init__()
        self.processor = processor
        self.initUI()
    
    def initUI(self):
        self.setGeometry(1000, 300, 200, 200)
        self.setWindowTitle('Open APP')

        self.inject_button = QPushButton("+", self)
        self.inject_button.clicked.connect(self.open_app)
        self.inject_button.setGeometry(50, 50, 100, 100)
    
    def open_app(self):
        self.processor.process("open_app")
        app = Ui_APP_UI(self.processor,self.processor.app_count)
        app.show()




# atm only

# if __name__ == '__main__':
#     reset()
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_ATM(MainWindow,my_processor)
#     MainWindow.show()
#     sys.exit(app.exec_())

# app_only
# if __name__ == '__main__':
#     reset()
#     app = QtWidgets.QApplication(sys.argv)
#     app_ui = QtWidgets.QWidget()
#     ui_app = Ui_APP_UI(my_processor)
#     ui_app.setupUi(app_ui, my_processor)
#     response = my_processor.process("open_app")
#     if response.startswith("app_opened#"):
#         app_id = response.split("#")[1]
#         ui_app.set_app_id(app_id)
#     app_ui.show()
#     sys.exit(app.exec_())



if __name__ == "__main__":
    reset()

    app = QtWidgets.QApplication(sys.argv)

    # Create APP_UI window
    open_button = Open_APP(my_processor)
    open_button.show()

    # Create ATM window
    MainWindow = QtWidgets.QMainWindow()
    ui_atm = Ui_ATM(MainWindow, my_processor,0)
    MainWindow.show()

    # Manage both windows
    app.lastWindowClosed.connect(app.quit)
    sys.exit(app.exec_())
