import sys
import time
import random
from PyQt5 import QtWidgets, QtCore
from NetClient import ZmqClientThread
from simulator import Simulator
from DB import reset
from processor import my_processor

# This function determines whether a new message has been received
def is_received_new_message(oldTimeStamp: int, oldServerMessage: str, Msgunprocessed: bool = False) -> bool:
    if Msgunprocessed:
        return True
    else:
        if oldTimeStamp == zmqThread.messageTimeStamp and oldServerMessage == zmqThread.receivedMessage:
            return False
        else:
            return True

if __name__ == '__main__':
    identity = "Team7"  # write your team name here.
    zmqThread = ZmqClientThread(identity=identity)

    timeStamp = -1
    serverMessage = ""
    messageUnprocessed = False

    reset()

    app = QtWidgets.QApplication([])

    MainWindow = QtWidgets.QMainWindow()
    sim = Simulator(MainWindow)
    sim.processor.return_signal.connect(zmqThread.sendMsg)
    MainWindow.show()

    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: sim.simulate(zmqThread.receivedMessage) if is_received_new_message(timeStamp, serverMessage, messageUnprocessed) else None)
    timer.start(5000)  

    sys.exit(app.exec_())
