# Utility.py
import csv
import os

class Utility:
    config_folder = "Configs"
    custom_config_folder = os.path.join(config_folder, "CUSTOM")
    universal_config_folder = os.path.join(config_folder, "UNIVERSAL")

    def __init__(self):
        # Optionally initialize any attributes
        pass

    @staticmethod
    def load_series_data(csv_path):
        series_data = {}  # Use a regular dictionary to store lists of row values
        try:
            with open(csv_path, 'r') as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames  # Get the headers from the CSV

                # Clean header names by stripping leading and trailing spaces
                cleaned_headers = [header.strip() for header in headers]

                for row in reader:
                    # Access row data using cleaned headers
                    series = row.get(cleaned_headers[0], "").strip()  # 'SERIES'
                    location = row.get(cleaned_headers[1], "").strip()  # 'LOCATION'
                    fabrication = row.get(cleaned_headers[2], "").strip()  # 'FABRICATION'
                    material = row.get(cleaned_headers[3], "").strip()  # 'MATERIAL'
                    package = row.get(cleaned_headers[4], "").strip()  # 'PACKAGE'

                    # Combine row data into a list
                    row_values = [location, fabrication, material, package]

                    # Initialize the list if it doesn't exist for the series key
                    if series not in series_data:
                        series_data[series] = []

                    # Append combined row values to the list for the corresponding series
                    series_data[series].append(row_values)

        except Exception as e:
            print(f"Error reading CSV file: {e}") # Exception Output Statement. Please leave in place.
        return series_data

    @staticmethod
    def create_kit_sku_config(kit_sku_config, series):
        # Stop to check if custom folder exists inside of config
        if not os.path.exists(Utility.custom_config_folder):
            os.makedirs(Utility.custom_config_folder)

        # Build series folder
        custom_config_series_folder  = os.path.join(Utility.custom_config_folder, series)
        print("Custom Config Series Folder: ", custom_config_series_folder)
        if not os.path.exists(custom_config_series_folder):
            os.makedirs(custom_config_series_folder)

        file_path = os.path.join(custom_config_series_folder, kit_sku_config + ".csv")

        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
            return file_path
        else:
            return file_path

    @staticmethod
    def load_kit_sku_data(csv_path):

        companion_data = {}  # Initialize dictionary to store companion data
        try:
            with open(csv_path, mode='r') as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames

                cleaned_headers = [header.strip() for header in headers]

                for row in reader:
                    # Access row data using cleaned headers
                    companion = row.get(cleaned_headers[0], "").strip()  # 'COMPANION'
                    selection1 = row.get(cleaned_headers[1], "").strip()  # Selection_1
                    selection2 = row.get(cleaned_headers[2], "").strip()  # Selection_2
                    type_var = row.get(cleaned_headers[3], "").strip()  # Type-Variable
                    location = row.get(cleaned_headers[4], "").strip()  # Location
                    group = row.get(cleaned_headers[5], "").strip()  # Group-ID

                    # Create a tuple or list of row values
                    companion_row_values = (selection1, selection2, type_var, location, group)

                    # Initialize the list if it doesn't exist for the companion key
                    if companion not in companion_data:
                        companion_data[companion] = []

                    # Append row values as a tuple to the list for the corresponding companion
                    companion_data[companion].append(companion_row_values)

        except Exception as e:
            print(f"Error reading CSV file: {e}")

        return companion_data

    @staticmethod
    def create_uni_config(series, kit_sku_config, sub_series_pieces):
        if sub_series_pieces:
            location = sub_series_pieces[0]
            fabrication = sub_series_pieces[1]
            material = sub_series_pieces[2]
            package = sub_series_pieces[3]
        # Build out folder for current UNI Series
        current_uni_series = os.path.join(Utility.universal_config_folder, series)
        if not os.path.exists(current_uni_series):
            os.makedirs(current_uni_series) # builds folders from Configs/Universal/-Current Series-

        # Build out folders for current UNI Sub Series
        current_uni_sub_series = os.path.join(current_uni_series, location, fabrication)
        if not os.path.exists(current_uni_sub_series):
            # Builds deepest level sub folder, all UNI assets for this Product SKU go here
            os.makedirs(current_uni_sub_series)

        # TODO build out files for UNI assets per Series/Sub Series
        csv_file_path = os.path.join(current_uni_sub_series, kit_sku_config + ".csv")
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)

        uni_center_file = os.path.join(current_uni_sub_series, "UNI_CENTERS" + ".csv")
        if not os.path.exists(uni_center_file):
            with open(uni_center_file, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)

            return csv_file_path, uni_center_file
        else:
            return csv_file_path, uni_center_file
   

    @staticmethod
    def load_uni_config(uni_csv_path):
        # Logic to handle loading in UNI part groups, or centers into a list for comprehension and alteration
        uni_groups_list = []
        try:
            with open(uni_csv_path, mode='r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row:
                        uni_groups_list.append(row[0])
            return uni_groups_list
        except FileNotFoundError:
            print("File not found:", uni_csv_path)

    @staticmethod
    def set_uni_centers():
        print("Set UNI Centers")

