import sys
from maya import cmds

from PySide6.QtWidgets import QMainWindow, QApplication
import Animation_Retime.UI.ui as ui

class Animation_Retime(QMainWindow):
    def __init__(self):
        super().__init__()

        self.UI = ui.Animation_Retime_UI()
        self.setCentralWidget(self.UI)

        self.UI.neg_100_btn.clicked.connect(self.button_pressed)
        self.UI.neg_50_btn.clicked.connect(self.button_pressed)
        self.UI.neg_10_btn.clicked.connect(self.button_pressed)
        self.UI.neg_1_btn.clicked.connect(self.button_pressed)
        self.UI.pos_1_btn.clicked.connect(self.button_pressed)
        self.UI.pos_10_btn.clicked.connect(self.button_pressed)
        self.UI.pos_50_btn.clicked.connect(self.button_pressed)
        self.UI.pos_100_btn.clicked.connect(self.button_pressed)

        self.prev_slider_val = 0

        self.UI.slider.valueChanged.connect(self.slider_change)

    def button_pressed(self):
        button = self.sender() # Gets the button clicked
        button_value = int(button.text()) # Value of button is text converted to int
        current_frame = int(cmds.currentTime(query=True)) # Gets the current time
        new_frame = current_frame + button_value # Adds clicked button value to current frame
        cmds.keyframe(time=(current_frame,), timeChange=new_frame) # Updates the current frame to the new frame
        cmds.currentTime(new_frame) # Set time to updated frame

    def slider_change(self, value):
        self.UI.slider_label.setText(f"{value}")
        current_frame = int(cmds.currentTime(query=True))
        
        # Not working as intended - Slider can be moved need to add logic to decrease by x steps if slider value is clicked
        # Need to add a check to reset the slider when a new object is selected
        if value > self.prev_slider_val:
            time_change = 1
        elif value < self.prev_slider_val:
            time_change = -1
        else:
            time_change = 0

        new_frame = current_frame + time_change
        cmds.currentTime(new_frame)
        self.prev_slider_val = value

if __name__ == '__main__':
    # Create a Qt application instance or use the existing one
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    # Create and show the UI window
    window = Animation_Retime()    
    window.show()