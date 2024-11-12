import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMainWindow,
    QPushButton, QScrollArea, QFrame
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orca Advanced Materials Inc. - NAME")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("background-color: #d8cfcf;")
        
        # Track currently selected option
        self.selected_option = None

        # Main layout
        main_layout = QHBoxLayout()

        # Sidebar layout
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        sidebar.setStyleSheet("background-color: #b7a9a9;")
        sidebar.setFixedWidth(250)

        # Title and subtitle in sidebar
        title_label = QLabel("Orca Advanced\nMaterial's Inc")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))

        subtitle_label = QLabel("NAME")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 10, QFont.Bold))
        subtitle_label.setStyleSheet("color: #000080;")

        sidebar_layout.addWidget(title_label)
        sidebar_layout.addWidget(subtitle_label)

        # Measurement expandable sections
        self.add_section(sidebar_layout, "2-probe Measurements", [
            "DC Resistance",
            "Current-Voltage",
            "Capacitance-Voltage",
            "Impedance Spectroscopy"
        ])
        self.add_section(sidebar_layout, "3-probe Measurements", [
            "Transfer Characteristics",
            "Output Characteristics",
            "Capacitance-Voltage",
            "Electrochemical"
        ])
        self.add_section(sidebar_layout, "4-probe Measurements", [
            "Probe Resistance",
            "Low-Resistance",
            "Impedance Spectroscopy"
        ])

        sidebar_layout.addStretch(1)
        sidebar.setLayout(sidebar_layout)

        # Main content area
        content_area = QWidget()
        content_layout = QVBoxLayout()
        content_area.setLayout(content_layout)

        # Bottom status bar
        status_bar = QWidget()
        status_layout = QHBoxLayout()
        status_bar.setStyleSheet("background-color: #b7a9a9;")

        # Status indicators
        indicators = [
            ("Device Connection", True),
            ("Probe Configuration Match", True),
            ("Power Good", True)
        ]

        for label_text, status in indicators:
            indicator_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 10))
            icon_label = QLabel("✔")                       # Placeholder checkmark
            icon_label.setFont(QFont("Arial", 10))
            indicator_layout.addWidget(label)
            indicator_layout.addWidget(icon_label)
            indicator_layout.setAlignment(Qt.AlignCenter)
            indicator_widget = QWidget()
            indicator_widget.setLayout(indicator_layout)
            status_layout.addWidget(indicator_widget)

        status_bar.setLayout(status_layout)

        # Add widgets to the main layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area)

        # Central widget for main layout
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addLayout(main_layout)
        central_layout.addWidget(status_bar)
        central_widget.setLayout(central_layout)

        # Set central widget
        self.setCentralWidget(central_widget)

    # Add an expandable section with the given title and options to the layout
    def add_section(self, layout, title, options):
        # Section title button
        button = QPushButton(title)
        button.setCheckable(True)
        button.setFont(QFont("Arial", 10))          # Match font size with status bar
        button.setStyleSheet("""
            background-color: #ffffff;
            padding: 8px;
            text-align: left;
            border: none;
        """)

        # Container for options that expands and collapses
        option_container = QWidget()
        option_layout = QVBoxLayout()
        option_container.setLayout(option_layout)
        option_container.setVisible(False)          # Start hidden

        # Add options as selectable labels
        for option_text in options:
            option_label = QLabel(option_text)
            option_label.setFont(QFont("Arial", 10))
            option_label.setStyleSheet("""
                padding: 5px;
                margin: 2px;
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
            """)
            option_label.setAlignment(Qt.AlignLeft)
            option_label.mousePressEvent = lambda event, label=option_label: self.highlight_selection(label)
            option_layout.addWidget(option_label)

        # Toggle option container visibility when the section title is clicked
        button.clicked.connect(lambda: option_container.setVisible(button.isChecked()))
        layout.addWidget(button)
        layout.addWidget(option_container)

    # Highlight the selected label by changing its background color and border (only one across all selections)
    def highlight_selection(self, label):
        # Reset the previously selected option
        if self.selected_option:
            self.selected_option.setStyleSheet("""
                padding: 5px;
                margin: 2px;
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
            """)

        # Highlight the new selected option
        label.setStyleSheet("""
            padding: 5px;
            margin: 2px;
            background-color: #cccccc;
            border: 2px solid black;
            border-radius: 4px;
        """)

        # Update the selected option
        self.selected_option = label

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())