# Set styles for direction labels as indicators
off = """
QLabel {
    background-color: grey;
    border-radius: 15px;
    padding: 1px;
    color: white;
    min-width: 30px;
    min-height: 30px;
    max-width: 30px;
    max-height: 30px;
}
"""

on = """
QLabel {
    background-color: green;
    border-radius: 15px;
    padding: 1px;
    color: white;
    min-width: 30px;
    min-height: 30px;
    max-width: 30px;
    max-height: 30px;
}
"""    

# Set styles for circle buttons
circle_button_style = """
QPushButton {
    border: 2px solid #8f8f91;
    border-radius: 25px;  /* Half of the button's size */
    padding: 1px;
    background-color: #f0f0f0;
    min-width: 50px;
    min-height: 50px;
    max-width: 100px;
    max-height: 100px;
}
QPushButton:pressed {
    background-color: #d0d0d0;
}
"""

circle_button_style_on = """
QPushButton {
    border: 2px solid #8f8f91;
    border-radius: 25px;  /* Half of the button's size */
    padding: 1px;
    background-color: green;
    min-width: 50px;
    min-height: 50px;
    max-width: 100px;
    max-height: 100px;
}
QPushButton:pressed {
    background-color: #d0d0d0;
}
"""

# Set styles for direction labels as indicators
indicator_style_off = """
QLabel {
    background-color: grey;
    border-radius: 15px;
    padding: 1px;
    color: white;
    min-width: 30px;
    min-height: 30px;
    max-width: 30px;
    max-height: 30px;
}
"""
indicator_style_on = """
QLabel {
    background-color: green;
    border-radius: 15px;
    padding: 1px;
    color: white;
    min-width: 30px;
    min-height: 30px;
    max-width: 30px;
    max-height: 30px;
}
"""