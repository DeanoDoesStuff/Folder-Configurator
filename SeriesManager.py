# SeriesManager.py
import os
from FolderTree import FolderTree
from FolderManager import FolderManager

class SeriesManager:
    def __init__(self, root_dir, series_buttons):
        self.root_dir = root_dir
        self.series_buttons = series_buttons
        self.active_series_button = None

    # Handles Series buttons visibility and activity
    def update_series_button_states(self, year_item):

        self.tree_widget = FolderTree(self.root_dir, FolderManager, self)
        year_path = self.tree_widget.get_item_path(year_item) # Gets year item path from FolderTree
        for button in self.series_buttons: # Begin looping through all existing Series
            series = button.text()
            # Combine found year path with current series to build new folder path
            series_folder_path = os.path.join(year_path, series)
            if os.path.exists(series_folder_path): # Check if built path already exists
                button.setStyleSheet("background-color: lightgreen; color: black;") # Set style if true
                # TODO button state is subject to change
                button.setEnabled(False) # Ensure button is not active if folder already exists
            else:
                button.setStyleSheet("background-color: red; color: white;")
                button.setEnabled(True) # Ensure button is still enabled in order to create folders
        if self.active_series_button: # If button is active
            self.highlight_active_series_button() # Call function to change button style

    def highlight_active_series_button(self):
        if self.active_series_button:
            self.active_series_button.setStyleSheet("background-color: green; color: white;")
