import sys
from maya import cmds

from PySide6.QtWidgets import QMainWindow, QApplication
import Animation_Retime.UI.ui as ui

class Animation_Retime(QMainWindow):
    def __init__(self):
        super().__init__()

        self.UI = ui.Animation_Retime_UI()
        self.setCentralWidget(self.UI)

        self.UI.zero_0_btn.pressed.connect(self.button_pressed)

    def button_pressed(self):
        cmds.polySphere()

if __name__ == '__main__':
    # Create a Qt application instance or use the existing one
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    # Create and show the UI window
    window = Animation_Retime()    
    window.show()