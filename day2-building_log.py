import csv
import random
from datetime import datetime, timedelta

def generate_building_entry_log(filename="building_entry_log.csv", max_rows=2500):
    """
    Generates a space-delimited CSV file simulating a building entry log.

    Args:
        filename (str, optional): The name of the output CSV file.
            Defaults to "building_entry_log.csv".
        max_rows (int, optional): The MAX number of rows to generate.
            Defaults to 2500.  
    """

    names = [
        "Alice", "Bob", "Charlie", "David", "Emily", "Frank", "Grace", "Henry",
        "Ivy", "Jack", "Katherine", "Liam", "Mia", "Noah", "Olivia", "Peter",
        "Quinn", "Ryan", "Sophia", "Thomas", "Ursula", "Victor", "Wendy", "Xavier",
        "Yara", "Zachary", "Abigail", "Benjamin", "Chloe", "Daniel", "Ella",
        "Finn", "Hannah", "Isaac", "Jasmine", "Kevin", "Lily", "Michael", "Natalie",
        "Owen", "Penelope", "Quentin", "Rebecca", "Samuel", "Taylor", "Uma",
        "Vincent", "Willow", "Xander", "Yasmine", "Zane", "Adam", "Beth", "Carl", "Diana",
        "Ethan", "Fiona", "George", "Hazel", "Ian", "Julia", "Kyle", "Lauren", "Mike", "Nancy"
    ]

    # Initialize list to track who is in the building, now storing entry times
    inside_building = {}  # {name: entry_time}
    rows = []
    current_time = datetime(2024, 1, 1, 8, 0)  # Start at 8:00 AM
    end_time = datetime(2024, 1, 1, 23, 0)  # End at 11:00 PM
    num_rows_generated = 0

    while current_time <= end_time and num_rows_generated < num_rows:  # Continue until end of day or max rows
        # Simulate events for this minute
        for _ in range(random.randint(0, 3)):  # 0-3 people enter or exit each minute
            name = random.choice(names)
            if not inside_building or random.random() < 0.6:  # 60% chance of entry if building is empty or not empty
                action = "enters"
                if name not in inside_building:
                    inside_building[name] = current_time  # Store entry time
                    rows.append({'time': current_time.strftime("%H:%M"), 'name': name, 'action': action})
                    num_rows_generated += 1
            elif inside_building:
                action = "exits"
                eligible_exitors = [p for p in inside_building if current_time >= inside_building[p] + timedelta(minutes=10)]
                if eligible_exitors:
                    exit_name = random.choice(eligible_exitors)
                    del inside_building[exit_name]  # Remove from inside_building
                    rows.append({'time': current_time.strftime("%H:%M"), 'name': exit_name, 'action': action})
                    num_rows_generated += 1
        current_time += timedelta(minutes=1)

    # Sort the rows by time
    rows.sort(key=lambda x: datetime.strptime(x['time'], '%H:%M'))

    # Write to CSV file, space delimited
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['time', 'name', 'action'], delimiter=' ')
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows of building entry log data and saved to {filename}")

if __name__ == '__main__':
    generate_building_entry_log()
