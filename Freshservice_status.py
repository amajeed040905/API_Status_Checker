# Freshservice Status Monitor
# Made by Ammar Majeed for CFSB on 8/1/25
#
# DESCRIPTION:
# This script checks the freshservice JSON endpoint for any incidents that occurred today. 
# It filters through the json endpoint to check for any incidents that have today's date 
# and convert their timezone to ETC from UTC for better readability. 
#
# KEY DETAILS:
#   - Automatically retrieves incidents from the dynamic Freshstatus API endpoint
#   - Filters through the incidents to only return incidents from the present day
#     and for relevant information
#   - Outputs any incidents and information found as a JSON
#   - Shows "No incidents found today" if Freshstatus did not experience issues
#
# REQUIREMENTS:
#   - Python 3.9+ (for zoneinfo)
#   - "requests" library (via 'pip install requests')

import requests
from datetime import datetime, timezone
import json
from zoneinfo import ZoneInfo

URL = "https://public-api.freshstatus.io/v1/public-incidents/?account_id=3616&end_time__gte=2025-05-02T04:00:00Z&end_time__isempty=true"
eastern_TZ = ZoneInfo("US/Eastern")

def get_today_incidents():
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    r = requests.get(URL)
    if r.status_code != 200:
        raise Exception(f"Error fetching incidents: {r.status_code}")

    incidents = r.json().get("results", [])
    filtered_incidents = []

    for incident in incidents:
        start_time = incident.get("start_time")
        if not start_time:
            continue

        # Convert API time to datetime object
        try:
            start_dt_utc = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        except ValueError:
            continue

        # Keep only today's incidents
        if start_dt_utc.strftime("%Y-%m-%d") == today_str:
            start_dt_eastern = start_dt_utc.astimezone(eastern_TZ)
            incident["start_time_eastern"] = start_dt_eastern.strftime("%Y-%m-%d %I:%M:%S %p %Z")
            filtered_incidents.append(incident)

    return filtered_incidents

if __name__ == "__main__":
    try:
        incidents = get_today_incidents()

        if incidents:
            print("There seems to be issues with Freshservice.")
            print(json.dumps(incidents, indent=2))
        else:
            print(json.dumps({"message": "No incidents found today."}, indent = 2))

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
