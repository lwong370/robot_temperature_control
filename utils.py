import csv
import time
from os.path import exists

def check_valid_input(prompt, expected_type):
    while True:
        try:
            user_input = expected_type(input(prompt))
            return user_input
        except ValueError:
            print(f"\nInput not valid. Please try again. ")
        except EOFError:
            print(f"\nNo input given. Please try again. ")


def is_invalid_number(value):
    try:
        float_value = float(value)
        return float_value <= 0
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