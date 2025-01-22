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
        # Need to add a check to reset the slider when a new object is selected

        # Set the slider label text to slider value
        self.UI.slider_label.setText(f"{value}")

        # Query current frame number from Maya
        current_frame = int(cmds.currentTime(query=True))
        
        # Get the number of steps between two points on the slider
        time_change = abs(self.prev_slider_val - value)

        """
            Decrease current frame time if prev slider value is less than new value
            Increase current frame time if prev slider value is greater than new value
            If they are the same there is no increase so new frame must be current frame
        """
        if self.prev_slider_val > value:
            new_frame = current_frame - time_change
        elif self.prev_slider_val < value:
            new_frame = current_frame + time_change
        else:
            new_frame = current_frame

        # Sets the current time in Maya to the new frame
        cmds.currentTime(new_frame)

        # Update the old slider value
        self.prev_slider_val = value

if __name__ == '__main__':
    # Create a Qt application instance or use the existing one
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    # Create and show the UI window
    window = Animation_Retime()    
    window.show()