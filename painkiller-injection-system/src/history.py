from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class HistoryPage(QDialog):
    '''
    This is a class for History Page.

    HistoryPage class create a window to show the inject history.

    Attributes:
        events_dict:   A dictory of events history.
    '''

    def __init__(self, events_lst):
        super().__init__()
        self.events_lst = events_lst
        self.initUI()
    
    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('History')

        layout = QVBoxLayout()
        self.tableWideget = QTableWidget()
        self.tableWideget.setRowCount(len(self.events_lst))
        self.tableWideget.setColumnCount(2)
        self.tableWideget.setColumnWidth(0, 300)
        self.tableWideget.setColumnWidth(1, 500)
        layout.addWidget(self.tableWideget)

        index = 0
        self.tableWideget.setHorizontalHeaderLabels(["Time", "Event"])
        for event in self.events_lst:
            newItem = QTableWidgetItem(event[0].toString('yyyy-MM-dd HH:mm:ss'))
            self.tableWideget.setItem(index, 0, newItem)
            newItem = QTableWidgetItem(event[1])
            self.tableWideget.setItem(index, 1, newItem)
            index = index + 1

        self.orderType = Qt.DescendingOrder

        self.setLayout(layout)
