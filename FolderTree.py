#FolderTree.py
import os
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QMenu, QInputDialog, QMessageBox,
                              QLineEdit, QTreeWidgetItemIterator)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt

# Covers functions for handling Tree processes
class FolderTree(QTreeWidget):
    # Define a custom signal
    item_clicked = pyqtSignal(QTreeWidgetItem)
    empty_space_clicked = pyqtSignal()

    def __init__(self, root_dir, folder_manager, series_manager, parent=None):
        super().__init__(parent)
        self.root_dir = root_dir
        self.folder_manager = folder_manager
        self.series_manager = series_manager
        self.setHeaderLabel("Folder Structure")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.refresh_tree()
        self.itemClicked.connect(self.on_item_clicked)

    # Handle sending signal when tree item is clicked
    def on_item_clicked(self, item, column):
        self.item_clicked.emit(item)

    # Handles loading folder structure into Tree Widget
    def load_folder_structure(self, startpath, tree):
        for element in os.listdir(startpath): # Loop through directory at startpath
            path_info = os.path.join(startpath, element)
            parent_item = QTreeWidgetItem(tree, [os.path.basename(element)])
            parent_item.setData(0, Qt.UserRole, path_info)  # Set the path as data
            if os.path.isdir(path_info):
                self.load_folder_structure(path_info, parent_item)
                # Default icon, this can be changed to custom asset for each element in Tree
                parent_item.setIcon(0, QIcon('assets/file.ico')) 
            else:
                # Keep this as the default icon in case custom asset is corrupted or missing etc.
                parent_item.setIcon(0, QIcon('assets/file.ico'))

    # Handles event for refreshing Tree
    def refresh_tree(self):
        self.clear()
        self.load_folder_structure(self.root_dir, self)

    # Handles opening of context menu modal for actions
    def open_context_menu(self, position):
        item = self.itemAt(position)
        if item:
            menu = QMenu()
            rename_action = menu.addAction("Rename")
            action = menu.exec_(self.viewport().mapToGlobal(position))
            # Rename action block
            if action == rename_action:
                self.rename_folder(item)
            # More action blocks for context menu can go here...

    # Handles folder renaming
    def rename_folder(self, item): # Selected item is passed in
        old_name = item.text(0) # Old name is extracted for user to compare with a new name input
        # Open create name dialogue modal
        new_name, ok = QInputDialog.getText(self, "Rename Folder", "Enter new folder name:", QLineEdit.Normal, old_name)
        if ok and new_name and new_name != old_name: # Handle when user confirms name change
            old_path = os.path.join(self.get_item_path(item.parent()), old_name) if item.parent() else os.path.join(self.root_dir, old_name)
            new_path = os.path.join(self.get_item_path(item.parent()), new_name) if item.parent() else os.path.join(self.root_dir, new_name)
            if self.folder_manager.rename_folder(old_path, new_path): # Sets path to new name
                item.setText(0, new_name)
                QMessageBox.information(self, "Success", f"Folder '{old_name}' renamed to '{new_name}' successfully.")
            else:
                # Handle when user creates new name that is same as old name
                QMessageBox.information(self, "Warning", f"Folder '{new_name}' already exists.")

    # Handles a request for item path
    def get_item_path(self, item):
        path = []
        while item:
            path.append(item.text(0))
            item = item.parent()
        return os.path.join(self.root_dir, *reversed(path))
    
    # Handles request for item depth
    def get_item_depth(self, item):
        depth = 0
        while item: # Loop depth until parent item becomes selected item
            item = item.parent()
            depth += 1 # Increase depth value until condition is met
        return depth

    # Handles Mouse press event signals inside Tree
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        item = self.itemAt(event.pos()) # Handles instance when mouse click is an item in Tree
        if item is None:
            # Emit custom signal to notify empty space click
            self.empty_space_clicked.emit()

    # Handles saving of Tree state
    def save_expanded_state(self):
        expanded_items = []
        iterator = QTreeWidgetItemIterator(self)
        # Loop through current opened item to ensure parent items in Tree remain expanded
        while iterator.value():
            item = iterator.value()
            if item.isExpanded():
                expanded_items.append(self.get_item_path(item))
            iterator += 1
        return expanded_items
    
    # Handles restoring Tree to expanded state
    def restore_expanded_state(self, expanded_items): # Pass in list of expanded items
        iterator = QTreeWidgetItemIterator(self)
        # Loop through expanded items
        while iterator.value():
            item = iterator.value()
            if self.get_item_path(item) in expanded_items:
                item.setExpanded(True)
            iterator += 1
    
    # Handles extraction of selected item path
    def save_selected_item(self):
        selected_items = self.selectedItems()
        if selected_items:
            return self.get_item_path(selected_items[0])
        return None
    
    # Handles restoration of the selected item
    def restore_selected_item(self, selected_item_path):
        if selected_item_path:
            iterator = QTreeWidgetItemIterator(self)
            while iterator.value():
                item = iterator.value()
                if self.get_item_path(item) == selected_item_path:
                    self.setCurrentItem(item)
                    break
                iterator += 1
                