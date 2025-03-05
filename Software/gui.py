import sys
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow,
    QPushButton, QFrame, QStackedWidget, QRadioButton, QLineEdit, QButtonGroup, QComboBox,
)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from interface import *
from registers import *
from constants import *
from comm_device import *
from calc import *
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Application window with basic settings
        self.setWindowTitle("OrcaProbe")                    # Title of the window
        self.setGeometry(100, 100, 800, 600)                # Set position and size of the window
        self.setStyleSheet("background-color: #d8cfcf;")    # Set background color for the main screen
        self.setWindowIcon(QIcon("./media/OrcaProbe_Logo.png"))   # Application icon path

        # Sidebar for measurement type selection
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()                          # Create a vertical layout for the sidebar
        sidebar.setStyleSheet("background-color: #b7a9a9;")     # Set sidebar background color
        sidebar.setFixedWidth(400)                              # Set the width of the sidebar

        # Sidebar title with an image
        image_label = QLabel()
        image_label.setPixmap(QPixmap("./media/orcalogo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setContentsMargins(0, 0, 0, 0)
        image_label.setStyleSheet("margin-bottom: 0px;")

        title_label = QLabel("Orca Advanced\nMaterial's Inc")                    # Sidebar title
        title_label.setAlignment(Qt.AlignLeft)                                   # Align the title
        title_label.setFont(QFont("Arial", 16, QFont.Bold))                      # Set font style and size
        title_label.setStyleSheet("color: #000000; margin-bottom: 0px;")         # Set the color, adjust margin below the subtitle

        # Combine the image and title in a horizontal layout
        title_layout = QHBoxLayout()
        title_layout.addWidget(image_label, alignment=Qt.AlignLeft)
        title_layout.addWidget(title_label, alignment=Qt.AlignRight)

        title_widget = QWidget()
        title_widget.setLayout(title_layout)
        title_widget.setContentsMargins(0, 0, 0, 0)                                             # Remove margins around the title widget

        sidebar_layout.setSpacing(5)                                                            # Reduce spacing between widgets
        sidebar_layout.addWidget(title_widget)                                                  # Add the combined widget to the sidebar

        subtitle_label = QLabel("OrcaProbe")                                                    # Sidebar subtitle
        subtitle_label.setAlignment(Qt.AlignCenter)                                             # Align the title
        subtitle_label.setFont(QFont("Arial", 14, QFont.Bold))                                  # Set font style and size
        subtitle_label.setStyleSheet("color: #000080; margin-top: 0px; margin-bottom: 10px;")   # Set the color, adjust margin above and below the subtitle
        sidebar_layout.addWidget(subtitle_label)                                                # Add the subtitle to the sidebar

        self.add_measurement_selection(sidebar_layout, "2-probe Measurements", [    # Add 2-probe measurement selections to the sidebar
            "DC Resistance",
            "Current-Voltage",
            "Capacitance-Voltage (2-p)",
            "Impedance Spectroscopy (2-p)"
        ])
        self.add_measurement_selection(sidebar_layout, "3-probe Measurements", [    # Add 3-probe measurement selections to the sidebar
            "Transfer Characteristics",
            "Output Characteristics",
            "Capacitance-Voltage (3-p)",
            "Electrochemical"
        ])
        self.add_measurement_selection(sidebar_layout, "4-probe Measurements", [    # Add 4-probe measurement selections to the sidebar
            "Probe Resistance",
            "Low-Resistance",
            "Impedance Spectroscopy (4-p)"
        ])

        sidebar_layout.addStretch(1)                                                # Add a spacer to push items to the top of the sidebar
        sidebar.setLayout(sidebar_layout)

        # Error bar at the bottom for showing the status of error checks
        error_bar = self.create_error_bar()

        # Probe configuration bar with dropdowns for selecting probe functionality
        self.probe_config_bar = self.create_probe_config_bar()

        # Page widget to hold different measurement pages
        self.page_widget = QStackedWidget()
        page_widget = QWidget()
        
        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar)              # Add the sidebar to the main layout
        main_layout.addWidget(self.page_widget)     # Add the central area to the main layout
        main_layout.setStretch(1, 2)                # Set the main layout's central area to stack the sidebar and measurement page appropriately

        # Central layout to organizes the layout of the main area
        central_layout = QVBoxLayout()
        central_layout.addLayout(main_layout)       # Add main layout (has sidebar and page widget)
        central_layout.addWidget(self.probe_config_bar)  # Add probe configuration bar
        central_layout.addWidget(error_bar)         # Add status bar

        # Initialize page widget for the main window
        self.setCentralWidget(page_widget)
        page_widget.setLayout(central_layout)       # Add the central layout to all the measurement pages

        # Blank main page
        self.main_page = QWidget()
        self.page_widget.addWidget(self.main_page)

        self.current_selected_measurement = None    # Initialize to track the selected measurement
        self.ser = init_ser_port('com3', 115200)   # open a serial connection on com8 with baud rate 115200

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_serial_data)  # Call periodically

    def add_measurement_selection(self, layout, section_title, options):
        # For each measurement section (2-probe, 3-probe and 4-probe)
        button = QPushButton(section_title)             # Create a button
        button.setCheckable(True)                       # Make the buttons toggleable
        button.setFont(QFont("Arial", 10, QFont.Bold))  # Set the font for the buttons
        button.setStyleSheet("""                
            background-color: #ffffff;
            padding: 6px;
            text-align: left;
            border: none;
        """)                                            # Add styling for the buttons
        
        option_container = QWidget()                    # Create container for measurement types
        option_layout = QVBoxLayout()                   # Vertical layout to arrange measurement types
        option_layout.setSpacing(3)                     # Reduce spacing between measurement types
        option_container.setLayout(option_layout)       # Use the layout initialized in the container
        option_container.setVisible(False)              # Options start collapsed

        # Connect the container to the measurement section when its clicked
        button.clicked.connect(lambda: option_container.setVisible(button.isChecked()))   
        
        # Add to the sidebar layout
        layout.addWidget(button)            # The measurement section buttons
        layout.addWidget(option_container)  # The measurement type container

        # For each measurement type
        for option_text in options:
            option_button = QPushButton(option_text)    # Create a button
            option_button.setFont(QFont("Arial", 10))   # Set the font for the buttons
            option_button.setStyleSheet("""
                background-color: #ffffff;
                padding: 5px;
                text-align: left;
                border: 1px solid #cccccc;
            """)                                        # Add styling for the buttons
            
            # Connect each button to a function that handles the selection state
            option_button.clicked.connect(lambda _, title=option_text, btn=option_button: self.toggle_selection(title, btn))

            # Add the option button to the layout under the measurement section
            option_layout.addWidget(option_button)

    def toggle_selection(self, title, button):
        # If the same button is clicked again, deselect it
        if self.current_selected_measurement == button:
            button.setStyleSheet("background-color: #ffffff; padding: 5px; text-align: left; border: 1px solid #cccccc;")
            self.page_widget.setCurrentWidget(self.main_page)   # Hide the page when deselected
            self.current_selected_measurement = None

        # If a different button is clicked
        else:
        # Deselect the previously selected one
            if self.current_selected_measurement:
                self.current_selected_measurement.setStyleSheet("background-color: #ffffff; padding: 5px; text-align: left; border: 1px solid #cccccc;")
            
        # Highlight the newly selected button
            button.setStyleSheet("background-color: #ffffff; padding: 5px; text-align: left; border: 2px solid black;")
            self.current_selected_measurement = button
            self.show_page(title)                           # Show the corresponding page

    def show_page(self, title):
        # Show the page corresponding to the selected measurement
        for index in range(self.page_widget.count()):
            if self.page_widget.widget(index).objectName() == title:
                self.page_widget.setCurrentIndex(index)                 # Display the  page
                return

        # If the page doesn't exist, create a new one
        new_page = self.create_measurement_page(title)
        new_page.setObjectName(title)                   # Set the page's name as the title of the measurement type
        self.page_widget.addWidget(new_page)            # Add the new page to the stacked widget
        self.page_widget.setCurrentWidget(new_page)     # Display the new page

    def create_measurement_page(self, title):
        page = QWidget()                                    # Create a new page for the selected measurement
        layout = QVBoxLayout()

        self.customize_measurement_page(title, layout)      # Customize the layout for the specific measurement type

        page.setLayout(layout)                              # Set the layout for the page
        return page

    def customize_measurement_page(self, title, layout):
        # Customize each measurement page based on the type
        if title == "DC Resistance":
            label = QLabel("DC Resistance Measurement")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Start/stop buttons
            start_button = QPushButton("Start")
            stop_button = QPushButton("Stop")
            start_button.setFont(QFont("Arial", 10))
            stop_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            stop_button.setStyleSheet("background-color: #f44336; color: white;")
            start_button.setFixedWidth(300)                                 # Limit the width of the start button
            stop_button.setFixedWidth(300)                                  # Limit the width of the stop button
            start_button.clicked.connect(lambda:self.start_dc_resistance_inputs())   
            button_layout = QVBoxLayout()                                   # Use QVBoxLayout to arrange buttons vertically
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)   # Add start button
            button_layout.addWidget(stop_button, alignment=Qt.AlignLeft)    # Add stop button below
            layout.addLayout(button_layout)

            self.result_label = QLabel("")
            self.result_label.setFont(QFont("Arial", 12))
            layout.addWidget(self.result_label)

        elif title == "Current-Voltage":
            label = QLabel("Current-Voltage (I-V) Measurement")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)
            
            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Dropdown for choosing sweep parameter
            sweep_dropdown = QComboBox()
            sweep_dropdown.addItems(["Sweep DC Voltage (V)", "Sweep Current (A)"])
            sweep_dropdown.setFont(QFont("Arial", 10))
            sweep_dropdown.setFixedWidth(300)                               # Set a fixed width for the dropdown
            sweep_dropdown.setFixedHeight(30)                               # Set a fixed width for the dropdown
            sweep_dropdown.setStyleSheet("background-color: white;")        # Set background color to white
            layout.addWidget(sweep_dropdown)

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                    # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting Value")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                    # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Ending Value")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                    # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Incremenet Value")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(300)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_current_voltage_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout)                                         # Add button layout under the title of the measurement type

            # **Add a Matplotlib canvas to display the plot**
            self.figure = Figure(figsize=(6, 4))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)

        elif title == "Capacitance-Voltage (2-p)":
            label = QLabel("Capacitance-Voltage Measurement (2-probe)")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting AC Offset Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Ending AC Offset Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Increment AC Offset Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(300)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_capacitance_voltage_2p_inputs())   
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout)                                         # Add button layout under the title of the measurement type

        elif title == "Impedance Spectroscopy (2-p)":
            label = QLabel("Impedance Spectroscopy (2-probe)")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Ending AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Increment AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Max Peak Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Min Peak Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(300)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_impedance_spectroscopy_2p_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

        elif title == "Transfer Characteristics":
            label = QLabel("Transfer Characteristics Measurement")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting Gate-Source Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Ending Gate-Source Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Increment Gate-Source Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(300)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_transfer_characteristics_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

        elif title == "Output Characteristics":
            label = QLabel("Output Characteristics Measurement")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting Drain-Source Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Ending Drain-Source Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Increment Drain-Source Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(300)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_output_characteristics_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

        elif title == "Capacitance-Voltage (3-p)":
            label = QLabel("Capacitance-Voltage Measurement (3-probe)")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting AC Offset Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Ending AC Offset Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Increment AC Offset Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(300)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_capacitance_voltage_3p_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout)  

        elif title == "Electrochemical":
            label = QLabel("Electrochemical Measurement")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Ending AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Increment AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Max Peak Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Min Peak Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(300)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_electrochemical_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

        elif title == "Probe Resistance":
            label = QLabel("Probe Resistance Measurement")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Start/stop buttons
            start_button = QPushButton("Start")
            stop_button = QPushButton("Stop")
            start_button.setFont(QFont("Arial", 10))
            stop_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            stop_button.setStyleSheet("background-color: #f44336; color: white;")
            start_button.setFixedWidth(300)                                 # Limit the width of the start button
            stop_button.setFixedWidth(300)                                  # Limit the width of the stop button
            start_button.clicked.connect(lambda:self.start_probe_resistance_inputs()) 
            button_layout = QVBoxLayout()                                   # Use QVBoxLayout to arrange buttons vertically
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)   # Add start button
            button_layout.addWidget(stop_button, alignment=Qt.AlignLeft)    # Add stop button below
            layout.addLayout(button_layout)

        elif title == "Low-Resistance":
            label = QLabel("Low-Resistance Measurement")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Start/stop buttons
            start_button = QPushButton("Start")
            stop_button = QPushButton("Stop")
            start_button.setFont(QFont("Arial", 10))
            stop_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            stop_button.setStyleSheet("background-color: #f44336; color: white;")
            start_button.setFixedWidth(300)                                 # Limit the width of the start button
            stop_button.setFixedWidth(300)                                  # Limit the width of the stop button
            start_button.clicked.connect(lambda:self.start_low_resistance_inputs()) 
            button_layout = QVBoxLayout()                                   # Use QVBoxLayout to arrange buttons vertically
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)   # Add start button
            button_layout.addWidget(stop_button, alignment=Qt.AlignLeft)    # Add stop button below
            layout.addLayout(button_layout)

        elif title == "Impedance Spectroscopy (4-p)":
            label = QLabel("Impedance Spectroscopy (4-probe)")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

            # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
            csv_radio = QRadioButton("Log data into a .CSV file")
            json_radio = QRadioButton("Log data into a .JSON file")
            csv_radio.setFont(QFont("Arial", 10))
            json_radio.setFont(QFont("Arial", 10))
            csv_radio.setChecked(True)                              # Default selection is CSV
            radio_layout = QVBoxLayout()                            # Create vertical selection/radio layout
            radio_layout.addWidget(csv_radio)                       # Add CSV button to the selection/radio layout
            radio_layout.addWidget(json_radio)                      # Add JSON button to the selection/radio layout
            layout.addLayout(radio_layout)                          # Add selection/radio layout under the title of the measurement type

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Ending AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Increment AC Frequency (Hz)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Max Peak Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                        # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Min Peak Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(300)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(300)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_impedance_spectroscopy_4p_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

        else:
            # Default layout for undefined measurement types
            label = QLabel(f"Page for {title}")
            label.setFont(QFont("Arial", 14, QFont.Bold))
            layout.addWidget(label)

    def create_error_bar(self):
        # Create a status bar for error checks
        error_bar = QWidget()
        status_layout = QHBoxLayout()
        error_bar.setStyleSheet("background-color: #b7a9a9;")
        error_bar.setFixedHeight(50)

        # Set margins and spacing
        status_layout.setContentsMargins(0, 0, 0, 0)

        # Indicators for different error statuses
        indicators = [
            ("Device Connection", True),
            ("Probe Configuration Match", True),
            ("Power Good", True)
        ]

        # Create and add each indicator to the status bar
        for label_text, status in indicators:
            indicator_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 10))
            icon_label = QLabel("✔")
            icon_label.setFont(QFont("Arial", 10))
            indicator_layout.addWidget(label)
            indicator_layout.addWidget(icon_label)
            indicator_layout.setAlignment(Qt.AlignCenter)
            indicator_widget = QWidget()
            indicator_widget.setLayout(indicator_layout)
            status_layout.addWidget(indicator_widget)

        # Set layout for the footer
        error_bar.setLayout(status_layout)
        return error_bar

    def create_probe_config_bar(self):
        # Create a bar to select probe configurations
        probe_bar = QWidget()
        probe_layout = QHBoxLayout()
        probe_bar.setStyleSheet("background-color: #b7a9a9;")

        # Supply and Measure options for the dropdowns
        supply_options = ["Choose Supply", "DC-Voltage Supply", "AC-Voltage Supply", "Current Supply", "Ground"]
        measure_options = ["Choose Measurement", "Voltage Measure", "Current Measure"]

        # Add dropdowns for all 4 probes
        for i in range(1, 5):
            # Create the left (supply) dropdown
            supply_dropdown = QComboBox()
            supply_dropdown.addItems(supply_options)  # Supply options dropdown
            supply_dropdown.setCurrentText("Choose Supply")  # Default text
            supply_dropdown.setFont(QFont("Arial", 8))
            supply_dropdown.setStyleSheet("background-color: #ffffff; padding: 3px;")

            # Create the right (measure) dropdown
            measure_dropdown = QComboBox()
            measure_dropdown.addItems(measure_options)  # Measure options dropdown
            measure_dropdown.setCurrentText("Choose Measurement")  # Default text
            measure_dropdown.setFont(QFont("Arial", 8))
            measure_dropdown.setStyleSheet("background-color: #ffffff; padding: 3px;")

            # Label for each probe
            probe_label = QLabel(f"Probe {i}")
            probe_label.setFont(QFont("Arial", 10, QFont.Bold))
            probe_label.setAlignment(Qt.AlignCenter)

            # Add the probe label and dropdowns to the layout
            probe_layout.addWidget(probe_label)
            probe_layout.addWidget(supply_dropdown)
            probe_layout.addWidget(measure_dropdown)

        # Set layout for the probe bar
        probe_bar.setLayout(probe_layout)
        return probe_bar

    def start_dc_resistance_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "DC Resistance":
                # Find all input fields in the page layout
                selected_probes = self.get_selected_probes(2)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_DC_RESISTANCE
                # write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                garbage = receive_samples(self.ser, 8192)
                while garbage is None:
                    garbage = receive_samples(self.ser, 8192)
                voltage = garbage[256]
                current = 3
                result = dc_resistance(voltage, current)
                # self.timer.start(100)  # Check every 100ms

    # def start_current_voltage_inputs(self):
    #     # Find the measurement page
    #     for index in range(self.page_widget.count()):
    #         page = self.page_widget.widget(index)
    #         if page.objectName() == "Current-Voltage":
    #             # Find all input fields in the page layout
    #             inputs = page.findChildren(QLineEdit)
    #             input_values = [input_field.text() for input_field in inputs]
    #             print(page.objectName(), "Input Values:", input_values)
    #             selected_probes = self.get_selected_probes(2)
    #             self.config_selected_probes(selected_probes,reg_map)
    #             reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
    #             reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
    #             reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
    #             reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
    #             reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
    #             reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_CURRENT_VOLTAGE
    #             # write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

    def start_current_voltage_inputs(self):
        """Starts the Current-Voltage measurement and embeds the graph in the GUI."""
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Current-Voltage":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)

                try:
                    # Determine if voltage or current is being swept
                    sweep_type = "voltage" if "Voltage" in inputs[0].text() else "current"
                    start = float(inputs[0].text())
                    end = float(inputs[1].text())
                    increment = float(inputs[2].text())

                    # Validate inputs
                    if increment <= 0 or end < start:
                        self.result_label.setText("Error: Invalid range or increment.")
                        return

                    # Configure measurement (Dummy Config)
                    selected_probes = self.get_selected_probes(2)
                    self.config_selected_probes(selected_probes, reg_map)

                    reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                    reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                    reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_CURRENT_VOLTAGE
                    # write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

                    # Generate sweep values
                    sweep_values = np.arange(start, end + increment, increment)

                    # **Generate synthetic y_values (e.g., linear relationship + noise)**
                    y_values = 2 * sweep_values + np.random.normal(0, 0.1, len(sweep_values))

                    # Update the GUI's Matplotlib plot
                    self.update_plot(sweep_values, y_values, sweep_type)

                    # Display confirmation message in the GUI
                    self.result_label.setText(f"{sweep_type.capitalize()} sweep completed!")

                except ValueError:
                    self.result_label.setText("Error: Please enter valid numerical inputs.")

    def start_capacitance_voltage_2p_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Capacitance-Voltage (2-p)":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(2)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_CAPACITANCE_VOLTAGE_2P
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def start_impedance_spectroscopy_2p_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Impedance Spectroscopy (2-p)":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(2)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_IMPEDANCE_SPECTROSCOPY_2P
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def start_transfer_characteristics_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Transfer Characteristics":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(3)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_3PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_TRANSFER_CHARACTERISTICS
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def start_output_characteristics_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Output Characteristics":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(3)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_3PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_OUTPUT_CHARACTERISTICS
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def start_capacitance_voltage_3p_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Capacitance-Voltage (3-p)":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(3)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_3PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_CAPACITANCE_VOLTAGE_3P
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def start_electrochemical_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Electrochemical":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(3)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_3PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_ELECTROCHEMICAL
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def start_probe_resistance_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Probe Resistance":
                selected_probes = self.get_selected_probes(4)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_4PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_PROBE_RESISTANCE
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def start_low_resistance_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Low-Resistance":
                selected_probes = self.get_selected_probes(4)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_4PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_LOW_RESISTANCE
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def start_impedance_spectroscopy_4p_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Impedance Spectroscopy (4-p)":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(4)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_4PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_IMPEDANCE_SPECTROSCOPY_4P
                # write_reg_DVC_MEASUREMENT_CONFIG(reg_map)

    def get_selected_probes(self, required_probes):
        """Fetch selected probes ensuring only one dropdown per probe is non-default 
        and the total selected probes match the required count."""
        
        # Ensure the probe configuration bar is correctly referenced
        probe_config_bar = self.probe_config_bar
        if not probe_config_bar:
            print("Error: Probe configuration bar not found!")
            return None

        probe_layout = probe_config_bar.layout()
        if not probe_layout:
            print("Error: Probe configuration layout not found!")
            return None

        selected_probes = {}

        for i in range(4):  # Iterate over the 4 probes
            probe_label = f"Probe {i + 1}"  # Manually defining probe labels
            
            # Extract dropdown widgets
            supply_dropdown = probe_layout.itemAt(i * 3 + 1).widget()  # Supply dropdown
            measure_dropdown = probe_layout.itemAt(i * 3 + 2).widget()  # Measurement dropdown

            if not supply_dropdown or not measure_dropdown:
                print(f"Error: Could not find dropdowns for {probe_label}")
                return None

            supply_value = supply_dropdown.currentText()
            measure_value = measure_dropdown.currentText()

            # Ensure only one dropdown per probe is selected
            # if supply_value != "Choose Supply" and measure_value != "Choose Measurement":
            #     print(f"Error: Both dropdowns are selected for {probe_label}! Only one is allowed.")
            #     return None
            if supply_value != "Choose Supply":
                selected_probes[probe_label] = supply_value
            if measure_value != "Choose Measurement":
                selected_probes[probe_label] = measure_value

        # Ensure the number of selected probes matches the required count
        if len(selected_probes) != required_probes:
            print(f"Error: {required_probes} probes required, but {len(selected_probes)} configured!")
            return None
        
        print("Selected Probes:", selected_probes)

        return selected_probes
    
    def config_selected_probes(self, selected_probes, reg_map):
        """Configures the selected probes by updating the Used_Probes register and setting probe-specific configurations."""

        # Mapping probe names to their corresponding register values
        probe_map = {
            "Probe 1": (GUI_PROBE_1_USED, "Probe_1_Config"),
            "Probe 2": (GUI_PROBE_2_USED, "Probe_2_Config"),
            "Probe 3": (GUI_PROBE_3_USED, "Probe_3_Config"),
            "Probe 4": (GUI_PROBE_4_USED, "Probe_4_Config"),
        }

        # Mapping configuration values for supply and measurement options
        probe_config_map = {
            "DC-Voltage Supply": (GUI_PROBE_SUPPLY_DCV, True),
            "AC-Voltage Supply": (GUI_PROBE_SUPPLY_ACV, True),
            "Current Supply": (GUI_PROBE_SUPPLY_CUR, True),
            "Ground": (GUI_PROBE_SUPPLY_GND, True),
            "Voltage Measure": (GUI_PROBE_MEASURE_VOL, False),
            "Current Measure": (GUI_PROBE_MEASURE_CUR, False),
        }

        # Initialize Used_Probes properly as a **list** (not a tuple)
        reg_map.DVC_PROBE_CONFIG.Used_Probes[0] = 0

        # Iterate over selected probes and configure them
        for probe, (used_flag, config_attr) in probe_map.items():
            if probe in selected_probes and selected_probes[probe] is not None:
                # Update Used_Probes
                reg_map.DVC_PROBE_CONFIG.Used_Probes[0] |= used_flag  # Perform bitwise OR update

                # Get the configuration value and shift requirement
                probe_value, should_shift = probe_config_map.get(selected_probes[probe], (None, None))
                if probe_value is not None:
                    # Correctly update the first index of Probe_X_Config
                    getattr(reg_map.DVC_PROBE_CONFIG, config_attr)[0] = probe_value << 3 if should_shift else probe_value

        print(f"Configured Used_Probes: {bin(reg_map.DVC_PROBE_CONFIG.Used_Probes[0])}")
        print(f"Configured Probes 1: {bin(reg_map.DVC_PROBE_CONFIG.Probe_1_Config[0])}")
        print(f"Configured Probes 2: {bin(reg_map.DVC_PROBE_CONFIG.Probe_2_Config[0])}")
        print(f"Configured Probes 3: {bin(reg_map.DVC_PROBE_CONFIG.Probe_3_Config[0])}")
        print(f"Configured Probes 4: {bin(reg_map.DVC_PROBE_CONFIG.Probe_4_Config[0])}")

    def check_serial_data(self):
        data = receive_value(self.ser)
        if data is not None:
            print(f"Received: {data}\n\r")
            self.timer.stop()  # Stop checking if we got 450

    def update_plot(self, x_values, y_values, sweep_type):
        """Updates the Matplotlib plot embedded in the GUI."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_values, y_values, marker='o', linestyle='-')
        ax.set_xlabel(f"{sweep_type.capitalize()} (swept)")
        ax.set_ylabel("Current" if sweep_type == "voltage" else "Voltage")
        ax.set_title("Current-Voltage Measurement")
        ax.grid(True)

        self.canvas.draw()  # Refresh the canvas with the updated plot
