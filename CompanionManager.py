#CompanionManager.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout, QFrame,
                              QRadioButton, QButtonGroup, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class CompanionManager(QWidget):
    # TODO find a way to build out rows with the same companion to be placed in a row together. 
    # TODO fix an issue where only the first instance of a companion will be displayed.
    # TODO the files need to go somewhere. Add in a feature so that dropped files can be stored.

    def __init__(self, parent=None):
        super(CompanionManager, self).__init__(parent)
        self.right_layout = QVBoxLayout()
        self.setLayout(self.right_layout)
        self.setAcceptDrops(True)  # Enable drag-and-drop for this widget

        # self.uni_part_group_buttons = {}
        

    # Handles creation of Companion Buttons to the right layout
    def create_companion_buttons(self, companions):
        # Clear existing companion buttons
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)  # Remove widget from the layout
                widget.deleteLater()    # Schedule it for deletion
        companion_buttons = {}
        for companion, type_data in companions.items():
            # Create a frame to contain the companion button and radio buttons
            frame = QFrame()
            frame_layout = QVBoxLayout()
            frame.setLayout(frame_layout)

            companion_button = QPushButton(companion)
            companion_button.setStyleSheet("background-color: #9C9C9C; color: black;")
            companion_button.setEnabled(True)
            companion_button.setVisible(True)
            # Add button widget to layout
            frame_layout.addWidget(companion_button)
            # self.right_layout.addWidget(companion_button)
            # Add frame to the main layout
            self.right_layout.addWidget(frame)
            
            # Store the frame and its type data
            companion_buttons[frame] = type_data
            # companion_buttons[companion_button] = type_data
        print("Companion Buttons: ", companion_buttons)
        
        return companion_buttons

    # Handles creation of radio buttons below each associated companion button
    def add_radio_buttons(self, companion_buttons):
        for frame, type_data in companion_buttons.items():
            button_group = QButtonGroup(self)  # Group radio buttons together
            
            for entry in type_data:
                radio_button = QRadioButton(entry['type-variable'])
                button_group.addButton(radio_button)

                # Add radio button to the frame layout
                hbox_layout = QHBoxLayout()
                hbox_layout.addWidget(radio_button)
                frame.layout().addLayout(hbox_layout)
        
        
    # Handles creation of file  image file drop widgets
    def create_file_input_widgets(self, companion_data):

        # Create drop areas for each file input
        for companion_name in companion_data.keys():
            # Create a label for each file input
            label = QLabel(companion_name)
            self.layout.addWidget(label)
            
            # Create a drop area label
            drop_area = QLabel("Drop image here")
            drop_area.setStyleSheet("border: 2px dashed gray; padding: 10px;")
            drop_area.setAlignment(Qt.AlignCenter)
            drop_area.setFixedSize(200, 200)  # Adjust size as needed
            drop_area.setProperty("companion_name", companion_name)
            drop_area.installEventFilter(self)
            self.layout.addWidget(drop_area)


    def create_type_variable_widgets(self, uni_centers_list):

        print("\n Creating UNI Center Widgets\n")
        group_box = QButtonGroup(self)
        for center in uni_centers_list:
            print("UNI Center: ", center)
            radio_button = QRadioButton(center)
            group_box.addButton(radio_button)
            self.layout.addWidget(radio_button)

    def eventFilter(self, source, event):
        if event.type() == event.DragEnter and source.property("companion_name"):
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
        elif event.type() == event.Drop and source.property("companion_name"):
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                if urls:
                    file_path = urls[0].toLocalFile()
                    self.handle_dropped_file(source, file_path)
                event.acceptProposedAction()
        return super(CompanionManager, self).eventFilter(source, event)


    # Handles proper storage of dropped image file
    def handle_dropped_file(self, drop_area, file_path):
        companion_name = drop_area.property("companion_name")
        # Handle the dropped file (e.g., show it in the label)
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            drop_area.setPixmap(pixmap.scaled(drop_area.size(), Qt.AspectRatioMode.KeepAspectRatio))
        print(f"File dropped for {companion_name}: {file_path}")
        # Additional handling, such as storing the file path or uploading, can be done here
        # TODO finish building logic to actually store dropped image files
