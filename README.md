Cloudflare Status Monitor Script
Made by Ammar Majeed for CFSB on 7/14/25

Description:
  - This Python script monitors Cloudflare’s public incident API to check for unresolved incidents reported today. It outputs alerts if active issues are detected and prints incident details. A link to Cloudflare’s official status page is included in the output for direct access to full information.

Key Details:
  - Checks for today's incidents using Cloudflare's /incidents.json endpoint.
  - Timezone conversion to US Eastern Time for consistent timestamp display.
  - Alerts if any incident status is not marked as "resolved".
  - Provides direct access link to the Cloudflare status page.
  - Does NOT monitor scheduled maintenance due to API limitations.
  - Designed for operational monitoring and alerting use cases.

Requirements:
  - Python 3.11+ (for zoneinfo support)
  - 'requests' library (install via: pip install requests)
  - Internet access required to query Cloudflare API endpoints.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Microsoft 365 Service Status Monitor
Made by Ammar Majeed for CFSB on 7/17/25

Description:
  - This Python script fetches live Microsoft 365 service status data from Microsoft's public API endpoint (https://status.cloud.microsoft/api/posts/m365Consumer). It processes the service status information and outputs a prioritized report:
       1. Displays services experiencing issues (non-operational) at the top.
       2. Provides a full report of all monitored services and their statuses.

Key Details:
  - Real-time data fetching (no static JSON files required).
  - Timezone conversion to US Eastern Time for consistent timestamp display.
  - Prioritized reporting of any service issues.
  - Clear, readable output suitable for console monitoring or log capture.

Requirements:
  - Python 3.11+ (for zoneinfo support).
  - Requests library (install via `pip install requests`).
  - Internet access required to query M365 API endpoints.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AWS Status Monitor Script
Made by Ammar Majeed for CFSB on 7/29/25

DESCRIPTION:
  This python script was created to check the health of AWS Services on the East and West Coast. It checks the
ws-broker-service endpoints from this url: https://clients.amazonworkspaces.com/Health.html across the regions 
by sending a GET request to each /ping URL. The it prints the status message if any of the regions report unhealthy

KEY DETAILS:
  - Uses built-in packagaes in Python to avod any external dependancies
  - Sends a GET request to each region's /ping URL
  - Parses the response body and looks for the keyword "healthy"
  - Prints the region name from the URL for clear reporting

REQUIREMENTS:
  - Python 3.7+
