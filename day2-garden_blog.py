import csv
import random
from datetime import datetime, timedelta

def generate_gardening_blog_log(filename="gardening_blog_log.csv", num_users=100, num_sessions_per_user=5, articles_per_session_min=1, articles_per_session_max=5):
    """
    Generates a CSV file simulating user browsing on a gardening blog.

    Args:
        filename (str, optional): The name of the output CSV file.
            Defaults to "gardening_blog_log.csv".
        num_users (int, optional): The number of unique users. Defaults to 100.
        num_sessions_per_user (int, optional): The average number of sessions per user. Defaults to 1.
        articles_per_session_min (int, optional): Minimum articles read per session. Defaults to 1.
        articles_per_session_max (int, optional): Maximum articles read per session. Defaults to 5.
    """

    articles = [
        "/how-to-grow-tomatoes",
        "/best-flowers-for-spring",
        "/organic-pest-control-tips",
        "/creating-a-raised-garden-bed",
        "/soil-types-and-amendments",
        "/watering-guide-for-beginners",
        "/pruning-roses-for-maximum-blooms",
        "/growing-herbs-indoors",
        "/composting-101",
        "/dealing-with-garden-pests",
        "/fall-garden-cleanup",
        "/winter-garden-prep",
        "/attracting-pollinators-to-your-garden",
        "/guide-to-companion-planting",
        "/troubleshooting-common-plant-diseases",
        "/gardening-tools-essentials",
        "/seed-starting-indoors",
        "/growing-succulents-and-cacti",
        "/vertical-gardening-ideas",
        "/hydroponics-for-home-gardeners"
    ]

    rows = []
    start_date = datetime(2025, 4, 1, 0, 0)  # Start at 8:00 AM
    end_date = datetime(2025, 4, 1, 23, 55)    # End at 8:00 PM.  (simulate most activity during the day)
    total_seconds = (end_date - start_date).total_seconds()

    for user_id in range(1, num_users + 1):
        # Simulate multiple sessions per user
        num_user_sessions = random.randint(1, num_sessions_per_user) # Each user has at least one session
        for session in range(num_user_sessions):
            # Stagger user sessions throughout the day
            session_start_time = start_date + timedelta(seconds=random.uniform(0, total_seconds))
            current_time = session_start_time

            num_articles = random.randint(articles_per_session_min, articles_per_session_max)
            articles_read = random.choices(articles, k=num_articles)

            for article_url in articles_read:
                # Simulate time on page with high variation (30s to 5 minutes)
                time_on_page = random.expovariate(1/120)  # Average: 120 seconds (2 minutes)
                time_on_page = max(30, min(time_on_page, 300))  # Ensure between 30s and 300s (5 minutes)
                current_time += timedelta(seconds=time_on_page)
                rows.append({
                    "timestamp": current_time.isoformat(),
                    "user_id": user_id,
                    "page_url": article_url
                })

            # Simulate a short break between articles within a session
            if num_articles > 1:
                current_time += timedelta(seconds=random.randint(10, 60))

    # Sort the rows by timestamp
    rows.sort(key=lambda x: x['timestamp'])

    # Write to CSV file
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "user_id", "page_url"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated browsing log data and saved to {filename}")

if __name__ == "__main__":
    generate_gardening_blog_log()

