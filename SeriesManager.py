# SeriesManager.py
import os
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QCheckBox

class SeriesManager:
    def __init__(self, root_dir, series_buttons, series_data, series_labels, series_checkboxes, current_mmy_path):
        self.root_dir = root_dir
        self.series_buttons = series_buttons
        self.series_data = series_data
        self.series_labels = series_labels
        self.series_checkboxes = series_checkboxes
        self.current_mmy_path = current_mmy_path
    
    # Handles logic for enabling series buttons when conditions are met
    def enable_series_buttons(self, enable, current_mmy_path=None):
        if enable and current_mmy_path:
            self.current_mmy_path = current_mmy_path
            for button in self.series_buttons:
                button.setVisible(True)
                button.setEnabled(True)
        else:
            for button in self.series_buttons:
                button.setVisible(False)
                button.setEnabled(False)
            self.current_mmy_path = ""
    
    # Handles if signal from Tree contains a Series and updates the active series buttons
    def update_active_series(self, item, current_mmy_path=None):
        if item:
            print("Current active Series Path: ", current_mmy_path)
            parts = current_mmy_path.split("\\")
            active_series = parts[-1]
            print("Active Series: ", active_series)
            for button in self.series_buttons:
                parts = current_mmy_path.split("\\")
                series_path = "\\".join(parts[:-1])
                series_path = os.path.join(series_path, button.text())
                print("Series Path: ", series_path)
                print("Button Series: ", button.text())

                if button.text() == active_series:
                    button.setStyleSheet("background-color: #2E982B; color: white") # Active button, Green
                elif os.path.exists(series_path):
                    print("Folder found, setting Button Style to Inactive but passive")
                    button.setStyleSheet("background-color: #0B8ED4; color: white") # Exists, marked blue
                    # Update header styles
                    self.update_headers(series_path)
                else:
                    print("No folder found, setting inactive and off.")
                    # Set folder status based on if it's inactive and doesn't exist
                    button.setStyleSheet("background-color: #C63F3F; color: white") # Doesn't exists, Red

    # Handles series button updates
    def update_series_button_states(self, item):
        # TODO make seperate case for when signal from Tree is deeper than 4
        """
        BUG if depth 4 or more selected in Tree, 
        path strings are adding current active selection plus looped series values
        """  
        # This loop runs when signal from Tree comes from depth 3 (year)
        if item:
            for button in self.series_buttons:
                series_path = os.path.join(self.current_mmy_path, button.text())
                print("Updating series button at: ", series_path)
                if os.path.exists(series_path):
                    button.setStyleSheet("background-color: #0B8ED4; color: white")
                else:
                    button.setStyleSheet("background-color: #C63F3F; color: white")
        else:
            pass

    def update_headers(self, series_path):
        print("Now Updating Headers")

        pass

    def header_styles(header):
        print("Header Style: ", header)
        # TODO check if KIT sku folder exists and set header style
        # Base style
        if header:
            style = """
                background-color: #3b3b3b;
                color: white;
                padding: 2px 5px;
                border: 1px solid #d0d0d0;
            """
        else:
            # Active label style
            active_style = """
                background-color: #2E982B;
                color: white;
                padding: 2px 5px;
                border: 1px solid #d0d0d0;
            """
            style = active_style

        return style
    
    def create_checkbox_folder():

        pass