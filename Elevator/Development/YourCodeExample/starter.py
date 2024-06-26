from processor import SystemProcessor
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    processor = SystemProcessor()
    processor.run()
    sys.exit(app.exec_())
