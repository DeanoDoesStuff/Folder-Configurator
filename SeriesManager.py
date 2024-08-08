# SeriesManager.py
from collections import defaultdict
import os
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QCheckBox, QMessageBox
from FolderManager import FolderManager
from Utility import load_series_data


class SeriesManager:
    def __init__(self, root_dir, series_buttons, series_data, series_labels,
                  series_checkboxes, current_mmy_path, folder_manager):
        self.root_dir = root_dir
        self.series_buttons = series_buttons
        self.series_data = series_data
        self.series_labels = series_labels
        self.series_checkboxes = series_checkboxes
        self.current_mmy_path = current_mmy_path
        self.folder_manager = folder_manager

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
                    self.update_headers(series_path)
                else:
                    button.setStyleSheet("background-color: #C63F3F; color: white")
        else:
            pass

    def update_checkbox_states(self, series_path, header, checkboxes):
        """
        Update checkbox state for each location based on whether the folder exists
        """
        print("\nUpdating checkbox state")
        for checkbox in checkboxes:
            location_folder = os.path.join(series_path, checkbox.text())
            print("Location Folder: ", location_folder)
            if os.path.exists(location_folder):
                checkbox.setChecked(True)
                print(f"Check for {checkbox.text()} checked (Folder exists).")
            else:
                checkbox.setChecked(False)
                print(f"Checkbox for {checkbox.text()} not checked (Folder does not exist)")


    def update_headers(self, series_path):
        """
        Update headers visibility and checkboxes based on the series path.
        """
        for header, checkboxes in self.series_checkboxes.items():
            print(f"Updating header: {header}")
            self.update_checkbox_states(series_path, header, checkboxes)


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

    # Handles checking checkbox folder status and creates new folder if needed
    def handle_checkbox(self, active_checkbox):
        print(f"\nHandle Checkbox Logic for: {active_checkbox}")
        # TODO pass in currently selected checkbox and create a folder for that box if none exists
        checkbox_path = os.path.join(self.current_mmy_path, active_checkbox)
        if not os.path.exists(checkbox_path):
            if self.folder_manager.create_folder(checkbox_path):
                print("Created Folder: ", checkbox_path)           
        else:
            print(f"Folder {active_checkbox} will be deleted")
            if self.folder_manager.delete_folder(checkbox_path):
                print("Deleted Folder: ", checkbox_path)
    
    # TODO new function added to replace checkbox functions and create folders for Kit Skus in bundles
    def create_bundle(self, series):
        if not self.current_mmy_path:
            print("No current MMY path selected.")
            return
        
        # Get the data for the specific series
        series_data = self.series_data.get(series, defaultdict)
        print("Series Data: ", series_data)

        # Create base folder path
        base_folder_path = os.path.join(self.current_mmy_path, series)
        self.create_folders(base_folder_path, series_data)
        #create_folders = self.create_folders(base_folder_path, series_data)

    # Handle extraction of Location data
    def create_folders(self, base_folder_path, series_data):
        print("\n Location Folders--")
        for location in series_data['LOCATION']:
            location_path = os.path.join(base_folder_path, location)
            print("Location Path: ", location_path)
            self.fabrication_folder(base_folder_path, location, series_data)

    def fabrication_folder(self, base_folder_path, location, series_data):
        print("\n Fabrication Folders--")
        for fabrication in series_data['FABRICATION']:
            fabrication_path = os.path.join(base_folder_path, location, fabrication)
            print("Fabrication Path: ", fabrication_path)
            self.material_folder(base_folder_path, location, fabrication, series_data)

    def material_folder(self, base_folder_path, location, fabrication, series_data):
        print("\n Material Folders--")
        for material in series_data['MATERIAL']:
            material_path = os.path.join(base_folder_path, location, fabrication, material)
            print("Material Path: ", material_path)
            self.package_folder(base_folder_path, location, fabrication, material, series_data)

    def package_folder(self, base_folder_path, location, fabrication, material, series_data):
        print("\n Package Folders--")
        for package in series_data['PACKAGE']:
            package_path = os.path.join(base_folder_path, location, fabrication, material, package)
            print("Package Path: ", package_path)
            self.create_package_folder(package_path, base_folder_path, location, fabrication, material, package, series_data)
        
        """Construct the folder path based on the provided parameters."""
        print("Base Folder Path: ", base_folder_path)

        # Build folder paths for each KIT SKU part
    def build_package_folder_path(self, base_folder_path, location, fabrication, material, package, series_data):
        print("\n Package Folders--")
        for package in series_data['PACKAGE']:
            package_path = os.path.join(base_folder_path, location, fabrication, material, package)
            print("Package Path: ", package_path)
            self.create_package_folder(package_path, base_folder_path, location, fabrication, material, package)

        """Construct the folder path based on the provided parameters."""
        # print("Base Folder Path: ", base_folder_path)
        # kit_sku_path = os.path.join(base_folder_path, "Text")
        # print("Kit Sku Path: ", kit_sku_path)
    

        # gets called after full Kit sku package has been built and creates folders
    def create_package_folder(self, package_path, base_folder_path, location, fabrication, material, package, series_data):
        print("Creating folder: ", package_path)
        """Iterate through the package data and build the final folder path."""
        for package in series_data['PACKAGE']:
            # folder_path = self.build_package_folder_path(base_folder_path, location, fabrication, material, package)
            os.makedirs(package_path, exist_ok=True)
            print(f"Created folder: {package_path}")