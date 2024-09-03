# SeriesManager.py

import os

# Handles all logic for middle layout from series to sub series buttons,
# creating folders, and highlighting folder to button relationship states.
class SeriesManager:
    def __init__(self, root_dir, series_buttons, child_buttons, series_data, kit_sku_dict,
                   current_mmy_path, parent_path, folder_manager):
        self.root_dir = root_dir
        self.series_buttons = series_buttons
        self.kit_sku_dict = kit_sku_dict
        self.child_buttons = child_buttons
        self.series_data = series_data
        self.current_mmy_path = current_mmy_path
        self.parent_path = parent_path
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
     

    # Handles series button updates
    def update_series_button_states(self, item):
        series_list = []
        parent_state_list = []
        if item:
            for button in self.series_buttons:
                series = button.text()
                series_path = os.path.join(self.current_mmy_path, series)
                series_list.append(series)
                if os.path.exists(series_path):
                    button.setStyleSheet("background-color: #0B8ED4; color: white") # Folder exists, button is blue
                    parent_state = "blue"
                    parent_state_list.append(parent_state)
                else:
                    button.setStyleSheet("background-color: #C63F3F; color: white") # Folder doesn't exist, button is red
                    parent_state = "red"
                    parent_state_list.append(parent_state)
            # Return list of tuples for series and parent states after looping through series buttons
            series_data = list(zip(series_list, parent_state_list))
            #print("Series Data: ", series_data)
            return series_data
        else:
            pass
    
    
    # Handle enabling child buttons states when conditions are met
    def enable_child_states(self):
        for button in self.child_buttons:
            button.setVisible(True)
            button.setEnabled(True)
    

    # Handle updates to passed in child button
    def update_child_button(self, button_id, kit):
        product_sku_path = self.construct_product_sku_path(kit)
        if os.path.exists(product_sku_path):
            button_id.setStyleSheet("background-color: #67a3db; color: white") 
        else:
            button_id.setStyleSheet("background-color: grey; color: white")


    # Handle building prdouct sku path to be used for checking folder status
    def construct_product_sku_path(self, row):
        kit_path_pieces = self.handle_sub_series_pieces(row)
        kit_path_pieces = "\\".join(kit_path_pieces)
        return os.path.join(self.current_mmy_path, kit_path_pieces)
    

    # Handles updates to active child button state
    def active_child_button(self, clicked_child, series):
        clicked_child.setStyleSheet("background-color: #2E982B; color: white;") # Button Active -- Setting Green
    

    # Breaks sub series button string into respective pieces for folder creation and comparison.
    def handle_sub_series_pieces(self, kit_bundle):
        sub_series_pieces = kit_bundle.split("->")
        return sub_series_pieces
    

    # Handles creation of sub series folder when a button is clicked and no folders exist
    def create_sub_series_folders(self, sub_series_pieces):
        location, fabrication, material, package = sub_series_pieces
        return location, fabrication, material, package


    # Handles formatting of each row to add the current series to the front of the row string
    # all unique series row string get added to a list
    def format_rows(self, combined_rows, series):
        current_row_string_list = []
        for entry in combined_rows:
            current_row_string = ''.join(series + "->" + entry)
            current_row_string_list.append(current_row_string)
        return current_row_string_list # Returns full row string including the current series at the beginning of every row


    # Handles formatting of each child button string by adding the current series to the front of every button string
    def format_child_strings(self, child_text, series):
        return f"{series}->{child_text}"


    # Handles creation of subfolders for sub series if current path doesn't exist.
    def create_sub_series(self, sub_series_path):
        if not os.path.exists(sub_series_path):
            os.makedirs(sub_series_path)
            return True
        else:
            return False
        
    
    # Handles the creation of a Support Assets folder 
    def create_support_assets(self, sub_series_path):
        support_assets_path = os.path.join(sub_series_path, "SUPPORT ASSETS")
        if not os.path.exists(support_assets_path):
            os.makedirs(support_assets_path)
            return support_assets_path
        else:
            return support_assets_path


    # Handles processing of Kit SKU config files 
    def handle_kit_config(self, series, kit_bundle):
        # Find special character in kit_bundle string to remove special characters
        if "->" in kit_bundle:
            # Add entry to list by splitting at special character
            format_kit_bundle_list = kit_bundle.split("->") 
            format_kit_bundle = "_".join(format_kit_bundle_list) # Joins the list into a string
            kit_sku_config = series + "_" + format_kit_bundle # Builds the final config file name
        return kit_sku_config
