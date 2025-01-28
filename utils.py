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
    

def read_csv(filename, num_subsystems):
    try:
        with open(filename, mode='r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                print(row[0:num_subsystems])
                yield row[0:num_subsystems]
    except FileNotFoundError:
        print("Error: File not found")