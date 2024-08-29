import requests
import json
from datetime import datetime, timedelta
import time
import pytz
import os

def fetch_and_save_data():
    # API URL and token
    api_url = "https://api.benzinga.com/api/v1/analyst/insights"
    token = "4c506ca1df2a42a6b3b9c815de5688ef"

    # Send API request with token as query parameter
    querystring = {"token": token,"pageSize": 1000}
    response = requests.request("GET", api_url, params=querystring)

    # Check if the request was successful
    if response.status_code == 200:
        # Clean up the data
        data = response.json()
        cleaned_data = clean_data(data)

        # Set the timezone to US/Eastern
        us_tz = pytz.timezone('US/Eastern')
        us_now = datetime.now(tz=us_tz)

        # Create the /data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)

        # Save data to a JSON file with filename based on US/Eastern timezone
        filename = f"data/{us_now.strftime('%Y-%m-%d')}.json"
        with open(filename, "w") as file:
            json.dump(cleaned_data, file, indent=4)

        print(f"Data saved to {filename}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def clean_data(data):
    # Set the timezone to US/Eastern
    us_tz = pytz.timezone('US/Eastern')

    # Get the current date and time in the US timezone
    us_now = datetime.now(tz=us_tz)
    us_current_date = us_now.date()

    filtered_data = []
    for rating in data["analyst-insights"]:
        rating_date = datetime.fromisoformat(rating["date"]).date()
        if rating_date == us_current_date:
            filtered_data.append(rating)
    return filtered_data

# Initial call to fetch and save data
fetch_and_save_data()

# Repeat the process every 24 hours
while True:
    next_run = datetime.now() + timedelta(days=1)
    time_to_sleep = (next_run - datetime.now()).total_seconds()
    print(f"Sleeping for {time_to_sleep} seconds until the next run.")
    time.sleep(time_to_sleep)
    fetch_and_save_data()