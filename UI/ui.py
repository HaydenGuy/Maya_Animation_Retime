from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class Animation_Retime_UI(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_UI()

    def setup_UI(self):
        main_layout = QVBoxLayout(self)

        self.button = QPushButton("Button")
        main_layout.addWidget(self.button)
