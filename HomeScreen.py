#HomeScreen.py
import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QCheckBox,
                             QMessageBox, QSplitter, QHBoxLayout, QLabel, QScrollArea)
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

        # Load series data from CSV file
        self.series_data = load_series_data('Configs/SERIES_CONFIG.csv')
        
        # Initialize SeriesManager
        self.series_buttons = []
        self.series_labels = {}
        self.series_checkboxes = {}
        self.series_manager = SeriesManager(
            root_dir = self.root_dir, 
            series_buttons = self.series_buttons, 
            series_data = self.series_data, 
            series_labels = self.series_labels, 
            series_checkboxes = self.series_checkboxes, 
            current_mmy_path=""
        )
        
        # Load and display series buttons
        self.load_series_buttons()  # Load series buttons

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

    # Handles signals from items clicked in Folder Tree
    def handle_tree_item_click(self, item):
        self.update_folder_type(item)
        depth = self.tree_widget.get_item_depth(item)
        if depth == 3:
            current_mmy_path = self.tree_widget.get_item_path(item)
            self.series_manager.enable_series_buttons(True, current_mmy_path)
            self.series_manager.update_series_button_states(item)
            self.update_header_visibility()

        elif depth > 3:
            current_mmy_path = self.tree_widget.get_item_path(item)
            print("Current Tree Item Path: ", current_mmy_path)
            self.series_manager.enable_series_buttons(True, current_mmy_path)
            self.series_manager.update_active_series(item, current_mmy_path)
            self.update_header_visibility()

        return depth

    # Handles tracking of selected folder type by calculating depth
    def update_folder_type(self, item):
        current_sku = ""
        if item:
            depth = self.tree_widget.get_item_depth(item)

            (make_id, model_id, year_id, series_id,
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
                current_sku = make_id + model_id + year_id + series_id + fab_id
            elif depth ==6:
                self.folder_type = " MATERIAL"
                current_sku = make_id + model_id + year_id + series_id + fab_id + mat_id
            elif depth == 7:
                self.folder_type = " PACKAGE"
                current_sku = make_id + model_id + year_id + series_id + fab_id + mat_id + package_id
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
        self.series_labels = {}
        self.series_checkboxes = {}

        series_keys = list(self.series_data.keys())

        for series in series_keys:
            print(f"Series {series} added to button")
            button = QPushButton(series)
            button.setStyleSheet("background-color: #C63F3F; color: white;")
            button.setEnabled(False)
            button.setVisible(False)
            button.clicked.connect(self.handle_series_button_click)
            self.middle_layout.addWidget(button)
            self.series_buttons.append(button)

            headers_layout = QVBoxLayout()

            for header in ["LOCATION", "FABRICATION", "MATERIAL", "PACKAGE"]:
                header_label = QLabel(header)
                header_label.setVisible(True)
                headers_layout.addWidget(header_label)
                header_style = SeriesManager.header_styles(header)
                header_label.setStyleSheet(header_style)

                checkbox_layout = QVBoxLayout()
                checkboxes = []
                for item in sorted(self.series_data[series][header]):
                    checkbox = QCheckBox(item)
                    checkbox.setVisible(True)
                    checkbox_layout.addWidget(checkbox)
                    checkboxes.append(checkbox)
                
                headers_layout.addLayout(checkbox_layout)
                self.series_labels[header] = header_label
                self.series_checkboxes[header] = checkboxes
            
            self.middle_layout.addLayout(headers_layout)
        
        self.series_manager.series_buttons = self.series_buttons
        self.series_manager.series_labels = self.series_labels
        self.series_manager.series_checkboxes = self.series_checkboxes

    # Handle signal emit when series button is clicked
    def handle_series_button_click(self):
        clicked_button = self.sender()
        series = clicked_button.text()
        print(f"Series: {series}")
        
        if self.active_series_button:
            self.active_series_button.setStyleSheet("background-color: #0B8ED4; color: white;")
        self.active_series_button = clicked_button
        clicked_button.setStyleSheet("background-color: #2E982B; color: white;")

        selected_item = self.tree_widget.currentItem() # Get selected item name from Tree
        parent_path = self.tree_widget.get_item_path(selected_item)
        print(f"Parent path: {parent_path}")

        item_depth = self.tree_widget.get_item_depth(selected_item) # Get selected item depth from Tree
        print("Selected Item Depth: ", item_depth)
        
        new_folder_path = os.path.join(parent_path, series)
        print("New Folder Path: ", new_folder_path)

        # TODO check depth when entering function, if beyond year, alter behavior
        if item_depth >= 4:
            if os.path.exists(parent_path):
                print(f"Folder Exists for Series: {series}")
                print(f"Folder Path: ", parent_path)

        else:
            # Check if newly created path already exists in the directory
            if not os.path.exists(new_folder_path):
                print("No folder exists yet for this series")
                if self.folder_manager.create_folder(new_folder_path):
                    print("New Folder Path: ", new_folder_path)
                    QMessageBox.information(self, "Success", f"Series folder '{series}' created successfully.")
                    self.tree_widget.expandItem(selected_item) # Ensure the newly created folder is visible
                    clicked_button.setStyleSheet("background-color: lightgreen; color: black;")  # Change to light green
                else:
                    QMessageBox.warning(self, "Error", f"Failed to create series folder '{series}'.")               

        self.update_header_visibility()

    # Handles when label headers are visible in the window
    def update_header_visibility(self):
        for series in self.series_data.keys():
            if series in self.series_labels:
                headers = self.series_labels[series]
                for header, label in headers.items():
                    label.setVisible(True)
                    checkboxes = self.series_checkboxes[series][header]
                    for checkbox in checkboxes:
                        checkbox.setVisible(True)
