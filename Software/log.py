import json
import csv
from datetime import datetime
import numpy as np

def save_to_file(x, y=None, file_format="csv"):
    filename = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Ensure x is a 2D list where each sublist is a column
    if isinstance(x, np.ndarray):
        x = x.tolist()
    
    if isinstance(x[0], (int, float)):
        # x is 1D: make it a single-column table
        x = [x]
    elif isinstance(x[0], (list, tuple)):
        # x is list of rows: transpose it to columns
        x = list(map(list, zip(*x)))

    num_cols = len(x)
    num_rows = len(x[0])
    headers = [f"x{i+1}" for i in range(num_cols)]

    # Combine into rows for CSV writing
    data = [dict(zip(headers, [x[i][j] for i in range(num_cols)])) for j in range(num_rows)]

    # Add y if provided
    if y is not None:
        if isinstance(y, np.ndarray):
            y = y.tolist()
        if isinstance(y[0], (list, tuple)):
            y = list(map(list, zip(*y)))  # transpose
        if isinstance(y[0], (int, float)):
            y = [y]  # single column
        headers += [f"y{i+1}" for i in range(len(y))]
        for j in range(num_rows):
            for i, y_col in enumerate(y):
                data[j][f"y{i+1}"] = y_col[j]

    # Save
    if file_format.lower() == "csv":
        with open(f"{filename}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}.csv")
    elif file_format.lower() == "json":
        with open(f"{filename}.json", "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}.json")
    else:
        print("Invalid file format.")
