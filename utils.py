import csv
import time
from os.path import exists

def is_invalid_number(value, invalid_include_zero=False):
    try:
        float_value = float(value)
        return float_value <= 0 if invalid_include_zero else float_value < 0
    except ValueError:
        return True

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