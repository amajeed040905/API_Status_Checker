# Cloudflare Status Monitor Script
# Made by Ammar Majeed for CFSB on 7/14/25
#
# DESCRIPTION:
# This Python script monitors Cloudflare’s public incident API to check for
# unresolved incidents reported today. It outputs alerts if active issues 
# are detected and prints incident details. A link to Cloudflare’s official
# status page is included in the output for direct access to full information.
#
# KEY DETAILS:
# - Checks for today's incidents using Cloudflare's /incidents.json endpoint.
# - Alerts if any incident status is not marked as "resolved".
# - Provides direct access link to the Cloudflare status page.
# - Does NOT monitor scheduled maintenance due to API limitations.
# - Designed for operational monitoring and alerting use cases.
#
# REQUIREMENTS:
# - Python 3.x
# - 'requests' library (install via: pip install requests)
# - Internet access required to query Cloudflare API endpoints.

import requests
from datetime import datetime, timezone
import json
import zoneinfo

# Define Eastern Time timezone for consistent timestamp display
ET_timezone = zoneinfo.ZoneInfo("US/Eastern")

CF_status_URL = "https://www.cloudflarestatus.com/api/v2/incidents.json"
CF_status_page_link = "https://www.cloudflarestatus.com/"

#Gets incident data from Cloudflare's API
def get_summary():
    try:
        response = requests.get(CF_status_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        #return "page" (Metadata about the status page itself)
        page_info = data.get("page", {})
        today = datetime.now(ET_timezone).date()

        incident_summaries = []
        alert_triggered = False   # Track if any problem detected    

        for incident in data.get("incidents", []):
            incident_created_at = incident.get("created_at")
            if not incident_created_at:
                continue

            incident_date = datetime.fromisoformat(incident_created_at.replace("Z", "+00:00")).date()
            if incident_date != today:
                continue

            status = incident.get("status", "").lower()

            # Check if the incident status is not "resolved"
            if status != "resolved":
                alert_triggered = True
                print(f"ALERT: Cloudflare issue detected! Status: {status}")

            summary = {
                "status": status,
                "created_at": incident.get("created_at"),
                "updated_at": incident.get("updated_at"),
                "started_at": incident.get("started_at"),
                "updates": []
            }

            for update in incident.get("incident_updates", []):
                update_created_at = update.get("created_at")
                if not update_created_at:
                    continue

                update_date = datetime.fromisoformat(update_created_at.replace("Z", "+00:00")).date()
                if update_date == today:
                    summary["updates"].append({
                        "created_at": update_created_at,
                        "body": update.get("body", "")
                    })

            if summary["updates"]:
                incident_summaries.append(summary)

        if not incident_summaries:
            incident_summaries.append({
                "message": "No incidents or investigations reported today."
            })

        if alert_triggered:
            print("\nCloudflare may be experiencing issues today.")
            print(f"\nView Cloudflare Status Page for full details:\n{CF_status_page_link}\n") #add link to check for extra problem details
        else:
            print("\nCloudflare appears operational.\n")

        return {
            "page": page_info,
            "incidents": incident_summaries
        }

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Cloudflare.")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    result = get_summary()
    if result:
        print(json.dumps(result, indent=2))