import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication
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
    def __init__(self, parent=maya_dockable_window(), toggle_state="horizontal", width=400, height=120):
        # Initializes the parent class and sets Maya main window as the parent
        super().__init__(parent)

        self.width = width
        self.height = height
        self.resize(self.width, self.height)

        # Create instance of UI from UI file with the UI toggle state set
        self.UI = ui.Animation_Retime_UI(toggle_state)

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

        self.UI.hoz_layout_btn.clicked.connect(self.setup_vert_window)
        self.UI.vert_layout_btn.clicked.connect(self.setup_hoz_window)

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

        # Call update_frame to update the keyframes and current time
        self.update_frame(current_frame, new_frame)

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

        # Call update_frame to update the keyframes and current time
        self.update_frame(current_frame, new_frame)

        # Update the old slider value
        self.prev_slider_val = value

    def check_keyed_frames_and_attributes(self):
        objects = cmds.ls(selection=True)
        if not objects:
            om.MGlobal.displayError("No object selected. Please select and object.")
        else:
            selected_obj = objects[0]

            keyable_attrs = cmds.listAttr(selected_obj, keyable=True) or []

    """
        Updates the keyframe and current time
        Raise error if no object selected or frames go negative
    """
    def update_frame(self, current_frame, new_frame):
        try:
            if new_frame < 1:
                om.MGlobal.displayError("Keyframes cannot be set to a negative value")
            else:
                # Increase the value of selected keyframe by new_frame
                cmds.keyframe(time=(current_frame,), timeChange=new_frame) 

                # Sets the current time in Maya to the new frame
                cmds.currentTime(new_frame) 
        except TypeError: # When no object selected
            om.MGlobal.displayWarning("No object selected")
        # except RuntimeError: # When trying to move a keyframe over another
            # Get obj and attr - cmds.ls(selection=True)[0]
            # cmds.cutKey(current_frame)
            # cmds.setKey(new_frame)

    # Setups a vertical window by closing and recreating a new Animation_Retime window
    def setup_vert_window(self):
        self.close()

        new_window = Animation_Retime(maya_dockable_window(), "vertical", 100, 200)
        new_window.show(dockable=True)

    # Setups a horizontal window by closing and recreating a new Animation_Retime window
    def setup_hoz_window(self):
        self.close()

        new_window = Animation_Retime(maya_dockable_window(), "horizontal", 400, 120)
        new_window.show(dockable=True)

# Checks if a window with the same title is open
def is_window_open(title):
    # Iterate through all top-level widgets to find a matching title
    for widget in QApplication.topLevelWidgets():
        if widget.windowTitle() == title and widget.isVisible():
            return widget
    return None

if __name__ == '__main__':
    # Create a Qt application instance or use the existing one
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    # Checks if a window is already open and brings it to the front if it is
    widget = is_window_open("Animation Retime")
    if widget:
        widget.raise_()
        widget.activateWindow()
    else:
        # Create and show the UI window
        window = Animation_Retime()    
        window.show(dockable=True)