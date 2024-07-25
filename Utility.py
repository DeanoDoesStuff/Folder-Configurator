import csv
from collections import defaultdict

def load_series_data(csv_path):
    series_data = defaultdict(lambda: defaultdict(set))  # Store unique values in sets
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames  # Get the headers from the CSV
            print("CSV Headers:", headers)  # Debugging: Print headers

            # Clean header names by stripping leading and trailing spaces
            cleaned_headers = [header.strip() for header in headers]

            for row in reader:
                # Access row data using cleaned headers
                series = row.get(cleaned_headers[0], "").strip()  # 'SERIES'
                location = row.get(cleaned_headers[1], "").strip()  # 'LOCATION'
                fabrication = row.get(cleaned_headers[2], "").strip()  # 'FABRICATION'
                material = row.get(cleaned_headers[3], "").strip()  # 'MATERIAL'
                package = row.get(cleaned_headers[4], "").strip()  # 'PACKAGE'

                # Store unique values in sets
                series_data[series]['LOCATION'].add(location)
                series_data[series]['FABRICATION'].add(fabrication)
                series_data[series]['MATERIAL'].add(material)
                series_data[series]['PACKAGE'].add(package)

    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return series_data
