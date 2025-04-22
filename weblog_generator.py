import csv
import random
import time
from datetime import datetime, timedelta

def generate_simulated_web_log(num_rows, filename="simulated_web_log.csv"):
    """
    Generates a CSV file simulating web server logs with user session constraints.

    Args:
        num_rows (int): The number of rows to generate.
        filename (str, optional): The name of the CSV file to create.
            Defaults to "simulated_web_log.csv".
    """

    # Define possible values for the fields
    event_types = ["pageview", "click", "purchase"]
    click_event_names = [
        "add_to_cart", "view_product", "go_to_checkout",
        "proceed_to_payment", "confirm_order", "home_page_click",
        "search_button", "next_page", "previous_page", "promotion_banner"
    ]
    urls = [
        "/", "/products", "/checkout", "/cart", "/order_confirmation",
        "/login", "/register", "/search", "/category/electronics",
        "/category/clothing"
    ]

    # Initialize random seed for reproducibility
    random.seed(42)

    # Calculate start and end timestamps
    start_time = datetime(2025, 4, 1)
    end_time = datetime(2025, 4, 2)
    time_range = (end_time - start_time).total_seconds()

    # Define session-related variables
    user_sessions = {}
    user_purchase_state = {}

    # Function to generate a realistic user session
    def generate_user_session(user_id, previous_session=None):
        """Generates a list of events for a single user session, ensuring
        a logical order of events leading up to a potential purchase.

        Args:
            user_id (int): The ID of the user for whom to generate the session.
            previous_session (list, optional):  A list of events from a previous
                session for the same user.  If provided, the new session will
                start after the last event of the previous session.

        Returns:
            list: A list of dictionaries, where each dictionary represents an event
                  in the user session.
        """
        session = []
        if previous_session:
            # Start the new session shortly after the end of the previous one
            last_event_time = datetime.fromisoformat(previous_session[-1]["timestamp"])
            timestamp = last_event_time + timedelta(hours=random.uniform(2, 24))  # User returns 2-24 hours later
        else:
            timestamp = start_time + timedelta(seconds=random.uniform(0, time_range))
        url = random.choice(urls)
        session.append({
            "id": len(session) + 1,
            "user_id": user_id,
            "timestamp": timestamp.isoformat(),
            "event_type": "pageview",
            "event_name": "home_page" if url == "/" else "pageview",
            "url": url,
        })

        num_events = random.randint(3, 15)
        for _ in range(num_events):
            timestamp = session[-1]["timestamp"]
            timestamp_dt = datetime.fromisoformat(timestamp)
            timestamp = timestamp_dt + timedelta(seconds=random.uniform(1, 600))
            if timestamp > end_time:
                break

            event_type = random.choices(event_types, weights=[0.6, 0.3, 0.1])[0]
            event_name = ""
            url = session[-1]["url"]  # Default to the previous page's URL

            if event_type == "click":
                event_name = random.choice(click_event_names)
                if event_name == "add_to_cart":
                    #  add_to_cart happens on the current page.
                    pass
                elif event_name == "go_to_checkout":
                    url = "/cart"  # User goes to checkout
                elif event_name == "proceed_to_payment":
                    url = "/checkout"
                elif event_name == "confirm_order":
                    url = "/checkout"
            elif event_type == "purchase":
                if user_purchase_state.get(user_id, 0) >= 2:
                    event_name = "purchase_complete"
                    url = "/order_confirmation"
                else:
                    event_type = "pageview"
                    event_name = "pageview"
                    url = random.choice(urls)
            elif event_type == "pageview":
                event_name = "pageview" # set event name to pageview

            session.append({
                "id": len(session) + 1,
                "user_id": user_id,
                "timestamp": timestamp.isoformat(),
                "event_type": event_type,
                "event_name": event_name,
                "url": url,
            })
            if event_type == "click" and event_name == "add_to_cart":
                user_purchase_state[user_id] = 1
            elif event_type == "click" and event_name == "go_to_checkout":
                user_purchase_state[user_id] = 2
            elif event_type == "purchase" and event_name == "purchase_complete":
                user_purchase_state[user_id] = 3

        return session

    # Generate data rows
    rows = []
    user_sessions = {} # keep track of user sessions.
    user_purchase_state = {} # clear purchase state
    for i in range(num_rows):
        user_id = i // 100
        if user_id not in user_sessions:
            # Check for previous session data.
            user_sessions[user_id] = generate_user_session(user_id)
        # get the event based on the id.
        event_index = i % 100
        if event_index < len(user_sessions[user_id]):
          rows.append(user_sessions[user_id][event_index])
        else:
          # pad with a page view if the user session is shorter than expected.
          timestamp = end_time + timedelta(seconds=random.uniform(0, 600))
          rows.append({
                "id": i+1,
                "user_id": user_id,
                "timestamp": timestamp.isoformat(),
                "event_type": "pageview",
                "event_name": "pageview",
                "url":  random.choice(urls),
            })

    # Sort the rows by timestamp
    rows.sort(key=lambda x: x['timestamp'])

    # Write data to CSV file
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {num_rows} rows of simulated web log data and saved to {filename}")

if __name__ == "__main__":
    num_rows = 1000000
    generate_simulated_web_log(num_rows)

