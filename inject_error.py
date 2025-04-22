import csv
import random
from datetime import datetime, timedelta
import copy

def introduce_errors(input_filename, output_filename):
    """
    Reads a CSV file of web server logs, introduces errors, and writes the
    modified data to a new CSV file.

    Args:
        input_filename (str): The name of the input CSV file.
        output_filename (str): The name of the output CSV file.
    """

    def corrupt_url(url):
        """
        Randomly introduces errors into a URL.

        Args:
            url (str): The URL to corrupt.

        Returns:
            str: The corrupted URL.
        """
        if random.random() < 0.1:  # 10% chance of corruption
            error_type = random.randint(1, 3)
            if error_type == 1:  # Add a typo
                if len(url) > 1:
                    index = random.randint(0, len(url) - 1)
                    char = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                    url = url[:index] + char + url[index + 1:]
            elif error_type == 2:  # Add extraneous characters
                num_chars = random.randint(1, 3)
                extra_chars = ''.join(random.choice('!@#$%^&*()_-+={}[]|;:<>,.?/~') for _ in range(num_chars))
                position = random.randint(0, len(url))
                url = url[:position] + extra_chars + url[position:]
            elif error_type == 3: # remove some characters
                if len(url) > 3:
                    num_chars = random.randint(1, 3)
                    start_pos = random.randint(0, len(url) - num_chars)
                    url = url[:start_pos] + url[start_pos+num_chars:]
            return url
        else:
            return url

    rows = []
    with open(input_filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        if not reader.fieldnames:
            print("Error: Input CSV file is empty or has no headers.")
            return
        rows = list(reader) # read all the rows

    new_rows = []
    for row in rows:
        # Introduce errors
        new_row = copy.deepcopy(row) # Create a copy to avoid modifying the original row

        if random.random() < 0.02:  # 2% chance of dropping an event
            continue  # Skip adding this row (drop event)

        if random.random() < 0.05:  # 5% chance of duplicating a click event
            if new_row["event_type"] == "click":
                num_duplicates = random.randint(1, 2)  # Duplicate 1 or 2 times
                for _ in range(num_duplicates):
                    duplicate_row = copy.deepcopy(new_row)
                    # slightly modify the timestamp to distinguish duplicates
                    timestamp_dt = datetime.fromisoformat(duplicate_row["timestamp"])
                    duplicate_row["timestamp"] = (timestamp_dt + timedelta(seconds=random.randint(1, 5))).isoformat()
                    new_rows.append(duplicate_row)

        new_row["url"] = corrupt_url(new_row["url"])  # Corrupt URL

        if random.random() < 0.025:  # 2.5% chance of delaying timestamp
            timestamp_dt = datetime.fromisoformat(new_row["timestamp"])
            delay_seconds = random.randint(1, 300)  # Delay by up to 5 minutes (300 seconds)
            new_row["timestamp"] = (timestamp_dt + timedelta(seconds=delay_seconds)).isoformat()

        new_rows.append(new_row)

    # Write the modified data to a new CSV file
    with open(output_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(new_rows)

    print(f"Errors introduced and saved to {output_filename}")

if __name__ == "__main__":
    input_filename = "simulated_web_log.csv"  # Replace with your input filename
    output_filename = "error_injected_web_log.csv"  # Choose an output filename
    introduce_errors(input_filename, output_filename)

