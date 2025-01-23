from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
from PySide6.QtGui import Qt

class Animation_Retime_UI(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        # Button used to toggle between vertical/horizontal layouts
        self.layout_toggle_btn = QPushButton("")
        self.layout_toggle_btn.setFixedHeight(2)
        self.layout_toggle_btn.setStyleSheet("background-color: white;")
        self.toggle_state = "horizontal"

        # Buttons in range -100:100
        self.neg_100_btn = QPushButton("-100")
        self.neg_50_btn = QPushButton("-50")
        self.neg_10_btn = QPushButton("-10")
        self.neg_1_btn = QPushButton("-1")
        self.pos_1_btn = QPushButton("+1")
        self.pos_10_btn = QPushButton("+10")
        self.pos_50_btn = QPushButton("+50")
        self.pos_100_btn = QPushButton("+100")

        self.negative_buttons = [self.neg_100_btn, self.neg_50_btn, self.neg_10_btn, self.neg_1_btn]
        self.positive_buttons = [self.pos_1_btn, self.pos_10_btn, self.pos_50_btn, self.pos_100_btn]

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

        self.setup_hoz_layout()

        self.layout_toggle_btn.clicked.connect(self.toggle_layout)

    def toggle_layout(self):
        self.clear_layout(self.main_layout)

        if self.toggle_state == "vertical":
            self.setup_hoz_layout()
        else:
            self.setup_vert_layout()

    # Removes items and layouts within a layout
    def clear_layout(self, layout):
        # Get number of things within the layout
        while layout.count():
            # Remove first item
            item = layout.takeAt(0)

            # If item is a layout, recursively clear it
            if item.layout():
                sub_layout = item.layout()
                self.clear_layout(sub_layout)

            # If item is a widget, schedule to delete
            if item.widget():
                item.widget().deleteLater()

    def setup_hoz_layout(self):
        button_layout = QHBoxLayout(self)
            
        # Add negative buttons to layout
        for btn in self.negative_buttons:
            button_layout.addWidget(btn)
        
        # Add the slider label
        button_layout.addWidget(self.slider_label)
        
        # Add positive buttons to layout
        for btn in self.positive_buttons:
            button_layout.addWidget(btn)
        
        # Add button_layout and slider to main_layout
        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.slider)
        self.main_layout.addWidget(self.layout_toggle_btn)

        self.toggle_state = "horizontal"

    def setup_vert_layout(self):
        button_layout = QVBoxLayout(self)

        for btn in self.positive_buttons:
            button_layout.addWidget(btn)

        button_layout.addWidget(self.slider_label)

        for btn in self.negative_buttons:
            button_layout.addWidget(btn)

        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.slider)
        self.main_layout.addWidget(self.layout_toggle_btn)

        self.toggle_state = "vertical"