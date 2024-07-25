import os
from collections import defaultdict
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QCheckBox, QLineEdit, QPushButton, 
                             QMessageBox, QSplitter, QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from FolderManager import FolderManager
from FolderTree import FolderTree
from SkuBuilder import SkuBuilder
from Utility import load_series_data

class HomeScreen(QMainWindow):
    def __init__(self, root_dir, folder_type, parent=None):
        super().__init__()

        self.root_dir = root_dir
        self.folder_type = folder_type
        self.parent = parent
        self.sku_builder = SkuBuilder()
        self.setWindowTitle("Folder Manager")
        self.setGeometry(100, 100, 1920, 1080)

        # Set window icon
        self.setWindowIcon(QIcon('C://DevProjects/Assets/Born to Build Circular Emblem.ico'))

        # Folder Manager
        self.folder_manager = FolderManager(self.root_dir)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Splitter to divide the main window
        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)

        # Left Widget (Folder Tree)
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)

        # Tree Widget
        self.tree_widget = FolderTree(self.root_dir, self.folder_manager, self)
        self.tree_widget.itemClicked.connect(self.handle_tree_item_click)
        self.tree_widget.empty_space_clicked.connect(self.reset_folder_type) # Connect to empty space signal 
        self.left_layout.addWidget(self.tree_widget)
        
        # Input for a new folder
        self.new_folder_input = QLineEdit()
        self.new_folder_input.setPlaceholderText(f"Enter new {self.folder_type}")
        self.left_layout.addWidget(self.new_folder_input)

        # Button for creating a new folder
        self.create_folder_button = QPushButton("Create Folder") # TODO update the button text for folder_type
        self.create_folder_button.clicked.connect(self.create_new_folder)
        self.create_folder_button.setStyleSheet("""
            QPushButton {
                background-color: #2E982B;
                color: white;
            }
            QPushButton:disabled {
                background-color: grey;
                color: white;
            }
        """)
        self.left_layout.addWidget(self.create_folder_button)

        # Button for deleting a selected folder
        self.delete_folder_button = QPushButton("Delete Folder")
        self.delete_folder_button.clicked.connect(self.delete_folder)
        self.delete_folder_button.setStyleSheet("background-color: #C63F3F; color: white;")
        self.left_layout.addWidget(self.delete_folder_button)

        # Add left widget to splitter
        self.splitter.addWidget(self.left_widget)
        
        # Middle Widget for Series options
        self.middle_widget = QWidget()
        self.middle_layout = QVBoxLayout()
        self.middle_widget.setLayout(self.middle_layout)
        self.splitter.addWidget(self.middle_widget)

        # Right Widget (Nothing here yet, but for testing)
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_widget.setLayout(self.right_layout)

        # Example of adding a button to the right widget
        self.example_button = QPushButton("Example Button")
        self.right_layout.addWidget(self.example_button)

        # Add a QLabel for displaying the SKU
        self.sku_label = QLabel("Current SKU: ")
        self.right_layout.addWidget(self.sku_label)

        # Add right widget to splitter
        self.splitter.addWidget(self.right_widget)

        # Create Series Widget
        self.series_widget = QWidget()
        self.series_layout = QVBoxLayout()
        self.series_widget.setLayout(self.series_layout)
        self.splitter.addWidget(self.series_widget)

        # Set initial sizes for the splitter (optional)
        self.splitter.setSizes([200, 400, 600])  # Set the initial size for the left and right widgets

        # Initialize folder type and button state
        self.update_folder_type(self.tree_widget.currentItem())

        # Load and display series buttons
        self.series_data = load_series_data('Configs/SERIES_CONFIG.csv')  # Updated with the actual path to the CSV file
        self.load_series_buttons()  # Load series buttons

        # Track the active series button
        self.active_series_button = None

    def handle_tree_item_click(self, item):
        self.update_folder_type(item)
        depth = self.tree_widget.get_item_depth(item)
        if depth == 3: # Year is selected
            self.enable_series_buttons(True)
        else:
            self.enable_series_buttons(False)

    def enable_series_buttons(self, enable):
        for i in range(self.middle_layout.count()):
            widget = self.middle_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setEnabled(enable)

    def update_folder_type(self, item):
        current_sku = ""
        if item:
            depth = self.tree_widget.get_item_depth(item)

            # Call SkuBuilder for the given depth
            make_id, model_id, year_id = self.sku_builder.process_depth(item, depth)
            if depth == 0: # Nothing is selected SKU is NULL
                self.folder_type = " Make"
            elif depth == 1:
                self.folder_type = " Model"
                # Make or deeper has been selected Make ID extracted
                current_sku = make_id
            elif depth == 2:
                self.folder_type = " Year"
                # Model or deeper has been selected Make and Model ID extracted
                current_sku = make_id + model_id
            elif depth == 3:
                self.folder_type = " SERIES"
                # Year has been selected, all MMY SKU ID's have been extracted
                current_sku = make_id + model_id + year_id
            else:
                self.folder_type = " None"
                current_sku = self.make_id # Base SKU
            # Update UI elements
            if depth < 3:
                # Set placeholder text if make or model depth selected
                self.new_folder_input.setPlaceholderText(f"Enter new{self.folder_type}")
            else:
                # Empty Text if year is selected
                self.new_folder_input.setPlaceholderText("")
            self.create_folder_button.setEnabled(self.folder_type != " None")
            self.create_folder_button.setEnabled(self.folder_type != " SERIES")
            # Update SKU label
            self.update_sku_label(current_sku)

    def create_new_folder(self):
        new_folder_name = self.new_folder_input.text().strip()
        if new_folder_name:
            selected_item = self.tree_widget.currentItem()
            if selected_item:
                parent_path = self.tree_widget.get_item_path(selected_item)
            else:
                parent_path = self.root_dir
            
            new_folder_path = os.path.join(parent_path, new_folder_name)
            if self.folder_manager.create_folder(new_folder_path):
                self.new_folder_input.clear()
                QMessageBox.information(self, "Success", f"Folder '{new_folder_name}' created successfully.")
                self.tree_widget.refresh_tree()
            else:
                QMessageBox.information(self, "Warning", f"Folder '{new_folder_name}' already exists.")

    def delete_folder(self):
        selected_item = self.tree_widget.currentItem()
        if selected_item:
            folder_path = self.tree_widget.get_item_path(selected_item)
            reply = QMessageBox.question(self, "Delete Folder", f"Are you sure you want to delete '{selected_item.text(0)}'?", 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.folder_manager.delete_folder(folder_path):
                    QMessageBox.information(self, "Success", f"Folder '{selected_item.text(0)}' deleted successfully.")
                    self.tree_widget.refresh_tree()
                else:
                    QMessageBox.warning(self, "Error", f"Failed to delete folder '{selected_item.text(0)}'. It might not be empty.")

    def update_sku_label(self, sku):
        self.sku_label.setText(f"Current SKU: {sku}")

    def reset_folder_type(self):
        self.update_folder_type(None)
    
    def load_series_buttons(self):
        for series in self.series_data:
            button = QPushButton(series)
            button.clicked.connect(self.handle_series_button_click)
            self.middle_layout.addWidget(button)

    def handle_series_button_click(self):
        sender = self.sender()
        series = sender.text()

        # Clear any existing checkboxes
        for i in reversed(range(self.middle_layout.count())):
            widget = self.middle_layout.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                self.middle_layout.removeWidget(widget)
                widget.deleteLater()

        # Add new checkboxes based on unique CSV data for the selected series
        if series in self.series_data:
            for category, values in self.series_data[series].items():
                for value in values:
                    checkbox = QCheckBox(f"{category}: {value}")
                    self.middle_layout.addWidget(checkbox)
