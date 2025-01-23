from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
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
        self.pos_1_btn = QPushButton("+1")
        self.pos_10_btn = QPushButton("+10")
        self.pos_50_btn = QPushButton("+50")
        self.pos_100_btn = QPushButton("+100")

        # Create horizontal slider with range -100 to 100
        self.slider = QSlider()
        self.slider.setRange(-100, 100)
        self.slider.setOrientation(Qt.Horizontal) # Slider orientation
        self.slider.setSingleStep(1) # Set the step size to 1 
        self.slider.setValue(0) # Starting value

        # Create a slider label with a grey background and white text
        self.slider_label = QLabel("0")
        self.slider_label.setStyleSheet("""
                                        background-color: #262626; 
                                        color: white;
                                        padding: 8px;                                        
                                   """)
        self.slider_label.setFixedWidth(50) # Sets width of label to fixed value
        self.slider_label.setAlignment(Qt.AlignCenter) # Center align text
        
        negative_buttons = [self.neg_100_btn, self.neg_50_btn, self.neg_10_btn, self.neg_1_btn]
        positive_buttons = [self.pos_1_btn, self.pos_10_btn, self.pos_50_btn, self.pos_100_btn]

        # Add negative buttons to layout
        for btn in negative_buttons:
            button_layout.addWidget(btn)

        # Add the slider label
        button_layout.addWidget(self.slider_label)

        # Add positive buttons to layout
        for btn in positive_buttons:
            button_layout.addWidget(btn)

        # Add button_layout and slider to main_layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.slider)