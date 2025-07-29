# AWS Status Monitor Script
# Made by Ammar Majeed for CFSB on 7/29/25
#
# DESCRIPTION:
# This python script was created to check the health of AWS Services on the East and West Coast. It checks the
# ws-broker-service endpoints from this url: https://clients.amazonworkspaces.com/Health.html across the regions 
# by sending a GET request to each /ping URL. The it prints the status message if any of the regions report unhealthy
#
# KEY DETAILS:
# - Uses built-in packagaes in Python to avoid any external dependancies
# - Sends a GET request to each region's /ping URL
# - Parses the response body and looks for the keyword "healthy"
# - Prints the region name from the URL for clear reporting
#
# REQUIREMENTS:
# - Python 3.7+

import http.client
import urllib.parse

# List of regional endpoints
urls = [
    "https://ws-broker-service.us-east-1.amazonaws.com/ping",
    "https://ws-broker-service.us-west-2.amazonaws.com/ping",
    # Add more regions as needed
]

def check_health_status(url):
    parsed_url = urllib.parse.urlparse(url)
    conn = http.client.HTTPSConnection(parsed_url.netloc)

    path = parsed_url.path or "/"
    conn.request("GET", path)
    response = conn.getresponse()

    status_code = response.status
    body = response.read().decode()

    region = parsed_url.netloc.split('.')[1]  # Extract region
    print(f"Checking region: {region}")

    if "healthy" in body.lower():
        print(f"{region}: Services are healthy.\n")
    else:
        print(f"{region}: Some Services may have issues...\nStatus Code: {status_code}\nResponse Body:\n{body}\n")

    conn.close()

# Check all regions
for url in urls:
    check_health_status(url)
