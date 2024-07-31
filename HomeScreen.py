#HomeScreen.py

import os
from collections import defaultdict
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QCheckBox, QLineEdit, QPushButton, 
                            QMessageBox, QSplitter, QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from FolderManager import FolderManager
from FolderTree import FolderTree
from SkuBuilder import SkuBuilder
from SeriesManager import SeriesManager
from Utility import load_series_data

class HomeScreen(QMainWindow):
    def __init__(self, root_dir, folder_type, parent=None):
        super().__init__()

        self.root_dir = root_dir
        self.folder_type = folder_type
        self.parent = parent
        self.sku_builder = SkuBuilder()
        self.setWindowTitle("Folder Manager")
        self.setGeometry(100, 100, 1920, 1080)

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
        
        # Middle Widget for Series options
        self.middle_widget = QWidget()
        self.middle_layout = QVBoxLayout()
        self.middle_widget.setLayout(self.middle_layout)
        self.splitter.addWidget(self.middle_widget)

        # Load and display series buttons
        self.series_data = load_series_data('Configs/SERIES_CONFIG.csv')  # Updated with the actual path to the CSV file
        self.load_series_buttons()  # Load series buttons

        # TODO finish refactoring new SeriesManager file
        # Initialize SeriesManager
        self.series_manager = SeriesManager(root_dir, self.series_buttons)

        # Tree Widget
        self.tree_widget = FolderTree(self.root_dir, self.folder_manager, self.series_manager, self)
        self.tree_widget.itemClicked.connect(self.handle_tree_item_click)
        self.tree_widget.empty_space_clicked.connect(self.reset_folder_type) # Connect to empty space signal 
        self.left_layout.addWidget(self.tree_widget)
        
        # Input for a new folder
        self.new_folder_input = QLineEdit()
        print("Folder Type: ", folder_type)
        self.new_folder_input.setPlaceholderText(f"Enter new {self.folder_type}")
        self.left_layout.addWidget(self.new_folder_input)

        # Button for creating a new folder
        self.create_folder_button = QPushButton("Create Folder") # TODO update the button text for folder_type
        self.create_folder_button.clicked.connect(self.create_new_folder)
        # Styles for create folder button found beneath the Tree
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
        # Add Create folder button to the left layout
        self.left_layout.addWidget(self.create_folder_button)

        # Button for deleting a selected folder
        self.delete_folder_button = QPushButton("Delete Folder")
        self.delete_folder_button.clicked.connect(self.delete_folder)
        self.delete_folder_button.setStyleSheet("background-color: #C63F3F; color: white;")
        self.left_layout.addWidget(self.delete_folder_button)

        # Right Widget (Nothing here yet, but for testing)
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_widget.setLayout(self.right_layout)

        # Example of adding a button to the right widget
        self.example_button = QPushButton("Example Button") # Example for showing location of right layout
        self.right_layout.addWidget(self.example_button)

        # Add a QLabel for displaying the SKU
        self.sku_label = QLabel("Current SKU: ")
        self.right_layout.addWidget(self.sku_label)

        # Add right widget to splitter
        self.splitter.addWidget(self.right_widget)

        # Create Series Widget
        self.series_widget = QWidget()
        self.series_layout = QVBoxLayout()
        self.series_widget.setLayout(self.series_layout)
        self.splitter.addWidget(self.series_widget)

        # Set initial sizes for the splitter (optional)
        self.splitter.setSizes([200, 400, 600])  # Set the initial size for the left and right widgets

        # Initialize folder type and button state
        self.update_folder_type(self.tree_widget.currentItem())

        # Track the active series button
        self.active_series_button = None
        

    def handle_tree_item_click(self, item):
        self.update_folder_type(item) # Updates folder type with current active item in Tree
        depth = self.tree_widget.get_item_depth(item) # Calls FolderTree function to find depth
        if depth >= 3: # Year or deeper is selected
            self.enable_series_buttons(True) # Series Buttons become active when at year or deeper
            self.series_manager.update_series_button_states(item) # Call update button state passing in current selection
            self.update_header_visibility() # Updates current header style
        else:
            self.enable_series_buttons(False)
            # Reset active series buttons when no year is selected
            if self.active_series_button:
                self.active_series_button.setStyleSheet("background-color: grey; color: white")
                self.active_series_button = None
            self.update_header_visibility()

    # Handle active button style    
    def highlight_active_series_button(self):
        if self.active_series_button:
            self.active_series_button.setStyleSheet("background-color: green; color: white;")

    # Handle series button activation
    def enable_series_buttons(self, enable):
        for button in self.series_buttons:
            button.setEnabled(enable)
            button.setVisible(enable)

    # Handle folder type and SKU dependant on current active item in Tree
    def update_folder_type(self, item):
        current_sku = ""
        if item:
            depth = self.tree_widget.get_item_depth(item)

            # Call SkuBuilder for the given depth
            make_id, model_id, year_id, series_id = self.sku_builder.process_depth(item, depth)
            if depth == 0: # Nothing is selected SKU is NULL
                self.folder_type = " Make"
            elif depth == 1:
                self.folder_type = " Model"
                # Make or deeper has been selected Make ID extracted
                current_sku = make_id
            elif depth == 2:
                self.folder_type = " Year"
                # Model or deeper has been selected Make and Model ID extracted
                current_sku = make_id + model_id
            elif depth == 3:
                self.folder_type = " SERIES"
                # Year has been selected, all MMY SKU ID's have been extracted
                current_sku = make_id + model_id + year_id
            elif depth == 4:
                # Series has been selected, update SKU
                self.folder_type = " LOCATION"
                current_sku = make_id + model_id + year_id + series_id
            else:
                self.folder_type = " None"
                current_sku = self.make_id # Base SKU
            # Update UI elements
            if depth < 3:
                # Set placeholder text if make or model depth selected
                self.new_folder_input.setPlaceholderText(f"Enter new{self.folder_type}")
            else:
                # Empty Text if year is selected
                self.new_folder_input.setPlaceholderText("")
            self.create_folder_button.setEnabled(self.folder_type != " None")
            self.create_folder_button.setEnabled(self.folder_type != " SERIES")
            # Update SKU label
            self.update_sku_label(current_sku)
            
    # Handles folder creation regardless of depth
    def create_new_folder(self):
        new_folder_name = self.new_folder_input.text().strip()
        if new_folder_name:
            # Folder name extracted from value of item being clicked in Tree
            selected_item = self.tree_widget.currentItem() 
            if selected_item:
                parent_path = self.tree_widget.get_item_path(selected_item)
            else:
                parent_path = self.root_dir

            # Join current selected item to parent path
            new_folder_path = os.path.join(parent_path, new_folder_name) 

            expanded_state = self.tree_widget.save_expanded_state() # Ensure Tree stays expanded
            selected_item_path = self.tree_widget.save_selected_item()
            print("Folder Path: ", selected_item_path) # Debug print statement
            if self.folder_manager.create_folder(new_folder_path):
                self.new_folder_input.clear()
                QMessageBox.information(self, "Success", f"Folder '{new_folder_name}' created successfully.")
                
                self.tree_widget.restore_expanded_state(expanded_state)
                self.tree_widget.restore_selected_item(selected_item_path)
                self.tree_widget.refresh_tree()
            else:
                QMessageBox.information(self, "Warning", f"Folder '{new_folder_name}' already exists.")

    # Handles folder deletion regardless of depth
    def delete_folder(self):
        selected_item = self.tree_widget.currentItem()
        if selected_item: # If an item in Tree is selected
            # Gets item path and sets folder path to that value
            folder_path = self.tree_widget.get_item_path(selected_item)
            reply = QMessageBox.question(self, "Delete Folder", f"Are you sure you want to delete '{selected_item.text(0)}'?", 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes: # If User selects yes in Modal
                if self.folder_manager.delete_folder(folder_path): # Ensures folder deletion
                    QMessageBox.information(self, "Success", f"Folder '{selected_item.text(0)}' deleted successfully.")
                    self.tree_widget.refresh_tree()
                    # Reset folder tree selections and collapse it
                    self.tree_widget.collapseAll()
                    self.tree_widget.clearSelection()
                else:
                    QMessageBox.warning(self, "Error", f"Failed to delete folder '{selected_item.text(0)}'. It might not be empty.")
    
    # Handles sku label value being displayed
    def update_sku_label(self, sku): 
        self.sku_label.setText(f"Current SKU: {sku}") # Assign SKU value to sku label widget
    
    # Handles folder type reset back to default state
    def reset_folder_type(self):
        print("Folder type reset: ")
        self.folder_type = " Make"
        self.new_folder_input.setPlaceholderText(f"Enter new {self.folder_type}")
        self.create_folder_button.setEnabled(True)
        self.update_sku_label("")
        self.enable_series_buttons(False)
        # Ensure folder tree is updated
        self.tree_widget.refresh_tree()
    
    # Handles assignment of series buttons and children labels
    def load_series_buttons(self): # TODO finish checkbox state check and folder creation
        self.series_buttons = [] # Empty list to hold series buttons
        self.series_labels = {} # Empty dict to hold child series labels

        # Create Series buttons and update visual state for active button
        for series in self.series_data:
            button = QPushButton(series) # Creates series button
            button.setStyleSheet("background-color: #FF474C ; color: white;")  # Initial red color if no series folder exists
            button.setEnabled(False) # Initially disable series buttons
            button.setVisible(False) # Initially hide series buttons
            button.clicked.connect(self.handle_series_button_click)
            self.middle_layout.addWidget(button)
            self.series_buttons.append(button) # Store series button in a list for access later
            print(f"Button for series '{series}' created and connected.")
            # Create a horizontal layour for headers
            headers_layout = QHBoxLayout()
            
            # Create a QLabel for the location headers
            location_label = QLabel("LOCATION")
            location_label.setVisible(False) # Initially hidden
            headers_layout.addWidget(location_label)

            # Create a QLabel for the fabrication headers
            fabrication_label = QLabel("FABRICATION")
            fabrication_label.setVisible(False) # Initially hidden
            headers_layout.addWidget(fabrication_label)

            # Create a QLabel for the material headers
            material_label = QLabel("MATERIAL")
            material_label.setVisible(False) # Initially hidden
            headers_layout.addWidget(material_label)

            # Create a QLabel for the package headers
            package_label = QLabel("PACKAGE")
            package_label.setVisible(False) # Initially hidden
            headers_layout.addWidget(package_label)

            # Add the horizontal layout to the middle layout
            self.middle_layout.addLayout(headers_layout)
            # Store location labels in dictionary
            self.series_labels[series] = (location_label, fabrication_label, material_label, package_label)

    # Handles header styles
    def update_header_visibility(self):
        selected_item = self.tree_widget.currentItem()
        depth = self.tree_widget.get_item_depth(selected_item)
        
        style = """
            background-color: #3b3b3b;
            color: white;
            padding: 2px 5px;
            border: 1px solid #d0d0d0;
        """
        # TODO more styles need to be created for labels that have  
        # Show or hide headers based on the selection depth
        if depth >= 3:  # Ensure we have a valid year or deeper selection
            for button in self.series_buttons:
                series = button.text()
                location_label, fabrication_label, material_label, package_label = self.series_labels.get(series, (None, None, None, None))
                if location_label: # TODO each label needs to have style change if check boxes are selected
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
            # Hide all headers if no valid year or deeper selection
            for labels in self.series_labels.values():
                for label in labels:
                    label.setVisible(False)

    # Function to pass signals when series buttons or their children are clicked
    def handle_series_button_click(self):
        print("Series button clicked")
        sender = self.sender()
        series = sender.text()
        print(f"Series: {series}")

        selected_item = self.tree_widget.currentItem()
        if not selected_item:
            print("No item was selected")
            return
        
        depth = self.tree_widget.get_item_depth(selected_item) # Fetches current item depth
        print(f"Selected item depth: {depth}") # Debug print statement to display current depth
        if depth != 3: # Error handling block, although this even should never happen
            print("Selected item is not at depth 3.")
            QMessageBox.warning(self, "Error", "Please select a year folder to create a Series.")
            return
        # Get current parent of selected item directory path
        parent_path = self.tree_widget.get_item_path(selected_item) 
        print(f"Parent path: {parent_path}") # Debug statement to display current path
        new_folder_path = os.path.join(parent_path, series) # Merges parent path with item path
        print("new folder path: ", new_folder_path) # Debug statement to display newly created path
        # Check if newly created path already exists in directory
        if not os.path.exists(new_folder_path):
            print("No folder exists yet for this series") # Debug statement when no existing folder exists
            if self.folder_manager.create_folder(new_folder_path): 
                print("New folder path: ", new_folder_path)
                QMessageBox.information(self, "Success", f"Series folder '{series}' created successfully.")
                self.tree_widget.expandItem(selected_item) # Ensure the newly created folder is visible
                sender.setStyleSheet("background-color: lightgreen; color: black;")  # Change to light green
            else:
                QMessageBox.warning(self, "Error", f"Failed to create series folder '{series}'.")

        # Change the color of the active button
        if self.active_series_button:
            self.active_series_button.setStyleSheet("background-color: lightgreen; color: black;")
        sender.setStyleSheet("background-color: green; color: white;")
        self.active_series_button = sender
        self.update_header_visibility()
