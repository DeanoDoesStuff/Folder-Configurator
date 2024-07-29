import os
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QMenu, QInputDialog, QMessageBox,
                              QLineEdit, QTreeWidgetItemIterator)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, Qt

class FolderTree(QTreeWidget):
    # Define a custom signal
    empty_space_clicked = pyqtSignal()
    def __init__(self, root_dir, folder_manager, parent=None):
        super().__init__(parent)
        self.root_dir = root_dir
        self.folder_manager = folder_manager
        self.setHeaderLabel("Folder Structure")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.refresh_tree()

    def load_folder_structure(self, startpath, tree):
        for element in os.listdir(startpath):
            path_info = os.path.join(startpath, element)
            parent_item = QTreeWidgetItem(tree, [os.path.basename(element)])
            if os.path.isdir(path_info):
                self.load_folder_structure(path_info, parent_item)
                parent_item.setIcon(0, QIcon('assets/file.ico'))
            else:
                parent_item.setIcon(0, QIcon('assets/file.ico'))

    def refresh_tree(self):
        self.clear()
        self.load_folder_structure(self.root_dir, self)

    def open_context_menu(self, position):
        item = self.itemAt(position)
        if item:
            menu = QMenu()
            rename_action = menu.addAction("Rename")
            action = menu.exec_(self.viewport().mapToGlobal(position))
            if action == rename_action:
                self.rename_folder(item)

    def rename_folder(self, item):
        old_name = item.text(0)
        new_name, ok = QInputDialog.getText(self, "Rename Folder", "Enter new folder name:", QLineEdit.Normal, old_name)
        if ok and new_name and new_name != old_name:
            old_path = os.path.join(self.get_item_path(item.parent()), old_name) if item.parent() else os.path.join(self.root_dir, old_name)
            new_path = os.path.join(self.get_item_path(item.parent()), new_name) if item.parent() else os.path.join(self.root_dir, new_name)
            if self.folder_manager.rename_folder(old_path, new_path):
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
    
    def get_item_depth(self, item):
        depth = 0
        while item:
            item = item.parent()
            depth += 1
        return depth

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        item = self.itemAt(event.pos())
        if item is None:
            # Emit custom signal to notify empty space click
            self.empty_space_clicked.emit()

    def save_expanded_state(self):
        expanded_items = []
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            if item.isExpanded():
                expanded_items.append(self.get_item_path(item))
            iterator += 1
        return expanded_items
    
    def restore_expanded_state(self, expanded_items):
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            if self.get_item_path(item) in expanded_items:
                item.setExpanded(True)
            iterator += 1
    
    def save_selected_item(self):
        selected_items = self.selectedItems()
        if selected_items:
            return self.get_item_path(selected_items[0])
        return None
    
    def restore_selected_item(self, selected_item_path):
        if selected_item_path:
            iterator = QTreeWidgetItemIterator(self)
            while iterator.value():
                item = iterator.value()
                if self.get_item_path(item) == selected_item_path:
                    self.setCurrentItem(item)
                    break
                iterator += 1
