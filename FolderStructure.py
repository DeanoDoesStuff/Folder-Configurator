import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QTreeWidget,
                             QTreeWidgetItem, QLineEdit, QPushButton, QMessageBox, QMenu, QInputDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Public Objects
root_page = "MAKE"

class HomeScreen(QMainWindow):
    def __init__(self, root_dir, folder_type, parent=None):
        super().__init__()
        
        self.root_dir = root_dir
        self.folder_type = folder_type
        self.parent = parent
        self.setWindowTitle(f"{folder_type} - Folder Manager")
        self.setGeometry(100, 100, 1920, 1080)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Tree Widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel(f"{folder_type} List")
        self.layout.addWidget(self.tree_widget)
        
        # Input for a new folder
        self.new_folder_input = QLineEdit()
        self.new_folder_input.setPlaceholderText(f"Enter new {folder_type}")
        self.layout.addWidget(self.new_folder_input)

        # Button for creating a new folder
        self.create_folder_button = QPushButton("Create Folder")
        self.create_folder_button.clicked.connect(self.create_new_folder)
        self.layout.addWidget(self.create_folder_button)

        # Load existing folders
        self.load_folder_structure(self.root_dir, self.tree_widget)

        # Connect context menu
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_widget.customContextMenuRequested.connect(self.open_context_menu)

    def load_folder_structure(self, startpath, tree):
        for element in os.listdir(startpath):
            path_info = os.path.join(startpath, element)
            parent_item = QTreeWidgetItem(tree, [os.path.basename(element)])
            if os.path.isdir(path_info):
                self.load_folder_structure(path_info, parent_item)
                parent_item.setIcon(0, QIcon('assets/folder.ico'))
            else:
                parent_item.setIcon(0, QIcon('assets/file.ico'))

    def create_new_folder(self):
        new_folder_name = self.new_folder_input.text().strip()
        if new_folder_name:
            new_folder_path = os.path.join(self.root_dir, new_folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                self.new_folder_input.clear()
                QMessageBox.information(self, "Success", f"Folder '{new_folder_name}' created successfully.")
                self.refresh_tree()
            else:
                QMessageBox.information(self, "Warning", f"Folder '{new_folder_name}' already exists.")
    
    def refresh_tree(self):
        self.tree_widget.clear()
        self.load_folder_structure(self.root_dir, self.tree_widget)

    def open_context_menu(self, position):
        item = self.tree_widget.itemAt(position)
        if item:
            menu = QMenu()
            rename_action = menu.addAction("Rename")
            action = menu.exec_(self.tree_widget.viewport().mapToGlobal(position))
            if action == rename_action:
                self.rename_folder(item)

    def rename_folder(self, item):
        old_name = item.text(0)
        new_name, ok = QInputDialog.getText(self, "Rename Folder", "Enter new folder name:", QLineEdit.Normal, old_name)
        if ok and new_name and new_name != old_name:
            old_path = os.path.join(self.get_item_path(item.parent()), old_name) if item.parent() else os.path.join(self.root_dir, old_name)
            new_path = os.path.join(self.get_item_path(item.parent()), new_name) if item.parent() else os.path.join(self.root_dir, new_name)
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                item.setText(0, new_name)
                QMessageBox.information(self, "Success", f"Folder '{old_name}' renamed to '{new_name}' successfully.")
            else:
                QMessageBox.information(self, "Warning", f"Folder '{new_name}' already exists.")

    def get_item_path(self, item):
        path = []
        while item:
            path.append(item.text(0))
            item = item.parent()
        return os.path.join(self.root_dir, *reversed(path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Root directory for home screen
    root_dir = "C://Instructions Gen 4"
    home_screen = HomeScreen(root_dir, root_page) # Root Page is updated from within app
    home_screen.show()

    sys.exit(app.exec_())
