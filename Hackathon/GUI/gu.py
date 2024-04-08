import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QComboBox, QWidget, QSplitter, QFrame)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl

class LeftSideWidget(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Store reference to main window
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        # Schedule section
        schedule_layout = QVBoxLayout()
        schedule_label = QLabel('SCHEDULE')
        schedule_layout.addWidget(schedule_label)
        main_layout.addLayout(schedule_layout)

        # Start section
        start_layout = QHBoxLayout()
        start_label = QLabel('Start: ')
        self.location_box = QComboBox()
        self.location_box.addItems(["Location 1", "Location 2"])
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.location_box)
        main_layout.addLayout(start_layout)

        # Button panel
        self.button_panel = ButtonPanel()
        main_layout.addWidget(self.button_panel)

        # Connect location box changes to update the map
        self.location_box.currentTextChanged.connect(self.updateMap)

    def updateMap(self, address):
        # Send the address to the main window to update the map
        self.main_window.right_widget.updateMapCenter(address)

class RightSideWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # QWebEngineView to load and display the map
        self.map_view = QWebEngineView()
        
        # Assuming your Flask app is running on localhost at port 5000
        self.map_view.load(QUrl("http://127.0.0.1:5000"))
        layout.addWidget(self.map_view)

    def updateMapCenter(self, address):
        # JavaScript code to update the map center
        js_code = f"""
        updateMapWithAddress("{address}");
        """
        self.map_view.page().runJavaScript(js_code)

class ButtonPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        self.delete_button = QPushButton('Delete')
        self.add_button = QPushButton('+')
        self.clear_button = QPushButton('Clear')
        self.find_button = QPushButton('Find')
        self.refresh_button = QPushButton('Refresh')

        layout.addWidget(self.delete_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.find_button)
        layout.addWidget(self.refresh_button)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Splitter to adjust the left and right sides
        self.splitter = QSplitter(Qt.Horizontal, self)

        self.left_widget = LeftSideWidget(self)
        self.right_widget = RightSideWidget()

        self.splitter.addWidget(self.left_widget)
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([300, 300])

        self.setCentralWidget(self.splitter)

        self.setWindowTitle('GUI with Splitter and Web Map')
        self.setGeometry(300, 300, 1000, 600)
        self.show()

def main():
    app = QApplication(sys.argv)
    # Add the following line to integrate PyQtWebEngine
    QWebEngineView()
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
