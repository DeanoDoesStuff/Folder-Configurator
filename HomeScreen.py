#HomeScreen.py
import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton,
                             QMessageBox, QSplitter, QHBoxLayout, QLabel, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from FolderManager import FolderManager
from FolderTree import FolderTree
from SkuBuilder import SkuBuilder
from CompanionManager import CompanionManager
from SeriesManager import SeriesManager
from Utility import load_series_data, create_kit_sku_config, load_kit_sku_data

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
        self.current_mmy_path = ""
        self.parent_path = ""
        # Load series data from CSV file
        self.series_data = load_series_data('Configs/SERIES_CONFIG.csv')

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
        self.tree_widget.itemClicked.connect(self.handle_tree_item_click)
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

        self.sku_label = QLabel("Current SKU: ")
        self.right_layout.addWidget(self.sku_label)

        self.splitter.addWidget(self.right_widget)

        # Set initial sizes for the splitter (optional)
        self.splitter.setSizes([200, 400, 600])

        # Initialize folder type and button state
        self.update_folder_type(self.tree_widget.currentItem())

        # Track the active series button
        self.active_series_button = None

        # Instantiate CompanionManager
        self.companion_manager = CompanionManager()
        self.right_layout.addWidget(self.companion_manager)
    

    # Handles signals from items clicked in Folder Tree
    def handle_tree_item_click(self, item):
        self.update_folder_type(item)
        depth = self.tree_widget.get_item_depth(item)
        if depth == 3:
            current_mmy_path = self.tree_widget.get_item_path(item)
            print("Current Path: ", current_mmy_path)
            self.series_manager.enable_series_buttons(True, current_mmy_path)
            series_data = self.series_manager.update_series_button_states(item)
            print("Series List: ", series_data)
            # TODO update SeriesManager methods to update sub series states when at Year depth
            self.series_manager.enable_child_states()
            self.series_manager.update_child_button_states(series_data)

        elif depth > 3:
            # TODO disable tree at depth greater than 3
            current_mmy_path = self.tree_widget.get_item_path(item)
            print("Current Tree Item Path: ", current_mmy_path)
            self.series_manager.enable_series_buttons(True, current_mmy_path)
            self.series_manager.update_series_button_states(item)
            #self.series_manager.update_active_series(item, current_mmy_path)
        return depth

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
            elif depth == 4:
                self.folder_type = " LOCATION"
                current_sku = make_id + model_id + year_id + series_id
            elif depth ==5:
                self.folder_type = " FABRICATION"
                current_sku = make_id + model_id + year_id + series_id + location_id
            elif depth ==6:
                self.folder_type = " MATERIAL"
                current_sku = make_id + model_id + year_id + series_id + location_id + fab_id
            elif depth == 7:
                self.folder_type = " PACKAGE"
                current_sku = make_id + model_id + year_id + series_id + location_id + fab_id + mat_id
            elif depth == 8:
                self.folder_type = " Full SKU"
                current_sku = make_id + model_id + year_id + series_id + location_id + fab_id + mat_id + package_id
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
            print("\nStart parent button Loop for Series: ", series)
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
            child_button = QPushButton(row)
            child_button.setStyleSheet("background-color: #9C9C9C; color: black;") # Inactive -- Grey
            # Initially hide buttons. Set visible when condition is met
            child_button.setEnabled(False)
            child_button.setVisible(False)
            child_button.clicked.connect(self.handle_child_button_click)
            series_layout.addWidget(child_button)
            # BUG fix the parent and child buttons appending issue. 
            self.child_buttons.append(child_button)
   
    # Handles string concat of extracted series config row data
    def get_combined_row_data(self, series, series_info):
        self.combined_rows = []
        
        # Check if series_info contains the necessary columns
        print("Series: ", series)
        print("Series Info: ", series_info)
        # Loop through rows and extract data into child buttons
        for row in series_info:
            combined_row = "->".join(row)
            # print("Combined Row: ", combined_row)
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
        print(f"Series: {series}")

        if self.active_series_button:
            self.active_series_button.setStyleSheet("background-color: #0B8ED4; color: white;") # Color Blue
        self.active_series_button = clicked_button
        
        clicked_button.setStyleSheet("background-color: #2E982B; color: white;") # Color Green

        selected_item = self.tree_widget.currentItem() # Get selected item name from Tree
        self.parent_path = self.tree_widget.get_item_path(selected_item)
        print(f"Parent path: {self.parent_path}")
        
        # Calls Helper function to handle sku updates,
        self.series_sku( clicked_button)

        new_folder_path = os.path.join(self.parent_path, series)
        # Check if newly created path already exists in the directory
        if not os.path.exists(new_folder_path):
            print("No folder exists yet for this series")
            if self.folder_manager.create_folder(new_folder_path):
                print("New Folder Path: ", new_folder_path)
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
            print("MMY SKU: ", mmy_sku_num)
        self.update_kit_sku(clicked_button, mmy_sku_num)

    # Helper function to build out sub series sku data
    def sub_series_sku(self, clicked_button):
        mmy_sku_num = self.sku_label.text().split(': ')[1]
        print("Sub Series Sku Number: ", mmy_sku_num)
        while len(mmy_sku_num) > 10:
            mmy_sku_num = mmy_sku_num[:-1]
            print("MMY SKU: ", mmy_sku_num)
        self.update_kit_sku(clicked_button, mmy_sku_num)


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


    # Handles logic for Series Child button clicks
    def handle_child_button_click(self):
        # TODO finish function logic to handle series child button clicks. 
        """
        This function handles events for series button clicks
        When no folders for the specified info exist if a series is active and the child button is clicked
        Folders for that specific series will be created in sequence. The button is then active
        Active buttons begin the processes of asset inputs into created folders on the right hand panel.
        """
        # BUG this logic should only fire if a parent series has been selected and activated
        
        if self.active_series_button:
            print("Parent Button: ", self.active_series_button.text())
            series = self.active_series_button.text()
            clicked_child = self.sender()
            kit_bundle = clicked_child.text()
            folders_created = False
            # Function calls for building, creating, and reading kit sku config files
            kit_sku_config = SeriesManager.handle_kit_config(self, series, kit_bundle)
            csv_path = create_kit_sku_config(kit_sku_config)

            # Load companion data from the current CSV
            companion_data = load_kit_sku_data(csv_path)
            print("Extracted Companion Data: ", companion_data)

            # Update active child state
            SeriesManager.active_child_button(self, clicked_child, series)

            sub_series_pieces = SeriesManager.handle_sub_series_pieces(self, kit_bundle)

            # Create folders if none exist
            series_path = os.path.join(self.parent_path, series)
            print("Series Path: ", series_path)
            (location, fabrication,
              material, package) = SeriesManager.create_sub_series_folders(self, sub_series_pieces)
            
            sub_series_path = series_path
            for folder in sub_series_pieces:
                sub_series_path = os.path.join(sub_series_path, folder)
            
                # Extracts sku data and update the current sku
                 # Calls Helper function to handle sku updates,
                self.sub_series_sku(clicked_child)

                # Call create sub series function while still in sub series list loop
                folders_created = SeriesManager.create_sub_series(self, sub_series_path)
            if folders_created == True:
                QMessageBox.information(self, "Success",
                                        f"Folders '{location}'; '{fabrication}'; '{material}'; '{package}'; Succesfully Created!")
            
            # Display file input widgets based on companion data
            self.companion_manager.create_file_input_widgets(companion_data)