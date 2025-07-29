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