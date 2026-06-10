import os
import csv
from datetime import datetime

# Define the relative path to our CSV storage file
CSV_PATH = os.path.join("data", "violations.csv")

def log_violation(violation_type):
    """
    Appends a detected violation to the CSV log file with a current timestamp.
    
    Args:
        violation_type (str): The description of the violation (e.g., "Mobile Phone Detected").
    """
    # Generate a readable timestamp (e.g., "2026-06-10 03:45:30 PM")
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    
    # Safety check: if the file was accidentally deleted, we note that it needs headers
    file_exists = os.path.isfile(CSV_PATH)
    
    try:
        # Open the file in 'append' mode ('a'). 
        # newline='' prevents blank lines between rows in Windows.
        with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # If the file didn't exist, write the header row first
            if not file_exists:
                writer.writerow(["Timestamp", "Violation Type"])
                
            # Write the actual log data
            writer.writerow([timestamp, violation_type])
            
        return True
    except Exception as e:
        # If the file is locked by another program (like Excel), fail gracefully
        print(f"Error writing to log file: {e}")
        return False