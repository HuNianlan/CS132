from processor import InjectProcessor
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    processor = InjectProcessor()

    processor.run()

    sys.exit(app.exec_())
