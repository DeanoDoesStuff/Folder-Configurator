# SeriesManager.py

import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QCheckBox, QLineEdit, QPushButton, 
                            QMessageBox, QSplitter, QHBoxLayout, QLabel)
from Utility import load_series_data

class SeriesManager:
    def __init__(self, series_widget, folder_manager, tree_widget, sku_builder, update_sku_label, enable_series_buttons):
        self.series_widget = series_widget
        self.folder_manager = folder_manager
        self.tree_widget = tree_widget
        self.sku_builder = sku_builder
        self.update_sku_label = update_sku_label
        self.enable_series_buttons = enable_series_buttons

        self.series_data = load_series_data('Configs/SERIES_CONFIG.csv')
        self.load_series_buttons()
        self.active_series_button = None

    def load_series_buttons(self):
        self.series_buttons = []
        self.series_labels = {}
        middle_layout = self.series_widget.layout()

        for series in self.series_data:
            button = QPushButton(series)
            button.setStyleSheet("background-color: #FF474C ; color: white;")
            button.setEnabled(False)
            button.setVisible(False)
            button.clicked.connect(self.handle_series_button_click)
            middle_layout.addWidget(button)
            self.series_buttons.append(button)

            headers_layout = QHBoxLayout()

            location_label = QLabel("LOCATION")
            location_label.setVisible(False)
            headers_layout.addWidget(location_label)

            fabrication_label = QLabel("FABRICATION")
            fabrication_label.setVisible(False)
            headers_layout.addWidget(fabrication_label)

            material_label = QLabel("MATERIAL")
            material_label.setVisible(False)
            headers_layout.addWidget(material_label)

            package_label = QLabel("PACKAGE")
            package_label.setVisible(False)
            headers_layout.addWidget(package_label)

            middle_layout.addLayout(headers_layout)
            self.series_labels[series] = (location_label, fabrication_label, material_label, package_label)

    def update_series_button_states(self, year_item):
        year_path = self.tree_widget.get_item_path(year_item)
        for button in self.series_buttons:
            series = button.text()
            series_folder_path = os.path.join(year_path, series)
            if os.path.exists(series_folder_path):
                button.setStyleSheet("background-color: lightgreen; color: black;")
                button.setEnabled(False)
            else:
                button.setStyleSheet("background-color: red; color: white;")
                button.setEnabled(True)
        if self.active_series_button:
            self.highlight_active_series_button()

    def highlight_active_series_button(self):
        if self.active_series_button:
            self.active_series_button.setStyleSheet("background-color: green; color: white;")

    def enable_series_buttons(self, enable):
        for button in self.series_buttons:
            button.setEnabled(enable)
            button.setVisible(enable)

    def handle_series_button_click(self):
        sender = self.series_widget.sender()
        series = sender.text()

        selected_item = self.tree_widget.currentItem()
        if not selected_item:
            return
        
        depth = self.tree_widget.get_item_depth(selected_item)
        if depth != 3:
            QMessageBox.warning(self, "Error", "Please select a year folder to create a Series.")
            return
        
        parent_path = self.tree_widget.get_item_path(selected_item)
        new_folder_path = os.path.join(parent_path, series)
        if not os.path.exists(new_folder_path):
            if self.folder_manager.create_folder(new_folder_path):
                QMessageBox.information(self, "Success", f"Series folder '{series}' created successfully.")
                self.tree_widget.expandItem(selected_item)
                sender.setStyleSheet("background-color: lightgreen; color: black;")
            else:
                QMessageBox.warning(self, "Error", f"Failed to create series folder '{series}'.")
        
        if self.active_series_button:
            self.active_series_button.setStyleSheet("background-color: lightgreen; color: black;")
        sender.setStyleSheet("background-color: green; color: white;")
        self.active_series_button = sender
        self.update_header_visibility()

    def update_header_visibility(self):
        selected_item = self.tree_widget.currentItem()
        depth = self.tree_widget.get_item_depth(selected_item)

        style = """
            background-color: #3b3b3b;
            color: white;
            padding: 2px 5px;
            border: 1px solid #d0d0d0;
        """

        if depth >= 3:
            for button in self.series_buttons:
                series = button.text()
                location_label, fabrication_label, material_label, package_label = self.series_labels.get(series, (None, None, None, None))
                if location_label:
                    location_label.setVisible(True)
                    location_label.setStyleSheet(style)
                if fabrication_label:
                    fabrication_label.setVisible(True)
                    fabrication_label.setStyleSheet(style)
                if material_label:
                    material_label.setVisible(True)
                    material_label.setStyleSheet(style)
                if package_label:
                    package_label.setVisible(True)
                    package_label.setStyleSheet(style)
        else:
            for labels in self.series_labels.values():
                for label in labels:
                    label.setVisible(False)
