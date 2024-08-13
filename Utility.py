# Utility.py
import csv

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
                print("Row In CSV:", row)
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