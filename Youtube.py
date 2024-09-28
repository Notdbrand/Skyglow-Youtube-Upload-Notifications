import requests
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

# How long until channels are checked for new uploads (seconds)
waitTime = 1800

# List of channel ids
channel_ids = [
    'UCULqEJCbEe8P4r9ZI15BofQ' # Enter the channel ids that you want updates for
]

# Sets the last time since the youtube channels were checked for new uploads
last_checked_time = datetime.now(timezone.utc)

# Sends the youtube notification
def send_notification(uploader, video_title):
    url = "http://localhost:7878/send_data" #Make sure the correct port is used to send the data to skyglow notification 
    payload = {
        "sender": f"{uploader} uploaded",
        "message": video_title,
        "topic": "com.google.ios.youtube"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    print(f"Notification sent. Status code: {response.status_code}, Payload: {payload}")

# Checks the xml file it receives back and checks for videos released since the server was started
def check_new_videos():
    global last_checked_time
    current_time = datetime.now(timezone.utc)
    new_uploads_found = False

    for channel_id in channel_ids:
        try:
            url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
            response = requests.get(url)
            response.raise_for_status()

            root = ET.fromstring(response.content)

            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                published = entry.find('{http://www.w3.org/2005/Atom}published').text
                published_datetime = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S%z")

                if published_datetime > last_checked_time:
                    author = entry.find('{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
                    title = entry.find('{http://www.w3.org/2005/Atom}title').text
                    print(f'{author} uploaded: {title}')
                    
                    send_notification(author, title)
                    new_uploads_found = True

        except requests.RequestException as e:
            print(f'Error fetching data for channel {channel_id}: {e}')
    
    # Update the time
    last_checked_time = current_time

    if not new_uploads_found:
        print(f"No new uploads found at {current_time}.")
        print(f"Checking again in {int(waitTime/60)} minutes.")

while True:
    check_new_videos()
    time.sleep(waitTime)
