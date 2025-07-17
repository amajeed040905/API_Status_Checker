# Cloudflare_API
This project was created during my tenure at CFSB in 2025 to solve a problem that they had an experienced while I was interning. I was asked to create a python script to grab certain keys from the json body of the Cloudflare API. The company needed this made because a couple of weeks before I initially started this project, Cloudflare was down for a day, and it affected big names like Google and Spotify. But it directly affected our company and some of the sevices and tools we utilized. So the goal for this project was to create a script that could be automated later so that our team members could be proactive, instead of reactive to a situation like I mentioned.

That being said, I was tasked with creating the script and later creating an automation to poll every 5 minutes and send an alert out if any incidents are detected. The script itself uses the Cloudflare API json body, and from the json body I grabbed multiple keys to create a proper report on the status of Cloudflare. The keys that are being grabbed are listed below:
  - "page" which includes the keys "id", "name", "url", "time_zone", and "updated_at"
  - "incidents" which includes the keys "status", "created_at", "updated_at", and "started_at"
  - "updates" which includes the keys "created_at" and "body"

The key "page" just presents the metadata for the page itself, which includes the keys listed with it. The most important keys to be acknowledged though, lie within the incidents key and also within the updates key (which is nested within incidents). 
INCIDENTS:
  - "status" tells you what the current situation is, like "resolved" or "investigating".
  - "created_at" tells you the timestamp for when the incident was created.
  - "updated_at" tells you the timestamp when the issue was last updated
  - "started_at" tells you the timestamp for when the issue initially started
UPDATES:
  - "created_at" tells you the timestamp for when the update was posted
  - "body" gives you the text body or the description of the update
