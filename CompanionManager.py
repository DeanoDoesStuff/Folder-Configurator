#CompanionManager.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class CompanionManager(QWidget):
    # CLASS todos
    # TODO find a way to build out rows with the same companion to be placed in a row together. 
    # TODO fix an issue where only the first instance of a companion will be displayed.
    # TODO the files need to go somewhere. Add in a feature so that dropped files can be stored.

    def __init__(self, parent=None):
        super(CompanionManager, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setAcceptDrops(True)  # Enable drag-and-drop for this widget

    def create_file_input_widgets(self, companion_data):
        # Clear existing widgets
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

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

    def handle_dropped_file(self, drop_area, file_path):
        companion_name = drop_area.property("companion_name")
        # Handle the dropped file (e.g., show it in the label)
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            drop_area.setPixmap(pixmap.scaled(drop_area.size(), Qt.AspectRatioMode.KeepAspectRatio))
        print(f"File dropped for {companion_name}: {file_path}")

        # Additional handling, such as storing the file path or uploading, can be done here

