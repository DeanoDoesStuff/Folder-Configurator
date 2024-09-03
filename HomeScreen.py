#HomeScreen.py
import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTreeWidgetItem,
                             QMessageBox, QSplitter, QHBoxLayout, QLabel, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from FolderManager import FolderManager
from FolderTree import FolderTree
from SkuBuilder import SkuBuilder
from CompanionManager import CompanionManager
from SeriesManager import SeriesManager
from Utility import Utility
from Companions import companion_dict_data, uni_part_groups

class HomeScreen(QMainWindow):
    def __init__(self, root_dir, folder_type, parent=None):
        super().__init__()

        self.root_dir = root_dir
        self.folder_type = folder_type
        self.parent = parent
        self.sku_builder = SkuBuilder()
        self.setWindowTitle("Folder Manager")
        self.setGeometry(0, 0, 1920, 1080)

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

        # Add left widget to splitter
        self.splitter.addWidget(self.left_widget)
        
        # Middle Widget for Series options with scroll area
        self.middle_scroll_area = QScrollArea()
        self.middle_scroll_area.setWidgetResizable(True)

        # Middle Widget for Series options
        self.middle_widget = QWidget()
        self.middle_layout = QVBoxLayout()
        self.middle_widget.setLayout(self.middle_layout)
        self.splitter.addWidget(self.middle_widget)

        self.middle_scroll_area.setWidget(self.middle_widget)
        self.splitter.addWidget(self.middle_scroll_area)

        # Initialize mmy path
        # TODO refactor path code to maintain only one variable to be updated, instead of moving the data from var to var
        self.current_mmy_path = ""
        self.parent_path = ""
        self.series_path = ""
        self.sub_series_path = ""
        # Load series data from CSV file
        self.series_data = Utility.load_series_data('Configs/SERIES_CONFIG.csv')

        self.kit_dict = {}
        # Initialize kit sku dictionary
        self.kit_sku_dict = {}
        
        # Initialize SeriesManager
        self.series_buttons = []
        self.child_buttons = []
        self.combined_rows = []
        self.series_manager = SeriesManager(
            root_dir = self.root_dir, 
            series_buttons = self.series_buttons,
            child_buttons = self.child_buttons,
            kit_sku_dict = self.kit_sku_dict,
            series_data = self.series_data,
            folder_manager = self.folder_manager,
            current_mmy_path = self.current_mmy_path,
            parent_path = self.parent_path
        )

        # Load and display series buttons
        self.load_series_buttons()

        # Tree Widget
        self.tree_widget = FolderTree(self.root_dir, self.folder_manager, self.series_manager, self)
        self.tree_widget.itemClicked.connect(self.handle_tree_item_click) # type: ignore
        self.tree_widget.empty_space_clicked.connect(self.reset_folder_type)  # Connect to empty space signal 
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

        # Right Widget (For displaying SKU and other controls)
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_widget.setLayout(self.right_layout)

        self.splitter.addWidget(self.right_widget)

        # Set initial sizes for the splitter (optional)
        self.splitter.setSizes([200, 400, 600])

        # Set Tulip integration window Layout
        self.submit_widget = QWidget()
        self.submit_layout = QVBoxLayout()
        self.submit_widget.setLayout(self.submit_layout)

        self.sku_label = QLabel("Current SKU: ")
        self.submit_layout.addWidget(self.sku_label)

        # Initialize folder type and button state
        self.update_folder_type(self.tree_widget.currentItem())

        # Track the active series button
        self.active_series_button = None

        # Instantiate CompanionManager
        self.companion_manager = CompanionManager()
        self.right_layout.addWidget(self.companion_manager)

        # Initialize Companion Data
        self.companion_buttons = {}


    # Handles signals from items clicked in Folder Tree
    def handle_tree_item_click(self, item):
        # Process current tree item depth
        depth = self.tree_widget.get_item_depth(item)

        if depth < 3:
            self.update_folder_type(item)
            self.tree_widget.setDisabled(False)

        if depth == 3:
            self.update_folder_type(item)
            current_mmy_path = self.tree_widget.get_item_path(item)
            self.series_manager.enable_series_buttons(True, current_mmy_path)
            self.series_data = self.series_manager.update_series_button_states(item)
            print("Series Data: ", self.series_data)
            self.series_manager.enable_child_states()

            for button_id, kit in self.kit_dict.items():
                print("Current Kit: ", kit)
                self.series_manager.update_child_button(button_id, kit)
            # Re-enable tree widget if at depth less than 3
            self.tree_widget.setDisabled(False)
            self.lock_tree_beyond_mmy(item, depth)

        elif depth > 3:
            self.lock_tree_beyond_mmy(item, depth)

        return depth

    def lock_tree_beyond_mmy(self, item, depth):
        if depth <= 2:
            return # Params met, tree is live for these depths
        
        # Recursively traverse tree items starting from the provided item
        for i in range(item.childCount()):
            child = item.child(i)
            child_depth = self.tree_widget.get_item_depth(child)  # You need to define this method
            if child_depth > 2:
                # Disable interaction for this child item
                self.set_item_interactive(child, False)
            else:
                # Continue traversing
                self.lock_tree_beyond_mmy(child, child_depth)

    def set_item_interactive(self, item, interactive):
        flags = item.flags()
        if interactive:
            # Add flags to make item selectable and enabled
            item.setFlags(flags | Qt.ItemIsSelectable | Qt.ItemIsEnabled) # type: ignore
        else:
            # Remove flags to make item non-selectable and disabled
            item.setFlags(flags & ~(Qt.ItemIsSelectable | Qt.ItemIsEnabled)) # type: ignore

    # Handles tracking of selected folder type by calculating depth
    def update_folder_type(self, item):
        current_sku = ""
        if item:
            depth = self.tree_widget.get_item_depth(item)

            (make_id, model_id, year_id, series_id, location_id,
              fab_id, mat_id, package_id) = self.sku_builder.process_depth(item, depth)
            if depth == 0:
                self.folder_type = " Make"
            elif depth == 1:
                self.folder_type = " Model"
                current_sku = make_id
            elif depth == 2:
                self.folder_type = " Year"
                current_sku = make_id + model_id
            elif depth == 3:
                self.folder_type = " SERIES"
                current_sku = make_id + model_id + year_id
            else:
                self.folder_type = " None"
                current_sku = self.make_id
            if depth < 3:
                self.new_folder_input.setPlaceholderText(f"Enter new{self.folder_type}")
            else:
                self.new_folder_input.setPlaceholderText("")
            self.create_folder_button.setEnabled(self.folder_type != " None")
            self.create_folder_button.setEnabled(self.folder_type != " SERIES")
            self.update_sku_label(current_sku)
            return current_sku
    
    # Handles the creation of new folders
    def create_new_folder(self):
        new_folder_name = self.new_folder_input.text().strip()
        if new_folder_name:
            selected_item = self.tree_widget.currentItem() 
            if selected_item:
                parent_path = self.tree_widget.get_item_path(selected_item)
            else:
                parent_path = self.root_dir

            new_folder_path = os.path.join(parent_path, new_folder_name) 

            expanded_state = self.tree_widget.save_expanded_state()
            selected_item_path = self.tree_widget.save_selected_item()
            if self.folder_manager.create_folder(new_folder_path):
                self.new_folder_input.clear()
                QMessageBox.information(self, "Success", f"Folder '{new_folder_name}' created successfully.")
                
                self.tree_widget.restore_expanded_state(expanded_state)
                self.tree_widget.restore_selected_item(selected_item_path)
                self.tree_widget.refresh_tree()
            else:
                QMessageBox.information(self, "Warning", f"Folder '{new_folder_name}' already exists.")

    # Handles the deletion of folders
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
                    self.tree_widget.collapseAll()
                    self.tree_widget.clearSelection()
                else:
                    QMessageBox.warning(self, "Error", f"Failed to delete folder '{selected_item.text(0)}'. It might not be empty.")
    
    # Handles the displayed object for current selections total SKU
    def update_sku_label(self, sku):
        self.sku_label.setText(f"Current SKU: {sku}") 
    
    # Handles folder type reset
    def reset_folder_type(self):
        self.folder_type = " Make"
        self.new_folder_input.setPlaceholderText(f"Enter new {self.folder_type}")
        self.create_folder_button.setEnabled(True)
        self.update_sku_label("")
        self.series_manager.enable_series_buttons(False)
        self.tree_widget.refresh_tree()

    # Handles the loading of series and children objects for KIT skus
    def load_series_buttons(self):
        self.series_buttons = []
        
        series_keys = list(self.series_data.keys())
        print("Series Keys: ", series_keys)
        for series, series_info in self.series_data.items():
            # Create a layout for each series
            series_layout = QVBoxLayout()

            # Create parent button for each series
            self.create_series_button(series, series_info, series_layout)

            # Add the series layout to the middle layout
            self.middle_layout.addLayout(series_layout)

        self.series_manager.series_buttons = self.series_buttons

    # handles creation of buttons for unique series found in the Series_Config.csv file
    def create_series_button(self, series, series_info, series_layout):
        # Create parent button for each series
        series_button = QPushButton(series)
        series_button.setStyleSheet("background-color: #C63F3F; color: white;") #
        # Initially hide buttons. Set visible when condition is met
        series_button.setEnabled(False)
        series_button.setVisible(False)
        series_button.clicked.connect(self.handle_series_button_click)
        series_layout.addWidget(series_button)
        
        # BUG for some reason the child series buttons are being added to the list of parent series buttons. 
        # They should be going into their own list instead
        self.series_buttons.append(series_button)

        #Create child buttons for each row of data in unique series
        self.create_child_buttons(series, series_info, series_layout)
        # Call Kit SKU dictionary to store series as key and combined rows as values
        self.kit_sku_dictionary(series, self.combined_rows)
        

    # Handles child series buttons. child series code from above function will be moved here 
    def create_child_buttons(self, series, series_info, series_layout):
        # Loop through extracted csv rows and set button layout and visuals
        for row in self.get_combined_row_data(series, series_info): # Call function to pass row string to build button string info
            #print("Child Row: ", row)
            self.child_button = QPushButton(row)
            self.child_button.setStyleSheet("background-color: #9C9C9C; color: black;") # Inactive -- Grey
            # Initially hide buttons. Set visible when condition is met
            self.child_button.setEnabled(False)
            self.child_button.setVisible(False)
            self.child_button.clicked.connect(self.handle_child_button_click)

            # Combine parent series text and child button text
            kit_text = f"{series}->{row}"

            # Populate the dictionary with the child button as key and the combined text as value
            self.kit_dict[self.child_button] = kit_text
            print("Kit Dictionary: ", self.kit_dict)

            series_layout.addWidget(self.child_button)
            self.child_buttons.append(self.child_button)


    # Handles string concat of extracted series config row data
    def get_combined_row_data(self, series, series_info):
        print("Series: ", series)
        print("Series Data: ", series_info)
        self.combined_rows = []
        for row in series_info:
            combined_row = "->".join(row)
            #print("Combined Row: ", combined_row)
            self.combined_rows.append(combined_row)
        return self.combined_rows


    # Handle dictionary to hold Series as keys and child buttons as values
    def kit_sku_dictionary(self, series, combined_rows):
        # Update dictionary to hold kit skus where series are keys and combined rows are values
        self.kit_sku_dict[series] = combined_rows
        self.series_manager.kit_sku_dict = self.kit_sku_dict
        return self.kit_sku_dict

    # Handle signal emit when series button is clicked
    def handle_series_button_click(self):
        clicked_button = self.sender()
        series = clicked_button.text()

        if self.active_series_button:
            self.active_series_button.setStyleSheet("background-color: #0B8ED4; color: white;") # Color Blue
        self.active_series_button = clicked_button
        
        clicked_button.setStyleSheet("background-color: #2E982B; color: white;") # Color Green

        selected_item = self.tree_widget.currentItem() # Get selected item name from Tree
        self.parent_path = self.tree_widget.get_item_path(selected_item)
        
        
        # Calls Helper function to handle sku updates,
        self.series_sku(clicked_button)

        new_folder_path = os.path.join(self.parent_path, series)
        # Check if newly created path already exists in the directory
        if not os.path.exists(new_folder_path):
            print("No folder exists yet for this series")
            if self.folder_manager.create_folder(new_folder_path):
                QMessageBox.information(self, "Success", f"Series folder '{series}' created successfully.")
                self.tree_widget.expandItem(selected_item) # Ensure the newly created folder is visible
                clicked_button.setStyleSheet("background-color: #2E982B; color: white;")  # Change to light green
            else:
                QMessageBox.warning(self, "Error", f"Failed to create series folder '{series}'.") 
        return

    # Helper function to build out series sku data
    def series_sku(self, clicked_button):
        mmy_sku_num = self.sku_label.text().split(': ')[1]
        while len(mmy_sku_num) > 8:
            mmy_sku_num = mmy_sku_num[:-1]
        self.update_kit_sku(clicked_button, mmy_sku_num)

    # Helper function to build out sub series sku data
    def sub_series_sku(self, clicked_button):
        mmy_sku_num = self.sku_label.text().split(': ')[1]
        while len(mmy_sku_num) > 10:
            mmy_sku_num = mmy_sku_num[:-1]
        self.update_kit_sku(clicked_button, mmy_sku_num)

    # Helper function to build out companio sku data
    def companion_sku(self, clicked_companion):
        mmy_sku_num = self.sku_label.text().split(': ')[1]
        while len(mmy_sku_num) > 14:
            mmy_sku_num = mmy_sku_num[:-1]
        self.update_companion_sku(clicked_companion, mmy_sku_num)


    # Handles logic for updating kit sku variable displayed in the right pane
    def update_kit_sku(self, clicked_button, mmy_sku_num):
        # Checks the length of parent SKU 
        if len(mmy_sku_num) == 8:
            # Process the sku as only the MMY and Series
            series_sku = SkuBuilder.process_kit_sku(clicked_button) # Calls function to process kit sku
        else:
            # Process the sku as the MMY and the full Kit SKU, building the full Product SKU as a result
            series_sku = SkuBuilder.process_product_sku(clicked_button) # Calls function to process product sku
            product_sku = mmy_sku_num + series_sku
            self.update_sku_label(product_sku) # Update display widget with newly build product SKU
            return # Kills the process before moving into kit sku functionality

        current_sku_num = mmy_sku_num # Assign mutable variable to current baseline MMY SKU
        
        current_sku = "".join(current_sku_num + series_sku[0]) # Joins base SKU with extracted data
        self.update_sku_label(current_sku) # Updates the display widget with newly build SKU

    # TODO wip trying to finish out companion sku funtionality
    def update_companion_sku(self, clicked_companion, mmy_sku_num):
        print("SKU Length: ", len(mmy_sku_num))
        if len(mmy_sku_num) == 14:
            companion_sku = SkuBuilder.process_kit_sku(clicked_companion)

        else:
            companion_sku = SkuBuilder.process_kit_sku(clicked_companion)
            full_sku = mmy_sku_num + "-"
            full_sku = mmy_sku_num + companion_sku[0]
            print("Full SKU: ", full_sku)
            self.update_sku_label(full_sku)

            return
        
        current_sku_num = mmy_sku_num
        current_sku_num = current_sku_num + "-"
        current_sku = "".join(current_sku_num + companion_sku[0])
        print("Current SKU: ", current_sku)
        self.update_sku_label(current_sku)

    """
    This function handles events for series button clicks
    When no folders for the specified info exist if a series is active and the child button is clicked
    Folders for that specific series will be created in sequence. The button is then active
    Active buttons begin the processes of asset inputs into created folders on the right hand panel.
    """
    def handle_child_button_click(self):

        # TODO create logic to handle creation of uni part groups
        # TODO create logic to handle storing of misc assets -- instructions, bend sheets, 
        if self.active_series_button:
            series = self.active_series_button.text()
            clicked_child = self.sender()
            kit_bundle = clicked_child.text()
            folders_created = False

            # Function calls for building, creating, and reading kit sku config files
            SeriesManager.handle_kit_config(self, series, kit_bundle)

            # Update active child state
            # TODO update to new function set
            for button_id, kit in self.kit_dict.items():
                print("Current Kit: ", kit)
                self.series_manager.update_child_button(button_id, kit)
            # self.series_manager.update_child_button_states(self.series_data)

            SeriesManager.active_child_button(self, clicked_child, series)
            # Calls function to format sub series, returns formatted pieces in a list
            sub_series_pieces = SeriesManager.handle_sub_series_pieces(self, kit_bundle)

            # Create folders if none exist
            self.series_path = os.path.join(self.parent_path, series)
            (location, fabrication,
              material, package) = SeriesManager.create_sub_series_folders(self, sub_series_pieces)
            self.sub_series_path = self.series_path
            
            for folder in sub_series_pieces:
                self.sub_series_path = os.path.join(self.sub_series_path, folder)

                # Extracts sku data and update the current sku
                # Calls Helper function to handle sku updates,
                self.sub_series_sku(clicked_child)

                # Call create sub series function while still in sub series list loop
                folders_created = SeriesManager.create_sub_series(self, self.sub_series_path)
                
                # TODO create logic to store misc assets as well as specific custom image assets
                SeriesManager.create_support_assets(self, self.sub_series_path)

            if folders_created == True:
                QMessageBox.information(self, "Success",
                                        f"Folders '{location}'; '{fabrication}'; '{material}'; '{package}'; Succesfully Created!")


            # Handle companion logic
            self.sub_series_combo = tuple(sub_series_pieces) # Convert the list to a tuple before accessing the dictionary
            series_data = companion_dict_data.get(series, {}) # Check if series exists
            companions = series_data.get(self.sub_series_combo, {}) # Access companions
            print("Companions: ", companions)
            # Calls function to create companion button widgets
            self.companion_buttons, companion_buttons_list = CompanionManager.create_companion_buttons(self, companions)
            for button in companion_buttons_list:
                CompanionManager.update_companion_buttons(self, button, self.sub_series_path)
            # Calls function to create companion based radio buttons
            CompanionManager.create_radio_buttons(self, self.companion_buttons)


    # Handles companion button click logic.
    def companion_button_click(self):

        clicked_companion = self.sender()
        self.companion = clicked_companion.text()

        full_path = os.path.join(self.sub_series_path, self.companion)
        clicked_companion.setStyleSheet("background-color: #2E982B; color: white;") # Active button - highlight green.

        # Calls Helper function to handle sku updates,
        self.companion_sku(clicked_companion)

        # Check if newly created path already exists in the directory
        if not os.path.exists(full_path): # If no path found create the new folder path
            print("No folder exists yet for this series")
            if self.folder_manager.create_folder(full_path):
                QMessageBox.information(self, "Success", f"Series folder '{self.companion}' created successfully.")
                clicked_companion.setStyleSheet("background-color: #2E982B; color: white;")  # Change to light green
            else: # error handling with message.
                QMessageBox.warning(self, "Error", f"Failed to create series folder '{self.companion}'.")
        return
        

    # Handles type-variable radio button click logic.
    def type_button_click(self):
        # TODO disable button click if no Companion is selected
        # Handle button click signals
        clicked_radio = self.sender()
        type_var = clicked_radio.text()
        if "=" in type_var:
            type_var_tuple = type_var.split("=")
            type_var_sku = type_var_tuple[0]
            print("Type SKU: ", type_var_sku)

        if type_var_sku == "C":
            print("Custom selected")

            CompanionManager.create_custom_file_input_widgets(self, companion_dict_data,
                                                               self.companion, self.sub_series_combo, clicked_radio)
        else:
            print("UNI Selected")
            # Grab UNI key portion of the current sku to pass into UNI companion dictionary as a key
            mmy_sku_num = self.sku_label.text().split(': ')[1]
            desired_length = 8 # Specific length of the expected key

            # Keep only the last characters until the specified length is reached
            uni_key = ''.join(mmy_sku_num[-desired_length:])
            print("UNI KEY: ", uni_key)

            # Check if current UNI Key exists in dictionary
            if uni_part_groups.get(uni_key) is not None:
                # Key found, pass the contents to now create uni input button widgets
                companion_data = uni_part_groups.get(uni_key)
                self.uni_buttons = CompanionManager.create_uni_input_widgets(self, companion_data,
                                                                             clicked_radio)
            else:
                # # No key found, kill the process.
                print("No matching key found")

    def uni_button_click(self):
        # TODO build out function to handle UNI button clicks here...
        clicked_uni = self.sender()
        uni_button_text = clicked_uni.text()
        print("Uni Button Text: ", uni_button_text)
        CompanionManager.update_uni_button(self, clicked_uni)

        clicked_uni.setStyleSheet("background-color: #2E982B; color: white;") # Active -- Green
        