from gui import *

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()                   # Show the main window
sys.exit(app.exec_())           # Start the application's event loop