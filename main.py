import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout
import shiboken6

from maya import cmds
import maya.api.OpenMaya as om
import maya.OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import Animation_Retime.UI.ui as ui

# Convert a Maya window into a QWidget object for interaction
def maya_dockable_window():
    main_window_pointer = omui.MQtUtil.mainWindow()
    return shiboken6.wrapInstance(int(main_window_pointer), QWidget)

# Creates a dockable window in Maya for retiming animated keyframes
class Animation_Retime(MayaQWidgetDockableMixin, QWidget):
    def __init__(self, parent=maya_dockable_window()):
        # Initializes the parent class and sets Maya main window as the parent
        super().__init__(parent)

        # Create instance of UI from UI file
        self.UI = ui.Animation_Retime_UI()

        # Set layout, window title, and add UI to layout
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.UI)
        self.setWindowTitle("Animation Retime")

        # Register callback to listen for the SelectionChanged event and trigger selection_changed when it occurs
        self.callback_id = om.MEventMessage.addEventCallback("SelectionChanged", self.selection_changed)

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

    """
        Whenever a selection is changed in Maya reset the slider and its label to 0
        *args is necessary to allow the method to take additional arguments
    """
    def selection_changed(self, *args):
        self.UI.slider.setValue(0)
        self.UI.slider_label.setText("0")

    # Removes the callback to stop listening for SelectionChanged
    def remove_callback(self):
        if self.callback_id:
            om.MMessage.removeCallback(self.callback_id)

    def button_pressed(self):
        # Checks which button was clicked
        button = self.sender() 

        # Value of buttons text converted to int
        button_value = int(button.text()) 
        
        # Query the current frame number from Maya
        current_frame = int(cmds.currentTime(query=True))

        # Adds clicked button value to current frame
        new_frame = current_frame + button_value 

        # Increase the value of selected keyframe by new_frame
        cmds.keyframe(time=(current_frame,), timeChange=new_frame) 
        
        # Sets the current time in Maya to the new frame
        cmds.currentTime(new_frame) 

    def slider_change(self, value):
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

        # Increase the value of selected keyframe by new_frame
        cmds.keyframe(time=(current_frame,), timeChange=new_frame)

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
    window.show(dockable=True)