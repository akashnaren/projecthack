import sys
from Application import Application
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QComboBox, QWidget, QSplitter, QFrame, QTreeWidget, QSizePolicy, QTreeWidgetItem, QListWidget, QPlainTextEdit)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal, QObject


class Worker(QObject):
    taskCompleted = pyqtSignal(object)  # Modify the signal to include data

    def __init__(self, application, start, schedule):
        super().__init__()
        self.application = application
        self.start = start
        self.schedule = schedule

    def run(self):
        result = self.application.optimize_schedule(self.start, self.schedule)  # Get the result from the backend function
        self.taskCompleted.emit(result)  

class RightSideWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing

        # QWebEngineView to load and display the map
        self.map_view = QWebEngineView()
        self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy to expanding
        self.map_view.setStyleSheet("background-color: transparent;")  # Set background color to transparent

        # Assuming your Flask app is running on localhost at port 5000
        self.map_view.load(QUrl("http://127.0.0.1:5000"))
        layout.addWidget(self.map_view)


class LeftSideWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Locations Section
        locations_label = QLabel('LOCATIONS', self)
        layout.addWidget(locations_label)

        self.location_combobox = QComboBox(self)


        self.location_options = ['Cafe Ventanas', 'Canyon View Center', 
                                  'Center Hall', 'Cognitive Science Building',
                  'CSE Building', 'Eleanor Roosevelt College', 'Eighth College',
                  'Franklin Antonio Hall', 'Food(any)','Jacobs School',
                  'Galbraith Hall', 'Geisel', 'Gym(any)','Main Gym', 'Mandeville Auditorium',
                  'Marshall College', 'Muir College',
                  'Ocean View Terrace', 'Pepper Canyon Hall',
                  'Pines', 'Price Center', 'Rady School', 
                  'Revelle College', 'RIMAC',
                  'Seventh College',
                  'Sixth College',
                  'Social Sciences Building',
                  'Study(any)',
                   'SuperComputer Center', 'Warren College', 'Warren Lecture Hall', 'York Hall',
                     '64 Degrees']


        self.location_combobox.addItems(self.location_options)
        layout.addWidget(self.location_combobox)

        # Location Table
        self.location_table = QTreeWidget(self)
        self.location_table.setHeaderLabels(['YOUR SCHEDULE'])
        layout.addWidget(self.location_table)

        # Start Section
        start_layout = QHBoxLayout()
        start_label = QLabel('Start: ')
        start_layout.addWidget(start_label)

        self.start_location_box = QComboBox(self)

        start_options = ['Cafe Ventanas', 'Canyon View Center', 
                                  'Center Hall', 'Cognitive Science Building',
                  'CSE Building', 'Eleanor Roosevelt College', 'Eighth College',
                  'Franklin Antonio Hall', 'Jacobs School',
                  'Galbraith Hall', 'Geisel', 'Main Gym', 'Mandeville Auditorium',
                  'Marshall College', 'Muir College',
                  'Ocean View Terrace', 'Pepper Canyon Hall',
                  'Pines', 'Price Center', 'Rady School', 
                  'Revelle College', 'RIMAC',
                  'Seventh College',
                  'Sixth College',
                  'Social Sciences Building',
                   'SuperComputer Center', 'Warren College', 'Warren Lecture Hall', 'York Hall',
                     '64 Degrees']

        self.start_location_box.addItems(start_options)

        start_layout.addWidget(self.start_location_box)

        self.start_location_box.currentIndexChanged.connect(self.updateMap)

        layout.addLayout(start_layout)

        # Button Panel
        self.button_panel = ButtonPanel(self)
        layout.addWidget(self.button_panel)

    def updateMap(self, index):
        address = self.start_location_box.currentText()
        self.main_window.updateMapCenter(address)



class ButtonPanel(QWidget):
    def __init__(self, left_widget):
        super().__init__()
        self.left_widget = left_widget
        self.initUI()

        self.application = Application()

        self.start = ''
        self.schedule = []

    def initUI(self):

        main_layout = QVBoxLayout(self)  # Create a vertical layout

        # Create the QPlainTextEdit widget
        self.text_edit = QPlainTextEdit(self)
        self.text_edit.setPlaceholderText("Enter text here...")  # Optional placeholder text
        main_layout.addWidget(self.text_edit)  # Add the text edit widget to the main layout

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton('Add', self)
        self.delete_button = QPushButton('Delete', self)
        self.clear_button = QPushButton('Clear', self)
        self.run_button = QPushButton('Run', self)

        # Add buttons to the button layout
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.run_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Connect button signals to slots
        self.add_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_row)
        self.clear_button.clicked.connect(self.clear_table)
        self.run_button.clicked.connect(self.run_algorithm)

        # Set the main layout for the widget
        self.setLayout(main_layout)

        '''
        layout = QHBoxLayout(self)

        self.add_button = QPushButton('Add', self)
        self.delete_button = QPushButton('Delete', self)
        self.clear_button = QPushButton('Clear', self)
        self.run_button = QPushButton('Run', self)

        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.run_button)

        self.add_button.clicked.connect(self.add_row)
        self.delete_button.clicked.connect(self.delete_row)
        self.clear_button.clicked.connect(self.clear_table)
        self.run_button.clicked.connect(self.run_algorithm)
        '''

    def add_row(self):
        selected_location = self.left_widget.location_combobox.currentText()
        if selected_location:  # Ensure a location is selected
            QTreeWidgetItem(self.left_widget.location_table, [selected_location])

        self.schedule.append(selected_location)
        print(f"self.schedule : {self.schedule}")

    def delete_row(self):
        selected_item = self.left_widget.location_table.currentItem()

        selected_text = selected_item.text(0)

        print(f"selected_item : {selected_item}")
        if selected_item:
            index = self.left_widget.location_table.indexOfTopLevelItem(selected_item)
            self.left_widget.location_table.takeTopLevelItem(index)

        self.schedule.remove(selected_text)
        print(f"self.schedule : {self.schedule}")

    def clear_table(self):
        self.left_widget.location_table.clear()

        self.schedule.clear()
        print(f"self.schedule : {self.schedule}")

    def run_algorithm(self):
        if not self.schedule:
            print(f"Please add items to your schedule")
            return

        self.start = self.left_widget.start_location_box.currentText()
        print(f"self.start : |{self.start}|")

        # Create the worker and thread
        self.worker = Worker(self.application, self.start, self.schedule)
        self.thread = QThread()

        # Move the worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.taskCompleted.connect(self.onTaskCompleted)  # Connect the custom signal to a slot
        self.thread.finished.connect(self.thread.deleteLater)

        # Start the thread
        self.thread.start()

    def onTaskCompleted(self, result):
        # This method will be called when the taskCompleted signal is emitted
        # 'result' is the data passed from the backend
        print("Thread task completed!")
        print("Result:", result)

        locations = result[1]

        formatted_list = "\n".join([f"- {location}" for location in locations])

        self.text_edit.setPlainText(formatted_list)
        
        # You can update the frontend with the result here



    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GUI with Splitter and Web Map')
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QHBoxLayout(self.central_widget)

        self.splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(self.splitter)

        self.left_widget = LeftSideWidget(self)
        self.splitter.addWidget(self.left_widget)

        # Correctly instantiate RightSideWidget without additional arguments
        self.right_widget = RightSideWidget()
        self.splitter.addWidget(self.right_widget)


    def updateMapCenter(self, address):
        # Implement map update functionality
        pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
