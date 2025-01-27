import csv
from os.path import exists

def write_to_csv(filename, headers, data):
    
    # Check if the file already exists
    file_exists = exists(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write headers only if the file doesn't exist
        if not file_exists:
            writer.writerow(headers)

        # Write the data row
        writer.writerow(data)
