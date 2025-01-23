from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel
from PySide6.QtGui import Qt

class Animation_Retime_UI(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        # Button used to toggle between vertical/horizontal layouts
        self.layout_toggle_btn = QPushButton("")
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

        # Setups a horizontal layout
        self.setup_hoz_layout()

        # Calls toggle_layout when toggle button is clicked
        self.layout_toggle_btn.clicked.connect(self.toggle_layout)

    # Toggles between the horizontal and vertical layouts
    def toggle_layout(self):

        # Clears the current self.main_layout
        self.clear_layout()

        # Call respective setup method based on toggle_state
        if self.toggle_state == "vertical":
            self.setup_hoz_layout()
            self.toggle_state = "horizontal"
        else:
            self.setup_vert_layout()
            self.toggle_state = "vertical"

    # Remove all items from the main layout but keep the widgets intact
    def clear_layout(self):
        # Gets number of items in layout
        while self.main_layout.count():

            # Removes item at index 0 which is always the first item
            item = self.main_layout.takeAt(0)
            
            # Checks if the item is a widget
            widget = item.widget() 
            
            # If item is a widget, detach the widget from the layout without deleting it
            if widget:
                widget.setParent(None)

    # Sets up a horizontal layout
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

        self.slider.setOrientation(Qt.Horizontal)

        # Add button_layout and slider to hoz_layout
        hoz_layout = QVBoxLayout()
        hoz_layout.addLayout(button_layout)
        hoz_layout.addWidget(self.slider)
        hoz_layout.addWidget(self.layout_toggle_btn)

        # Add hoz_layout to main_layout
        self.main_layout.addLayout(hoz_layout)

        self.toggle_state = "horizontal"

    # Sets up a vertical layout
    def setup_vert_layout(self):
        button_layout = QVBoxLayout(self)

        for btn in self.positive_buttons:
            button_layout.addWidget(btn)

        button_layout.addWidget(self.slider_label)

        for btn in self.negative_buttons:
            button_layout.addWidget(btn)

        self.slider.setOrientation(Qt.Vertical)

        # Add button_layout and slider to hoz_layout
        hoz_layout = QHBoxLayout()
        hoz_layout.addWidget(self.layout_toggle_btn)
        hoz_layout.addLayout(button_layout)
        hoz_layout.addWidget(self.slider)

        # Add hoz_layout to main_layout
        self.main_layout.addLayout(hoz_layout)

        self.toggle_state = "vertical"