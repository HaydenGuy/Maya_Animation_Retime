from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider
from PySide6.QtGui import Qt


class Animation_Retime_UI(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_UI()

    def setup_UI(self):
        main_layout = QVBoxLayout(self)

        button_layout = QHBoxLayout(self)

        self.neg_100_btn = QPushButton("-100")
        self.neg_50_btn = QPushButton("-50")
        self.neg_10_btn = QPushButton("-10")
        self.neg_1_btn = QPushButton("-1")
        self.pos_1_btn = QPushButton("1")
        self.pos_10_btn = QPushButton("10")
        self.pos_50_btn = QPushButton("50")
        self.pos_100_btn = QPushButton("100")

        buttons = [self.neg_100_btn, self.neg_50_btn, self.neg_10_btn, self.neg_1_btn,
                   self.pos_1_btn, self.pos_10_btn, self.pos_50_btn, self.pos_100_btn]

        for btn in buttons:
            button_layout.addWidget(btn)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(100)
        self.slider.setValue(0)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.slider)
