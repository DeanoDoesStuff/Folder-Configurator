import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
                              QLineEdit, QPushButton, QMessageBox, QSplitter, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from FolderManager import FolderManager
from FolderTree import FolderTree
from SkuBuilder import SkuBuilder

# Public Objects
folder_type = " Make"

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
        
        # Right Widget (for context buttons or other widgets)
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

        # Set initial sizes for the splitter (optional)
        self.splitter.setSizes([200, 600])  # Set the initial size for the left and right widgets

        # Initialize folder type and button state
        self.update_folder_type(self.tree_widget.currentItem())

    def handle_tree_item_click(self, item):
        self.update_folder_type(item)

    def update_folder_type(self, item):
        if item:
            depth = self.tree_widget.get_item_depth(item)
            if depth == 0:
                self.folder_type = " Make"
            elif depth == 1:
                self.folder_type = " Model"
            elif depth == 2:
                self.folder_type = " Year"
            else:
                self.folder_type = " None"
        else:
            self.folder_type = " Make"
        
        self.new_folder_input.setPlaceholderText(f"Enter new{self.folder_type}")
        self.create_folder_button.setEnabled(self.folder_type != " None")

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

    def reset_folder_type(self):
        self.update_folder_type(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Root directory for home screen
    root_dir = "C://Instructions Gen 4"
    home_screen = HomeScreen(root_dir, folder_type)
    home_screen.show()

    sys.exit(app.exec_())

