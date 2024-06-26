from PyQt5 import QtCore, QtGui, QtWidgets


class NumberPadWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NumberPadWidget, self).__init__(parent)
        self.current_line_edit = None
        self.setFixedSize(350, 350)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QGridLayout()

        numbers = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('', 3, 0), ('0', 3, 1), ('', 3, 2)
        ]

        # Create number buttons and add them to the layout
        for text, row, col in numbers:
            button = QtWidgets.QPushButton(text, self)
            button.setFixedSize(80, 80)
            if text:
                button.clicked.connect(self.buttonClicked)
            layout.addWidget(button, row, col)

        # Add Clear and Enter buttons
        clear_button = QtWidgets.QPushButton('Clear', self)
        clear_button.setFixedSize(80, 160)
        clear_button.clicked.connect(self.clear_display)
        layout.addWidget(clear_button, 0, 3, 2, 1)

        enter_button = QtWidgets.QPushButton('Enter', self)
        enter_button.setFixedSize(80, 160)
        enter_button.clicked.connect(self.enter_amount)
        layout.addWidget(enter_button, 2, 3, 2, 1)

        self.setLayout(layout)

    def buttonClicked(self):
        if self.current_line_edit:
            sender = self.sender()
            current_text = self.current_line_edit.text()
            new_text = current_text + sender.text()
            self.current_line_edit.setText(new_text)

    def clear_display(self):
        if self.current_line_edit:
            self.current_line_edit.clear()

    def enter_amount(self):
        if self.current_line_edit:
            print(f"Entered amount: {self.current_line_edit.text()}")
            # self.clear_display()

    def set_current_line_edit(self, line_edit):
        self.current_line_edit = line_edit

    