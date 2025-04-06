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
from signal_reconstructor import *
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

        self.ser = init_ser_port('com4', 115200)   # open a serial connection on com8 with baud rate 115200
        
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
            start_button.setFixedWidth(350)                                 # Limit the width of the start button
            stop_button.setFixedWidth(350)                                  # Limit the width of the stop button
            start_button.clicked.connect(lambda:self.start_dc_resistance_inputs())   
            button_layout = QVBoxLayout()                                   # Use QVBoxLayout to arrange buttons vertically
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)   # Add start button
            # button_layout.addWidget(stop_button, alignment=Qt.AlignLeft)    # Add stop button below
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
            sweep_dropdown.addItems(["Sweep DC Voltage (V)", "Sweep Current (uA)"])
            sweep_dropdown.setFont(QFont("Arial", 10))
            sweep_dropdown.setFixedWidth(350)                               # Set a fixed width for the dropdown
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(350)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_current_voltage_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout)                                         # Add button layout under the title of the measurement type

            # **Add a Matplotlib canvas to display the plot**
            self.figure = Figure(figsize=(8, 6))
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(350)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_capacitance_voltage_2p_inputs())   
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout)                                         # Add button layout under the title of the measurement type
            
            # **Add a Matplotlib canvas to display the plot**
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)

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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(350)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_impedance_spectroscopy_2p_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)

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

            # Dropdowns
            gate_dropdown = QComboBox()
            gate_label = QLabel("Which probe is the Gate?")
            gate_label.setAlignment(Qt.AlignLeft)
            gate_label.setFont(QFont("Arial", 10, QFont.Bold))
            gate_dropdown.addItems(["Probe 1", "Probe 2", "Probe 3", "Probe 4"])
            gate_dropdown.setFont(QFont("Arial", 10))
            gate_dropdown.setFixedWidth(350)                               # Set a fixed width for the dropdown
            gate_dropdown.setFixedHeight(30)                               # Set a fixed width for the dropdown
            gate_dropdown.setStyleSheet("background-color: white;")        # Set background color to white
            layout.addWidget(gate_label)
            layout.addWidget(gate_dropdown)

            drain_dropdown = QComboBox()
            drain_label = QLabel("Which probe is the Drain?")
            drain_label.setAlignment(Qt.AlignLeft)
            drain_label.setFont(QFont("Arial", 10, QFont.Bold))
            drain_dropdown.addItems(["Probe 1", "Probe 2", "Probe 3", "Probe 4"])
            drain_dropdown.setFont(QFont("Arial", 10))
            drain_dropdown.setFixedWidth(350)                               # Set a fixed width for the dropdown
            drain_dropdown.setFixedHeight(30)                               # Set a fixed width for the dropdown
            drain_dropdown.setStyleSheet("background-color: white;")        # Set background color to white
            layout.addWidget(drain_label)
            layout.addWidget(drain_dropdown)

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Drain Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting Gate-Source Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(350)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_transfer_characteristics_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

            # **Add a Matplotlib canvas to display the plot**
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)

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

           # Dropdowns
            gate_dropdown = QComboBox()
            gate_label = QLabel("Which probe is the Gate?")
            gate_label.setAlignment(Qt.AlignLeft)
            gate_label.setFont(QFont("Arial", 10, QFont.Bold))
            gate_dropdown.addItems(["Probe 1", "Probe 2", "Probe 3", "Probe 4"])
            gate_dropdown.setFont(QFont("Arial", 10))
            gate_dropdown.setFixedWidth(350)                               # Set a fixed width for the dropdown
            gate_dropdown.setFixedHeight(30)                               # Set a fixed width for the dropdown
            gate_dropdown.setStyleSheet("background-color: white;")        # Set background color to white
            layout.addWidget(gate_label)
            layout.addWidget(gate_dropdown)

            drain_dropdown = QComboBox()
            drain_label = QLabel("Which probe is the Drain?")
            drain_label.setAlignment(Qt.AlignLeft)
            drain_label.setFont(QFont("Arial", 10, QFont.Bold))
            drain_dropdown.addItems(["Probe 1", "Probe 2", "Probe 3", "Probe 4"])
            drain_dropdown.setFont(QFont("Arial", 10))
            drain_dropdown.setFixedWidth(350)                               # Set a fixed width for the dropdown
            drain_dropdown.setFixedHeight(30)                               # Set a fixed width for the dropdown
            drain_dropdown.setStyleSheet("background-color: white;")        # Set background color to white
            layout.addWidget(drain_label)
            layout.addWidget(drain_dropdown)

            # Text box for entering measurement values
            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Gate Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)
            
            value_layout = QVBoxLayout()                            # Use QVBoxLayout to stack label and textbox vertically
            value_label = QLabel("Starting Drain-Source Voltage (V)")
            value_label.setAlignment(Qt.AlignLeft)
            value_label.setFont(QFont("Arial", 10, QFont.Bold))
            value_input = QLineEdit()
            value_input.setPlaceholderText("Enter value")
            value_input.setFont(QFont("Arial", 10))
            value_input.setStyleSheet("background-color: white;")
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(350)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_output_characteristics_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

            # **Add a Matplotlib canvas to display the plot**
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)

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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(350)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_capacitance_voltage_3p_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout)  

            # **Add a Matplotlib canvas to display the plot**
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)

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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(350)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_electrochemical_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 
            
            # **Add a Matplotlib canvas to display the plot**
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)

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
            start_button.setFixedWidth(350)                                 # Limit the width of the start button
            stop_button.setFixedWidth(350)                                  # Limit the width of the stop button
            start_button.clicked.connect(lambda:self.start_probe_resistance_inputs()) 
            button_layout = QVBoxLayout()                                   # Use QVBoxLayout to arrange buttons vertically
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)   # Add start button
            # button_layout.addWidget(stop_button, alignment=Qt.AlignLeft)    # Add stop button below
            layout.addLayout(button_layout)

            self.result_label = QLabel("")
            self.result_label.setFont(QFont("Arial", 12))
            layout.addWidget(self.result_label)

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
            start_button.setFixedWidth(350)                                 # Limit the width of the start button
            stop_button.setFixedWidth(350)                                  # Limit the width of the stop button
            start_button.clicked.connect(lambda:self.start_low_resistance_inputs()) 
            button_layout = QVBoxLayout()                                   # Use QVBoxLayout to arrange buttons vertically
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)   # Add start button
            # button_layout.addWidget(stop_button, alignment=Qt.AlignLeft)    # Add stop button below
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
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
            value_input.setFixedWidth(350)
            value_layout.addWidget(value_label)
            value_layout.addWidget(value_input)
            layout.addLayout(value_layout)

            # Start button
            start_button = QPushButton("Start Measurement")
            start_button.setFont(QFont("Arial", 10))
            start_button.setStyleSheet("background-color: #4CAF50; color: white;")
            start_button.setFixedWidth(350)                                         # Set a fixed width for the button
            start_button.clicked.connect(lambda:self.start_impedance_spectroscopy_4p_inputs()) 
            button_layout = QHBoxLayout()                                           # Create button layout
            button_layout.addWidget(start_button, alignment=Qt.AlignLeft)           # Add start button and align button to the left
            layout.addLayout(button_layout) 

            # **Add a Matplotlib canvas to display the plot**
            self.figure = Figure(figsize=(8, 6))
            self.canvas = FigureCanvas(self.figure)
            layout.addWidget(self.canvas)

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
            # ("Probe Configuration Match", True),
            ("Power Good", True)
        ]

        # Create and add each indicator to the status bar
        for label_text, status in indicators:
            indicator_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 10))
            icon_label = QLabel("✘") if self.ser is None else QLabel("✔")
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
        supply_options = ["Choose Supply", "DC-Voltage Supply", "AC-Voltage Supply", "DC-Current Supply", "AC-Current Supply" ,"Ground"]
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
                selected_probes = self.get_selected_probes(2)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_DC_RESISTANCE
                reg_map.DVC_2PM_DCRESISTANCE_1.Test_Current_Value[0] = 60
                write_reg_DVC_PROBE_CONFIG(self.ser, reg_map)
                write_reg_DVC_2PM_DCRESISTANCE_1(self.ser, reg_map)
                write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                time.sleep(0.1)
                read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                while reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0]:
                    read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                adc_samples = receive_samples(self.ser, 1,8192*2)
                while adc_samples is None:
                    adc_samples = receive_samples(self.ser, 1,8192*2)
                adc_samples = adc_samples/4096*5
                voltage = np.average(adc_samples)
                current = 0.058
                result = dc_resistance(voltage, current)
                self.result_label.setText(result)

    def start_current_voltage_inputs(self):
        """Starts the Current-Voltage measurement and embeds the graph in the GUI."""
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Current-Voltage":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                dropdown = page.findChildren(QComboBox)
                try:
                    # Determine if voltage or current is being swept
                    sweep_type = 1 if "Sweep DC Voltage (V)" in dropdown[0].currentText() else 2
                    start = float(inputs[0].text())
                    end = float(inputs[1].text())
                    increment = float(inputs[2].text())

                    # Validate inputs
                    if increment <= 0 or end < start:
                        self.result_label.setText("Error: Invalid range or increment.")
                        return

                    # Configure measurement (Dummy Config)
                    selected_probes = self.get_selected_probes(2)
                    self.config_selected_probes(selected_probes,reg_map)
                    reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                    reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                    reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                    reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                    reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                    reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_CURRENT_VOLTAGE
                    reg_map.DVC_2PM_CURRVOLT_1.Sweep_Param[0] = sweep_type
                    if sweep_type == 1:                    
                        reg_map.DVC_2PM_CURRVOLT_2.Starting_Param[0] = int(start*1000)
                        reg_map.DVC_2PM_CURRVOLT_3.Ending_Param[0] = int(end*1000)
                        reg_map.DVC_2PM_CURRVOLT_4.Increment_Param[0] = int(increment*1000)
                    else:
                        reg_map.DVC_2PM_CURRVOLT_2.Starting_Param[0] = int(start)
                        reg_map.DVC_2PM_CURRVOLT_3.Ending_Param[0] = int(end)
                        reg_map.DVC_2PM_CURRVOLT_4.Increment_Param[0] = int(increment)
                    write_reg_DVC_PROBE_CONFIG(self.ser, reg_map)
                    write_reg_DVC_2PM_CURRVOLT_1(self.ser, reg_map)
                    write_reg_DVC_2PM_CURRVOLT_2(self.ser, reg_map)
                    write_reg_DVC_2PM_CURRVOLT_3(self.ser, reg_map)
                    write_reg_DVC_2PM_CURRVOLT_4(self.ser, reg_map)
                    write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

                    # Generate sweep values
                    sweep_values = np.arange(start, end + increment, increment)

                    # **Generate synthetic y_values (e.g., linear relationship + noise)**
                    y_values = np.zeros(len(sweep_values))

                    adc_to_use = 1 if sweep_type == 2 else 3

                    for i in range(len(y_values)):
                        read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                        while reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0]:
                            read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                        adc_samples = receive_samples(self.ser, adc_to_use,8192*2)
                        while adc_samples is None:
                            adc_samples = receive_samples(self.ser, adc_to_use,8192*2)
                        if sweep_type == 1:
                            adc_samples = (adc_samples*1000000/(4096*500))
                        else:
                            adc_samples = adc_samples/4096*5   
                        adc_sample_avg = np.average(adc_samples)
                        y_values[i] = adc_sample_avg
                        print(f"rep {i} done")

                    # Update the GUI's Matplotlib plot
                    sweep_param = "voltage" if sweep_type == 1 else "current"
                    self.update_plot(sweep_values, y_values, sweep_param)

                    # Display confirmation message in the GUI
                    # self.result_label.setText(f"{sweep_param.capitalize()} sweep completed!")

                except ValueError:
                    self.result_label.setText("Error: Please enter valid numerical inputs.")

    def start_capacitance_voltage_2p_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Capacitance-Voltage (2-p)":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                volt_start = float(inputs[0].text())
                volt_end = float(inputs[1].text())
                volt_incr = float(inputs[2].text())
                selected_probes = self.get_selected_probes(2)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_CAPACITANCE_VOLTAGE_2P
                reg_map.DVC_2PM_CAPVOLT_1.Starting_Volt[0] = int(volt_start*1000)
                reg_map.DVC_2PM_CAPVOLT_2.Ending_Volt[0] = int(volt_end*1000)
                reg_map.DVC_2PM_CAPVOLT_3.Increment_Volt[0] = int(volt_incr*1000)
                write_reg_DVC_PROBE_CONFIG(self.ser, reg_map)
                write_reg_DVC_2PM_CAPVOLT_1(self.ser, reg_map)
                write_reg_DVC_2PM_CAPVOLT_2(self.ser, reg_map)
                write_reg_DVC_2PM_CAPVOLT_3(self.ser, reg_map)
                write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

                # Generate sweep values 
                sweep_values = np.arange(volt_start, volt_end + volt_incr, volt_incr)

                # **Generate synthetic y_values (e.g., linear relationship + noise)**
                y_values = np.zeros(len(sweep_values))

                for i in range(len(y_values)):
                    read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                    while reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0]:
                        read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                    adc_samples1 = receive_samples(self.ser, 3,8192*2)
                    while adc_samples1 is None:
                        adc_samples1 = receive_samples(self.ser, 3,8192*2)
                    val_time2, val_volt2 , fitted_amplitude2, fitted_frequency2, fitted_phase2, fitted_offset2 = reconstruct_signal((adc_samples1[:400]*1000000/(4096*500)))
                    self.update_plot_ac(val_time2,val_volt2)
                    print("Current")
                    print(f"fitted_amplitude : {fitted_amplitude2}")
                    print(f"fitted_frequency : {fitted_frequency2}")
                    print(f"fitted_phase : {fitted_phase2*180/3.14}")
                    print(f"fitted_offset : {fitted_offset2}")
                    print("----------------------------------------")
                    print(f"rep {i} done")

    def start_impedance_spectroscopy_2p_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Impedance Spectroscopy (2-p)":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                try:
                    start_freq = int(inputs[0].text())
                    end_freq = int(inputs[1].text())
                    increment_freq = int(inputs[2].text())
                    max_peak_volt = float(inputs[3].text())
                    min_peak_volt = float(inputs[4].text())
                    selected_probes = self.get_selected_probes(2)
                    self.config_selected_probes(selected_probes,reg_map)
                    start_freq_u14b,start_freq_l14b = self.encode_dds_freq(start_freq)
                    end_freq_u14b,end_freq_l14b = self.encode_dds_freq(end_freq)
                    incr_freq_u14b,incr_freq_l14b = self.encode_dds_freq(increment_freq)
                    reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                    reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                    reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                    reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                    reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                    reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_IMPEDANCE_SPECTROSCOPY_2P
                    reg_map.DVC_2PM_IMPSPEC_1.Starting_Freq_1[0] = start_freq_l14b
                    reg_map.DVC_2PM_IMPSPEC_2.Starting_Freq_2[0] = start_freq_u14b
                    reg_map.DVC_2PM_IMPSPEC_3.Ending_Freq_1[0] = end_freq_l14b
                    reg_map.DVC_2PM_IMPSPEC_4.Ending_Freq_2[0] = end_freq_u14b
                    reg_map.DVC_2PM_IMPSPEC_5.Increment_Freq_1[0] = incr_freq_l14b
                    reg_map.DVC_2PM_IMPSPEC_6.Increment_Freq_2[0] = incr_freq_u14b
                    reg_map.DVC_2PM_IMPSPEC_7.Max_Peak_Volt[0] = int(max_peak_volt*1000)
                    reg_map.DVC_2PM_IMPSPEC_8.Min_Peak_Volt[0] = int(min_peak_volt*1000)
                    write_reg_DVC_PROBE_CONFIG(self.ser, reg_map)
                    write_reg_DVC_2PM_IMPSPEC_1(self.ser, reg_map)
                    write_reg_DVC_2PM_IMPSPEC_2(self.ser, reg_map)
                    write_reg_DVC_2PM_IMPSPEC_3(self.ser, reg_map)
                    write_reg_DVC_2PM_IMPSPEC_4(self.ser, reg_map)
                    write_reg_DVC_2PM_IMPSPEC_5(self.ser, reg_map)
                    write_reg_DVC_2PM_IMPSPEC_6(self.ser, reg_map)
                    write_reg_DVC_2PM_IMPSPEC_7(self.ser, reg_map)
                    write_reg_DVC_2PM_IMPSPEC_8(self.ser, reg_map)
                    write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

                    # Generate sweep values
                    sweep_values = np.arange(start_freq, end_freq + increment_freq, increment_freq)

                    # **Generate synthetic y_values (e.g., linear relationship + noise)**
                    y_values = np.zeros(len(sweep_values))

                    for i in range(len(y_values)):
                        read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                        while reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0]:
                            read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                        adc_samples1 = receive_samples(self.ser, 1,8192*2)
                        while adc_samples1 is None:
                            adc_samples1 = receive_samples(self.ser, 1,8192*2)
                        adc_samples2 = receive_samples(self.ser, 3,8192*2)
                        while adc_samples2 is None:
                            adc_samples2 = receive_samples(self.ser, 3,8192*2)
                        val_time1, val_volt1 , fitted_amplitude1, fitted_frequency1, fitted_phase1, fitted_offset1 = reconstruct_signal(adc_samples1[:400]/4096*5)
                        val_time2, val_volt2 , fitted_amplitude2, fitted_frequency2, fitted_phase2, fitted_offset2 = reconstruct_signal((adc_samples2[:400]*1000000/(4096*500)))
                        self.update_plot_ac(val_time2,val_volt2)
                        print("Current")
                        print(f"fitted_amplitude : {fitted_amplitude2}")
                        print(f"fitted_frequency : {fitted_frequency2}")
                        print(f"fitted_phase : {fitted_phase2*180/3.14}")
                        print(f"fitted_offset : {fitted_offset2}")
                        print("----------------------------------------")
                        print("Voltage")
                        print(f"fitted_amplitude : {fitted_amplitude1}")
                        print(f"fitted_frequency : {fitted_frequency1}")
                        print(f"fitted_phase : {fitted_phase1*180/3.14}")
                        print(f"fitted_offset : {fitted_offset1}")

                        print(f"rep {i} done")

                except ValueError:
                    self.result_label.setText("Error: Please enter valid numerical inputs.")

    def start_transfer_characteristics_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Transfer Characteristics":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                dropdown = page.findChildren(QComboBox)
                drain_volt = float(inputs[0].text())
                gate_volt_start = float(inputs[1].text())
                gate_volt_end = float(inputs[2].text())
                gate_volt_incr = float(inputs[3].text())
                if "Probe 1" in dropdown[0].currentText():
                    gate_probe = 1
                elif "Probe 2" in dropdown[0].currentText():
                    gate_probe = 2
                elif "Probe 3" in dropdown[0].currentText():
                    gate_probe = 4
                elif "Probe 4" in dropdown[0].currentText():
                    gate_probe = 8
                if "Probe 1" in dropdown[1].currentText():
                    drain_probe = 1
                elif "Probe 2" in dropdown[1].currentText():
                    drain_probe = 2
                elif "Probe 3" in dropdown[1].currentText():
                    drain_probe = 4
                elif "Probe 4" in dropdown[1].currentText():
                    drain_probe = 8
                selected_probes = self.get_selected_probes(3)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_3PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_TRANSFER_CHARACTERISTICS
                reg_map.DVC_3PM_TRANSCHAR_1.Drain_Probe[0] = drain_probe
                reg_map.DVC_3PM_TRANSCHAR_1.Gate_Probe[0] = gate_probe
                reg_map.DVC_3PM_TRANSCHAR_2.Drain_Volt[0] = int(drain_volt*1000)
                reg_map.DVC_3PM_TRANSCHAR_3.Starting_Volt[0] = int(gate_volt_start*1000)
                reg_map.DVC_3PM_TRANSCHAR_4.Ending_Volt[0] = int(gate_volt_end*1000)
                reg_map.DVC_3PM_TRANSCHAR_5.Increment_Volt[0] = int(gate_volt_incr*1000)
                write_reg_DVC_PROBE_CONFIG(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_1(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_2(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_3(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_4(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_5(self.ser, reg_map)
                write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

                # Generate sweep values
                sweep_values = np.arange(gate_volt_start, gate_volt_end + gate_volt_incr, gate_volt_incr)

                # **Generate synthetic y_values (e.g., linear relationship + noise)**
                y_values = np.zeros(len(sweep_values))

                for i in range(len(y_values)):
                    read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                    while reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0]:
                        read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                    adc_samples = receive_samples(self.ser, 3,8192*2)
                    while adc_samples is None:
                        adc_samples = receive_samples(self.ser, 3,8192*2)
                    adc_samples = (adc_samples*1000000/(4096*50))
                    adc_sample_avg = np.average(adc_samples)
                    y_values[i] = adc_sample_avg
                    print(f"rep {i} done")

                self.update_plot(sweep_values, y_values, "voltage")                

    def start_output_characteristics_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Output Characteristics":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                dropdown = page.findChildren(QComboBox)
                gate_volt = float(inputs[0].text())
                drain_volt_start = float(inputs[1].text())
                drain_volt_end = float(inputs[2].text())
                drain_volt_incr = float(inputs[3].text())
                if "Probe 1" in dropdown[0].currentText():
                    gate_probe = 1
                elif "Probe 2" in dropdown[0].currentText():
                    gate_probe = 2
                elif "Probe 3" in dropdown[0].currentText():
                    gate_probe = 4
                elif "Probe 4" in dropdown[0].currentText():
                    gate_probe = 8
                if "Probe 1" in dropdown[1].currentText():
                    drain_probe = 1
                elif "Probe 2" in dropdown[1].currentText():
                    drain_probe = 2
                elif "Probe 3" in dropdown[1].currentText():
                    drain_probe = 4
                elif "Probe 4" in dropdown[1].currentText():
                    drain_probe = 8
                selected_probes = self.get_selected_probes(3)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_3PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_OUTPUT_CHARACTERISTICS
                reg_map.DVC_3PM_OUTCHAR_1.Drain_Probe[0] = drain_probe
                reg_map.DVC_3PM_OUTCHAR_1.Gate_Probe[0] = gate_probe
                reg_map.DVC_3PM_OUTCHAR_2.Gate_Volt[0] = int(gate_volt*1000)
                reg_map.DVC_3PM_OUTCHAR_3.Starting_Volt[0] = int(drain_volt_start*1000)
                reg_map.DVC_3PM_OUTCHAR_4.Ending_Volt[0] = int(drain_volt_end*1000)
                reg_map.DVC_3PM_OUTCHAR_5.Increment_Volt[0] = int(drain_volt_incr*1000)
                write_reg_DVC_PROBE_CONFIG(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_1(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_2(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_3(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_4(self.ser, reg_map)
                write_reg_DVC_3PM_TRANSCHAR_5(self.ser, reg_map)
                write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

                # Generate sweep values
                sweep_values = np.arange(drain_volt_start, drain_volt_end + drain_volt_incr, drain_volt_incr)

                # **Generate synthetic y_values (e.g., linear relationship + noise)**
                y_values = np.zeros(len(sweep_values))

                for i in range(len(y_values)):
                    read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                    while reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0]:
                        read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                    adc_samples = receive_samples(self.ser, 3,8192*2)
                    while adc_samples is None:
                        adc_samples = receive_samples(self.ser, 3,8192*2)
                    adc_samples = (adc_samples*1000000/(4096*50))
                    adc_sample_avg = np.average(adc_samples)
                    y_values[i] = adc_sample_avg
                    print(f"rep {i} done")

                self.update_plot(sweep_values, y_values, "voltage")     

    def start_capacitance_voltage_3p_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Capacitance-Voltage (3-p)":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(2)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_DC_RESISTANCE
                # write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

    def start_electrochemical_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Electrochemical":
                # Find all input fields in the page layout
                inputs = page.findChildren(QLineEdit)
                input_values = [input_field.text() for input_field in inputs]
                print(page.objectName(), "Input Values:", input_values)
                selected_probes = self.get_selected_probes(2)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_DC_RESISTANCE
                # write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

    def start_probe_resistance_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Probe Resistance":
                selected_probes = self.get_selected_probes(4)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_4PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_PROBE_RESISTANCE
                reg_map.DVC_4PM_PROBERESISTANCE_1.Test_Current_Value[0] = 60
                write_reg_DVC_PROBE_CONFIG(self.ser, reg_map)
                write_reg_DVC_4PM_PROBERESISTANCE_1(self.ser, reg_map)
                write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                time.sleep(0.1)
                read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                while reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0]:
                    read_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)
                adc_samples1 = receive_samples(self.ser, 1,8192*2)
                while adc_samples1 is None:
                    adc_samples1 = receive_samples(self.ser, 1,8192*2)
                adc_samples1 = adc_samples1/4096*5
                voltage1 = np.average(adc_samples1)
                adc_samples2 = receive_samples(self.ser, 2,8192*2)
                while adc_samples2 is None:
                    adc_samples2 = receive_samples(self.ser, 2,8192*2)
                adc_samples2 = adc_samples2/4096*5
                voltage2 = np.average(adc_samples1)
                current = 0.058
                result = dc_resistance(voltage1-voltage2, current)
                self.result_label.setText(result)

    def start_low_resistance_inputs(self):
        # Find the measurement page
        for index in range(self.page_widget.count()):
            page = self.page_widget.widget(index)
            if page.objectName() == "Low-Resistance":
                selected_probes = self.get_selected_probes(2)
                self.config_selected_probes(selected_probes,reg_map)
                reg_map.DVC_MEASUREMENT_CONFIG.Start_Measure[0] = 1
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_DC_RESISTANCE
                # write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

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
                reg_map.DVC_MEASUREMENT_CONFIG.Stop_Measure[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_In_Progress[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Valid_Measure_Config[0] = 0
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Probe_Config[0] = GUI_2PROBES
                reg_map.DVC_MEASUREMENT_CONFIG.Measure_Type_Config[0] = GUI_DC_RESISTANCE
                # write_reg_DVC_MEASUREMENT_CONFIG(self.ser, reg_map)

    def get_selected_probes(self, required_probes):
        """Fetch selected probes ensuring the total selected probes match the required count.
        Each probe can have both a supply and a measurement option selected.
        """

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

            # Add selections without overwriting
            probe_selections = []

            if supply_value != "Choose Supply":
                probe_selections.append(supply_value)

            if measure_value != "Choose Measurement":
                probe_selections.append(measure_value)

            if probe_selections:
                selected_probes[probe_label] = probe_selections

        # Ensure the number of selected probes matches the required count
        if len(selected_probes) != required_probes:
            print(f"Error: {required_probes} probes required, but {len(selected_probes)} configured!")
            return None

        print("Selected Probes:", selected_probes)

        return selected_probes
    
    def config_selected_probes(self, selected_probes, reg_map):
        """Configures the selected probes by updating the Used_Probes register 
        and setting probe-specific configurations with both supply and measurement options."""

        # Mapping probe names to their corresponding register values
        probe_map = {
            "Probe 1": (GUI_PROBE_1_USED, "Probe_1_Config"),
            "Probe 2": (GUI_PROBE_2_USED, "Probe_2_Config"),
            "Probe 3": (GUI_PROBE_3_USED, "Probe_3_Config"),
            "Probe 4": (GUI_PROBE_4_USED, "Probe_4_Config"),
        }

        # Mapping configuration values for supply (upper 3 bits) and measurement (lower 2 bits)
        probe_config_map = {
            "DC-Voltage Supply": (GUI_PROBE_SUPPLY_DCV, True),  # Upper 3 bits
            "AC-Voltage Supply": (GUI_PROBE_SUPPLY_ACV, True),
            "DC-Current Supply": (GUI_PROBE_SUPPLY_DCI, True),
            "AC-Current Supply": (GUI_PROBE_SUPPLY_ACI, True),
            "Ground": (GUI_PROBE_SUPPLY_GND, True),
            "Voltage Measure": (GUI_PROBE_MEASURE_VOL, False),  # Lower 2 bits
            "Current Measure": (GUI_PROBE_MEASURE_CUR, False),
        }

        # Initialize Used_Probes properly as a **list** (not a tuple)
        reg_map.DVC_PROBE_CONFIG.Used_Probes[0] = 0

        # Iterate over selected probes and configure them
        for probe, selections in selected_probes.items():
            if probe in probe_map:
                used_flag, config_attr = probe_map[probe]

                # Update Used_Probes
                reg_map.DVC_PROBE_CONFIG.Used_Probes[0] |= used_flag  # Perform bitwise OR update

                # Start with a 0-value config for this probe
                probe_config_value = 0

                for selection in selections:
                    # Get the configuration value and determine if it should be shifted
                    probe_value, should_shift = probe_config_map.get(selection, (None, None))
                    if probe_value is not None:
                        # Apply shifting for supply (upper 3 bits)
                        if should_shift:
                            probe_config_value |= (probe_value << 2)
                        else:  # Measurement (lower 2 bits)
                            probe_config_value |= probe_value

                # Update the probe's configuration register
                getattr(reg_map.DVC_PROBE_CONFIG, config_attr)[0] = probe_config_value

        # Debug prints
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
        ax.set_ylabel("Current (uA)" if sweep_type == "voltage" else "Voltage (V)")
        ax.set_title("Current-Voltage Measurement")
        ax.grid(True)

        self.canvas.draw()  # Refresh the canvas with the updated plot

    def update_plot_ac(self, x_values, y_values):
        """Updates the Matplotlib plot embedded in the GUI."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_values, y_values, 'r--', linewidth=2.0)
        ax.set_xlabel(f"time")
        ax.set_ylabel("Voltage")
        ax.set_title("AC Waveform Measurement")
        ax.grid(True)

        self.canvas.draw()  # Refresh the canvas with the updated plot

    def encode_dds_freq(self, freq):
        val = int(freq * (2**28) / 25000000)  # Compute val as an integer
        upper_14 = (val >> 14) & 0x3FFF  # Extract upper 14 bits
        lower_14 = val & 0x3FFF  # Extract lower 14 bits
        return upper_14, lower_14
