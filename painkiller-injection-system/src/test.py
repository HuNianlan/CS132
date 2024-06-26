from processor import InjectProcessor
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    processor = InjectProcessor()

    cases = [
        "set_baseline@0.01ml/min",
        "set_bolus@0.30ml/shot",
        "baseline_on",
        "30min request_bolus",
        "75min request_bolus",
        "baseline_off",
        "set_baseline@0.1ml/min",
        "baseline_on",
        # "test_finish"
    ]

    processor.run()

    processor.txtcasesUpload(cases)
    
    sys.exit(app.exec_())
