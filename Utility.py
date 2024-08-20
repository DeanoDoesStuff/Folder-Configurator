# Utility.py
import csv
import os

config_folder = "Configs"

# Handles SERIES_CONFIG.csv file data
def load_series_data(csv_path):
    print("CSV Path:", csv_path)
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
        print(f"Error reading CSV file: {e}")
    return series_data

# Handles creation of kit sku config file if none exists
def create_kit_sku_config(kit_sku_config):
    print("\nconfig folder: ", config_folder)
    file_path = os.path.join(config_folder, kit_sku_config + ".csv")
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
        return file_path
    else:
        return file_path

# Loads kit sku config data if a file is found
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