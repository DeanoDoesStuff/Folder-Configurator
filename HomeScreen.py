import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, 
                            QMessageBox, QSplitter, QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from FolderManager import FolderManager
from FolderTree import FolderTree
from SkuBuilder import SkuBuilder
from SeriesManager import SeriesManager

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
        self.tree_widget.empty_space_clicked.connect(self.reset_folder_type)
        self.left_layout.addWidget(self.tree_widget)

        # Input for a new folder
        self.new_folder_input = QLineEdit()
        self.new_folder_input.setPlaceholderText(f"Enter new {self.folder_type}")
        self.left_layout.addWidget(self.new_folder_input)

        # Button for creating a new folder
        self.create_folder_button = QPushButton("Create Folder")
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

        # Create Series Manager
        self.series_manager = SeriesManager(self.middle_widget, self.folder_manager, self.tree_widget, self.sku_builder, self.update_sku_label, self.enable_series_buttons)

        # Set initial sizes for the splitter (optional)
        self.splitter.setSizes([300, 500, 500])

    def handle_tree_item_click(self, item):
        self.series_manager.update_series_button_states(item)

    def reset_folder_type(self):
        self.new_folder_input.clear()
        self.create_folder_button.setEnabled(True)

    def create_new_folder(self):
        folder_name = self.new_folder_input.text().strip()
        if folder_name:
            selected_item = self.tree_widget.currentItem()
            if not selected_item:
                QMessageBox.warning(self, "Error", "Please select a folder to create a new folder inside.")
                return
            
            parent_path = self.tree_widget.get_item_path(selected_item)
            new_folder_path = os.path.join(parent_path, folder_name)
            if not os.path.exists(new_folder_path):
                if self.folder_manager.create_folder(new_folder_path):
                    QMessageBox.information(self, "Success", f"Folder '{folder_name}' created successfully.")
                    self.tree_widget.expandItem(selected_item)
                else:
                    QMessageBox.warning(self, "Error", f"Failed to create folder '{folder_name}'.")
            else:
                QMessageBox.warning(self, "Error", "Folder already exists.")

    def delete_folder(self):
        selected_item = self.tree_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Please select a folder to delete.")
            return
        
        folder_path = self.tree_widget.get_item_path(selected_item)
        if os.path.exists(folder_path):
            if self.folder_manager.delete_folder(folder_path):
                QMessageBox.information(self, "Success", "Folder deleted successfully.")
                self.tree_widget.removeItem(selected_item)
            else:
                QMessageBox.warning(self, "Error", "Failed to delete folder.")
        else:
            QMessageBox.warning(self, "Error", "Folder does not exist.")
    
    def update_sku_label(self, sku):
        self.sku_label.setText(f"Current SKU: {sku}")

    def enable_series_buttons(self, enable):
        self.series_manager.enable_series_buttons(enable)
