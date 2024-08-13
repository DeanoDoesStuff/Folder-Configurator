# SeriesManager.py
from collections import defaultdict
import os
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMessageBox
from FolderManager import FolderManager
from Utility import load_series_data


class SeriesManager:
    def __init__(self, root_dir, series_buttons, child_buttons, series_data, series_labels,
                  series_checkboxes, current_mmy_path, folder_manager):
        self.root_dir = root_dir
        self.series_buttons = series_buttons
        self.child_buttons = child_buttons
        self.series_data = series_data
        self.series_labels = series_labels
        self.series_checkboxes = series_checkboxes
        self.current_mmy_path = current_mmy_path
        self.folder_manager = folder_manager

    # Handles logic for enabling series buttons when conditions are met
    def enable_series_buttons(self, enable, current_mmy_path=None):
        print("Enable Series buttons: ")
        if enable and current_mmy_path:
            self.current_mmy_path = current_mmy_path
            print("Current MMY Path: ", current_mmy_path)
            for button in self.series_buttons:
                button.setVisible(True)
                button.setEnabled(True)
        else:
            print("No button available to enable")
            for button in self.series_buttons:
                button.setVisible(False)
                button.setEnabled(False)
            self.current_mmy_path = ""
     
    # Handles series button updates
    def update_series_button_states(self, item):
        if item:
            for button in self.series_buttons:
                series_path = os.path.join(self.current_mmy_path, button.text())
                if os.path.exists(series_path):
                    button.setStyleSheet("background-color: #0B8ED4; color: white") # Folder exists, button is blue
                    parent_button = button
                    parent_state = "blue"
                    self.update_child_button_states(parent_button, parent_state)
                else:
                    button.setStyleSheet("background-color: #C63F3F; color: white") # Folder doesn't exist, button is red
                    parent_button = button
                    parent_state = "red"
                    self.update_child_button_states(parent_button, parent_state)
        else:
            pass
    
    # Handle enableing child buttons states when conditions are met
    def enable_child_states(self):
        for button in self.child_buttons:
            button.setVisible(True)
            button.setEnabled(True)
    
    # Handles updates to the buttons states for Series Child buttons
    def update_child_button_states(self, parent_button, parent_state):
        print("Child Buttons: ", self.child_buttons)
        for child_button in self.child_buttons:
            if parent_state == "blue":
                child_button.setStyleSheet("background-color: #C63F3F; color: white") # Set to Red
            elif parent_state == "red":
                child_button.setStyleSheet("background-color: #9C9C9C; color: white") # Set to Grey
            else:
                child_button.setStyleSheet("background-color: #9C9C9C; color: white") # Default Set to Grey


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

        # gets called after full Kit sku package has been built and creates folders
    def create_package_folder(self, package_path, base_folder_path, location, fabrication, material, package, series_data):
        print("Creating folder: ", package_path)
        """Iterate through the package data and build the final folder path."""
        for package in series_data['PACKAGE']:
            # folder_path = self.build_package_folder_path(base_folder_path, location, fabrication, material, package)
            os.makedirs(package_path, exist_ok=True)
            print(f"Created folder: {package_path}")
