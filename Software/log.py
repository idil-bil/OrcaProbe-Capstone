import json
import csv
from datetime import datetime

# Save lists x and y to a file in the specified format (CSV or JSON) with a timestamped filename
def save_to_file(x, y, file_format):
    """
    Parameters:
    - x: list of values for x (e.g., independent variable data or timestamps)
    - y: list of values for y (e.g., dependent variable data or measurements)
    - file_format: "csv" or "json" (default is "csv")
    
    Returns:
    - None
    """
    filename = datetime.now().strftime("%Y%m%d_%H%M%S")                 # Set filename to the current date and time in "YYYYMMDD_HHMMSS" format
    
    data = [{"x": x_val, "y": y_val} for x_val, y_val in zip(x, y)]     # Combine x and y into a list of dictionaries for easier saving
    
    # Save as CSV file
    if file_format.lower() == "csv":                                    
        with open(f"{filename}.csv", "w", newline="") as csv_file:      # Open the file in write mode with f"{filename}.json" to save with .json extension
            writer = csv.DictWriter(csv_file, fieldnames=["x", "y"])    # Initialize a DictWriter to write "x" and "y" as column headers
            writer.writeheader()                                        # Write headers to the CSV file
            writer.writerows(data)                                      # Combine x and y into a list of dictionaries for easier saving
        print(f"Data saved to {filename}.csv")                          

    # Save as JSON file
    elif file_format.lower() == "json":                                 
        with open(f"{filename}.json", "w") as json_file:                # Open the file in write mode with f"{filename}.json" to save with .json extension
            json.dump(data, json_file, indent=4)                        # Write the data list with an indentation of 4 spaces for readability
        print(f"Data saved to {filename}.json")
    
    # Handle invalid file format input
    else:
        print("Invalid file format. Choose either 'csv' or 'json'.")

# Example usage:
x = [1, 2, 3, 4]
y = [10, 20, 30, 40]
save_to_file(x, y, file_format="json")