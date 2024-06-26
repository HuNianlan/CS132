import sys
sys.path.append("src")
from processor import InjectProcessor
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtTest import QTest

# Get information
cases_3_1 = []

# Get dynamic data
cases_3_2 = [
    "set_baseline@0.01ml/min",
    "set_bolus@0.30ml/shot",
    "baseline_on",
    "30min request_bolus",
    "75min request_bolus",
    "baseline_off",
    "set_baseline@0.1ml/min",
    "baseline_on",
]

# Set Parameter
# cases_3_3 = [
# Press reset Pin button;
# Enter Wrong Pin;
# Enter Correct Pin;
# Type correct form of new Pin and Confirm
# (new Pin = “123456”)
# Press Setting button 
# Set invalid parameter with:
# baseline = 0.00; bolus = 0.00;
# Set valid parameter with:
# baseline = 0.01; bolus = 0.30;
# Confirm with initial Pin(“000000”)
# Confirm with new Pin(“123456”)
# Press query(history) button
# ]



# Inject
cases_3_4 = [
    "set_baseline@0.02ml/min",
    "set_bolus@0.30ml/shot",
    "baseline_on",
    "10min request_bolus",
    "15min request_bolus",
    "20min request_bolus",
    "baseline_off",
    "78min request_bolus",
    "86min request_bolus",
    "baseline_on",
    "220min request_bolus",
]

def functional_test(cases):

    processor = InjectProcessor()

    processor.run()
    QTest.qWait(2000)

    processor.txtcasesUpload(cases)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    functional_test(cases_3_1) 
    functional_test(cases_3_2) 
    functional_test(cases_3_4) 

    sys.exit(app.exec_())
