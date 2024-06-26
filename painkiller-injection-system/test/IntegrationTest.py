import sys
sys.path.append("src")
from processor import InjectProcessor
from PyQt5.QtTest import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from unittest.mock import patch

def time_tracing_test():
    # Initialization and parameter setting
    app = QApplication(sys.argv)
    
    processor = InjectProcessor()
    
    processor.database.baseline = 0.01  
    processor.database.bolus = 0.3      
    
    # run
    processor.run()
    
    QTest.qWait(40000)
    
    app.exit()

@patch('PyQt5.QtWidgets.QMessageBox.warning')
@patch('checkPIN.CheckPINPage.exec_', return_value= QDialog.Accepted)
def setting_and_querying_test(mock_checkPINPage,mock_warning):
    # Initialization and parameter setting
    app = QApplication(sys.argv)
    
    processor = InjectProcessor()

    # run
    processor.run()

    # Press status button
    QTest.mouseClick(processor.mainboard.status_button, Qt.LeftButton)
    QTest.qWait(1000)

    # Press setting button
    QTest.mouseClick(processor.mainboard.setting_button,Qt.LeftButton)
    QTest.qWait(1000)

    # Set invalid parameter with baseline = 0.0; bolus = 0.0; limit_hour = 0.0;limit_day = 0
    processor.mainboard.setting_page.line_edits["Baseline (mL/min)"].setFocus()
    processor.mainboard.setting_page.line_edits["Baseline (mL/min)"].clear()
    QTest.keyClicks(processor.mainboard.setting_page.line_edits["Baseline (mL/min)"], "0.00")
    QTest.qWait(100)
    processor.mainboard.setting_page.line_edits["Bolus (mL/shot)"].setFocus()
    processor.mainboard.setting_page.line_edits["Bolus (mL/shot)"].clear()
    QTest.keyClicks(processor.mainboard.setting_page.line_edits["Bolus (mL/shot)"], "0.00")
    QTest.qWait(100)
    processor.mainboard.setting_page.line_edits["Limit per hour (mL)"].setFocus()
    processor.mainboard.setting_page.line_edits["Limit per hour (mL)"].clear()
    QTest.keyClicks(processor.mainboard.setting_page.line_edits["Limit per hour (mL)"], "0.00")
    QTest.qWait(100)
    processor.mainboard.setting_page.line_edits["Limit per day (mL)"].setFocus()
    processor.mainboard.setting_page.line_edits["Limit per day (mL)"].clear()
    QTest.keyClicks(processor.mainboard.setting_page.line_edits["Limit per day (mL)"], "0.0")

    QTest.qWait(1000)
    QTest.mouseClick(processor.mainboard.setting_page.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
    mock_warning.assert_called_once_with(processor.mainboard.setting_page, "Invalid Parameter", "Invalid input for Baseline (mL/min)!")

    # Set valid parameter with: baseline = 0.02; bolus = 0.3; limit_hour = 0.5;limit_day = 2 and Confirm with correct Pin
    processor.mainboard.setting_page.line_edits["Baseline (mL/min)"].setFocus()
    processor.mainboard.setting_page.line_edits["Baseline (mL/min)"].clear()
    QTest.keyClicks(processor.mainboard.setting_page.line_edits["Baseline (mL/min)"], "0.02")
    QTest.qWait(100)
    processor.mainboard.setting_page.line_edits["Bolus (mL/shot)"].setFocus()
    processor.mainboard.setting_page.line_edits["Bolus (mL/shot)"].clear()
    QTest.keyClicks(processor.mainboard.setting_page.line_edits["Bolus (mL/shot)"], "0.30")
    QTest.qWait(100)
    processor.mainboard.setting_page.line_edits["Limit per hour (mL)"].setFocus()
    processor.mainboard.setting_page.line_edits["Limit per hour (mL)"].clear()
    QTest.keyClicks(processor.mainboard.setting_page.line_edits["Limit per hour (mL)"], "0.50")
    QTest.qWait(100)
    processor.mainboard.setting_page.line_edits["Limit per day (mL)"].setFocus()
    processor.mainboard.setting_page.line_edits["Limit per day (mL)"].clear()
    QTest.keyClicks(processor.mainboard.setting_page.line_edits["Limit per day (mL)"], "2.0")

    QTest.qWait(1000)
    QTest.mouseClick(processor.mainboard.setting_page.button_box.button(QDialogButtonBox.Ok), Qt.LeftButton)
    
    QTest.qWait(1000)


    # Press status button
    QTest.mouseClick(processor.mainboard.status_button, Qt.LeftButton)
    QTest.qWait(1000)

    # Press query button
    QTest.mouseClick(processor.mainboard.history_button, Qt.LeftButton)
    QTest.qWait(1000)
    app.exit()


def add_injection_test():
    # initialization
    app = QApplication(sys.argv)
    
    processor = InjectProcessor()
    
    processor.database.baseline = 0.02  
    processor.database.bolus = 0.3      
    processor.database.remaining = 0
    # run
    processor.run()
    
    # (patient) press patient_button intending for inject bolus
    QTest.mouseClick(processor.mainboard.patient_button.inject_button, Qt.LeftButton)
    QTest.qWait(500)

    # (physician) press add_button to add painkiller
    QTest.mouseClick(processor.mainboard.add_button, Qt.LeftButton)
    QTest.qWait(1000)
    
    # (patient) press patient_button intending for inject bolus
    QTest.mouseClick(processor.mainboard.patient_button.inject_button, Qt.LeftButton)
    QTest.qWait(1000)
    
    # (patient) press patient_button intending for inject bolus
    QTest.mouseClick(processor.mainboard.patient_button.inject_button, Qt.LeftButton)
    QTest.qWait(1000)

    # (patient) press patient_button intending for inject bolus
    QTest.mouseClick(processor.mainboard.patient_button.inject_button, Qt.LeftButton)
    QTest.qWait(1000)
    
    # (patient) press patient_button intending for inject bolus
    QTest.mouseClick(processor.mainboard.patient_button.inject_button, Qt.LeftButton)
    QTest.qWait(1000)

    QTest.qWait(2000)
    
    app.exit()


if __name__ == '__main__':
    time_tracing_test()
    setting_and_querying_test()
    add_injection_test()
