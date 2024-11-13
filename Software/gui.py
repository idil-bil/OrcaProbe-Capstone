import sys
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow,
    QPushButton, QFrame, QStackedWidget, QRadioButton, QLineEdit, QButtonGroup, QComboBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Application window with basic settings
        self.setWindowTitle("NAME")                             # Title of the window
        self.setGeometry(100, 100, 800, 600)                    # Set position and size of the window
        self.setStyleSheet("background-color: #d8cfcf;")        # Set background color for the main screen
    
        # Sidebar for measurement type selection
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()                                              # Create a vertical layout for the sidebar
        sidebar.setStyleSheet("background-color: #b7a9a9;")                         # Set sidebar background color
        sidebar.setFixedWidth(300)                                                  # Set the width of the sidebar

        title_label = QLabel("Orca Advanced\nMaterial's Inc")                       # Sidebar title
        title_label.setAlignment(Qt.AlignRight)                                     # Align the title
        title_label.setFont(QFont("Arial", 12, QFont.Bold))                         # Set font style and size
        title_label.setStyleSheet("color: #000000;")                                # Set text color

        subtitle_label = QLabel("NAME")                                             # Sidebar subtitle
        subtitle_label.setAlignment(Qt.AlignRight)                                  # Align the title
        subtitle_label.setFont(QFont("Arial", 10, QFont.Bold))                      # Set font style and size
        subtitle_label.setStyleSheet("color: #000080;")                             # Set text color

        sidebar_layout.addWidget(title_label)                                       # Add the title to the sidebar
        sidebar_layout.addWidget(subtitle_label)                                    # Add the subtitle to the sidebar

        self.current_selected_measurement = None                                    # Initialize and track the currently selected measurement

        self.add_measurement_selection(sidebar_layout, "2-probe Measurements", [    # Add 2-probe measurement selections to the sidebar
            "DC Resistance",
            "Current-Voltage",
            "Capacitance-Voltage",
            "Impedance Spectroscopy"
        ])
        self.add_measurement_selection(sidebar_layout, "3-probe Measurements", [    # Add 3-probe measurement selections to the sidebar
            "Transfer Characteristics",
            "Output Characteristics",
            "Capacitance-Voltage",
            "Electrochemical"
        ])
        self.add_measurement_selection(sidebar_layout, "4-probe Measurements", [    # Add 4-probe measurement selections to the sidebar
            "Probe Resistance",
            "Low-Resistance",
            "Impedance Spectroscopy"
        ])

        sidebar_layout.addStretch(1)                                                # Add a spacer to push items to the top of the sidebar
        sidebar.setLayout(sidebar_layout)

        # Error bar at the bottom for showing the status of error checks
        error_bar = self.create_error_bar()

        # Probe configuration bar with dropdowns for selecting probe functionality
        probe_config_bar = self.create_probe_config_bar()

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
        central_layout.addWidget(probe_config_bar)  # Add probe configuration bar
        central_layout.addWidget(error_bar)         # Add status bar

        # Initialize page widget for the main window
        self.setCentralWidget(page_widget)
        page_widget.setLayout(central_layout)       # Add the central layout to all the measurement pages

        # Blank main page
        self.main_page = QWidget()
        self.page_widget.addWidget(self.main_page)

    def add_measurement_selection(self, layout, section_title, options):
        # For each measurement section (2-probe, 3-probe and 4-probe)
        button = QPushButton(section_title)             # Create a button
        button.setCheckable(True)                       # Make the buttons toggleable
        button.setFont(QFont("Arial", 10))              # Set the font for the buttons
        button.setStyleSheet("""                
            background-color: #ffffff;
            padding: 8px;
            text-align: left;
            border: none;
        """)                                            # Add styling for the buttons
        
        option_container = QWidget()                    # Create container for measurement types
        option_layout = QVBoxLayout()                   # Vertical layout to arrange measurement types
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
        # Create a new page for the selected measurement
        page = QWidget()
        layout = QVBoxLayout()

        # Title for the measurement type page
        title_label = QLabel(f"{title}")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label)

        # Buttons to select a data logging format (CSV or JSON), radio button used so one can be selected at a time           
        csv_radio = QRadioButton("Log data into a .CSV file")
        json_radio = QRadioButton("Log data into a .JSON file")
        csv_radio.setChecked(True)              # Default selection is CSV
        radio_layout = QHBoxLayout()            # Create Selection/radio layout
        radio_layout.addWidget(csv_radio)       # Add CSV button to the selection/radio layout
        radio_layout.addWidget(json_radio)      # Add JSON button to the selection/radio layout
        layout.addLayout(radio_layout)          # Add Selection/radio layout under the title of the measurement type

        # Start/stop buttons
        start_button = QPushButton("Start")
        stop_button = QPushButton("Stop")
        start_button.setStyleSheet("background-color: #4CAF50; color: white;")
        stop_button.setStyleSheet("background-color: #f44336; color: white;")
        button_layout = QHBoxLayout()           # Create button layout
        button_layout.addWidget(start_button)   # Add start button
        button_layout.addWidget(stop_button)    # Add stop button
        layout.addLayout(button_layout)         # Add button layout under the title of the measurement type

        # Text box for entering measurement values
        value_layout = QHBoxLayout()
        value_label = QLabel("VALUE")
        value_input = QLineEdit()
        value_input.setPlaceholderText("Enter value")
        unit_label = QLabel("Ohms")
        value_layout.addWidget(value_label)
        value_layout.addWidget(value_input)
        value_layout.addWidget(unit_label)
        layout.addLayout(value_layout)

        # Set layout for the page
        page.setLayout(layout)
        return page

    def create_error_bar(self):
        # Create a status bar for error checks
        error_bar = QWidget()
        status_layout = QHBoxLayout()
        error_bar.setStyleSheet("background-color: #b7a9a9;")

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
        probe_options = ["Off", "DC-Voltage Supply", "AC-Voltage Supply", "Current Supply", "Voltage Measure", "Current Measure"]

        # Add dropdowns for all 4 probes
        for i in range(1, 5):
            probe_dropdown = QComboBox()
            probe_dropdown.addItems(probe_options)          # Create dropdown for each probe with all the functionalities possible
            probe_dropdown.setCurrentText("Off")            # Default selection is "Off"
            probe_dropdown.setFont(QFont("Arial", 10))
            probe_dropdown.setStyleSheet("background-color: #ffffff; padding: 3px;")
            
            probe_label = QLabel(f"Probe {i}")
            probe_label.setFont(QFont("Arial", 10))

            probe_layout.addWidget(probe_label)
            probe_layout.addWidget(probe_dropdown)

        # Set layout for the footer
        probe_bar.setLayout(probe_layout)
        return probe_bar

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()                   # Show the main window
sys.exit(app.exec_())           # Start the application's event loop