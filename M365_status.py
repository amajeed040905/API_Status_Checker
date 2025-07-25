# Microsoft 365 Service Status Monitor
# Made by Ammar Majeed for CFSB on 7/17/25
#
# Description:
#    This Python script fetches live Microsoft 365 service status data from Microsoft's public
#    API endpoint (https://status.cloud.microsoft/api/posts/m365Consumer). It processes the
#    service status information and outputs a prioritized report:
#
#       1. Displays services experiencing issues (non-operational) at the top.
#       2. Provides a full report of all monitored services and their statuses.
#
# Key Details:
#    - Real-time data fetching (no static JSON files required).
#    - Timezone conversion to US Eastern Time for consistent timestamp display.
#    - Prioritized reporting of any service issues.
#    - Clear, readable output suitable for console monitoring or log capture.
#
# Requirements:
#    - Python 3.11+ (for zoneinfo support).
#    - Requests library (install via `pip install requests`).
#
# Notes:
#    - This script assumes the public API endpoint remains accessible and stable.
#    - A standard User-Agent header is included to mimic browser requests, improving reliability.

import json
import requests
from datetime import datetime
import zoneinfo

# Define Eastern Time timezone for consistent timestamp display
ET_timezone = zoneinfo.ZoneInfo("US/Eastern")

# Microsoft 365 Status API Endpoint (Live Data)
M365_STATUS_URL = "https://status.cloud.microsoft/api/posts/m365Consumer"
STATUS_PAGE_URL = "https://status.cloud.microsoft/m365/referrer=serviceStatusRedirect"

# Returns default headers for HTTP requests.
# Useful to mimic a browser and avoid basic bot blocking.

# Returns:
#    dict: Headers including User-Agent.
def get_standard_headers():
    return {
        "User-Agent": "Mozilla/5.0"
    }

def get_m365_status():

    # headers = get_standard_headers() USE IF TROUBLE GETTING PAGE INFO
    response = requests.get(M365_STATUS_URL) #, headers = headers)
    response.raise_for_status()  # Automatically stops script if request fails
    return response.json()

# Fetch the live JSON data from Microsoft
data = get_m365_status()

# Containers for reporting
issues_found = []
service_reports = []

# Loop through each service and process its status
for service in data:
    service_name = service.get("ServiceDisplayName", "Unknown Service")
    status = service.get("Status", "Unknown Status")
    message = service.get("Message", "No message available.")
    title = service.get("Title", "No title available.")
    last_updated_raw = service.get("LastUpdatedTime", "")

    # Convert last updated timestamp to Eastern Time
    try:
        last_updated_utc = datetime.fromisoformat(last_updated_raw.replace("Z", "+00:00"))
        last_updated_et = last_updated_utc.astimezone(ET_timezone)
        last_updated_str = last_updated_et.strftime("%Y-%m-%d %I:%M:%S %p %Z")
    except Exception:
        last_updated_str = "Unknown timestamp."

    # Store full service status for final report
    service_reports.append({
        "service": service_name,
        "status": status,
        "title": title,
        "message": message,
        "last_updated": last_updated_str
    })

    # If service is not operational, log it for priority reporting
    if status.lower() != "operational":
        issues_found.append({
            "service": service_name,
            "status": status,
            "title": title,
            "message": message,
            "last_updated": last_updated_str
        })

# FIRST REPORT: Highlight non-operational services immediately
if issues_found:
    print("\n Some services are reporting issues:\n")
    print(f"Visit the official page for more details:\n{STATUS_PAGE_URL}\n")
    for issue in issues_found:
        print(f"- {issue['service']}: {issue['status']}")
        print(f"  Title: {issue['title']}")
        print(f"  Message: {issue['message']}")
        print(f"  Last Updated: {issue['last_updated']}\n")
else:
    print("\n All Microsoft 365 services are operational.\n")

# FULL REPORT: Show all monitored services
print("Full Report:")
print("-" * 40)
for report in service_reports:
    print(f"Service: {report['service']}")
    print(f"Status : {report['status']}")
    print(f"Title  : {report['title']}")
    print(f"Message: {report['message']}")
    print(f"Last Updated: {report['last_updated']}")
    print("-" * 40)