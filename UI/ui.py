from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QFrame
from PySide6.QtGui import Qt

class Animation_Retime_UI(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_UI()

    def setup_UI(self):
        main_layout = QVBoxLayout(self)

        button_layout = QHBoxLayout(self)

        # Buttons in range -100:100
        self.neg_100_btn = QPushButton("-100")
        self.neg_50_btn = QPushButton("-50")
        self.neg_10_btn = QPushButton("-10")
        self.neg_1_btn = QPushButton("-1")
        self.pos_1_btn = QPushButton("1")
        self.pos_10_btn = QPushButton("10")
        self.pos_50_btn = QPushButton("50")
        self.pos_100_btn = QPushButton("100")

        # Create a vertical line
        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.VLine)

        # Set the thickness of the line
        vertical_line.setStyleSheet("QFrame { background-color: #262626; width: 5px; }")
        
        buttons = [self.neg_100_btn, self.neg_50_btn, self.neg_10_btn, self.neg_1_btn,
                   vertical_line, self.pos_1_btn, self.pos_10_btn, self.pos_50_btn, self.pos_100_btn]

        # Add buttons and line to layout
        for btn in buttons:
            button_layout.addWidget(btn)

        # Create horizontal slider with max 100 min -100
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(100)
        self.slider.setValue(0)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.slider)
