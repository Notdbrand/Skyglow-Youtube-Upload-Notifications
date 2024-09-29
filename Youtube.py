import requests
import time
import xml.etree.ElementTree as ET
import json
import os
import argparse

# How long until channels are checked for new uploads (seconds)
waitTime = 1800
json_file = "checked_videos.json"

# List of channel ids
channel_ids = [
    'YoutubeChannelID1',
    'YoutubeChannelID2'
]

def load_checked_videos():
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            checked_videos = json.load(f)
    else:
        checked_videos = {}

    for channel_id in channel_ids:
        if channel_id not in checked_videos:
            checked_videos[channel_id] = []

    return checked_videos

def save_checked_videos(checked_videos):
    with open(json_file, 'w') as f:
        json.dump(checked_videos, f, indent=4)

# Sends the Youtube notification
def send_notification(uploader, video_title):
    url = "http://localhost:7878/send_data"
    payload = {
        "sender": f"{uploader} uploaded",
        "message": video_title,
        "topic": "com.google.ios.youtube"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    print(f"Notification sent. Status code: {response.status_code}, Payload: {payload}")

# Checks the XML feed and finds new videos by comparing video IDs
def check_new_videos(checked_videos, channel_list=False):
    for channel_id in channel_ids:
        print(f"Checking Channel {channel_id}")
        try:
            url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
            response = requests.get(url)
            response.raise_for_status()
            root = ET.fromstring(response.content)

            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                video_id = entry.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
                author = entry.find('{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
                title = entry.find('{http://www.w3.org/2005/Atom}title').text

                # Adds existing video IDs to a json file
                if channel_list:
                    if video_id not in checked_videos[channel_id]:
                        checked_videos[channel_id].append(video_id)
                        print(f"Added existing video: {title} (ID: {video_id})")
                else:
                    # Check if video ID is new
                    if video_id not in checked_videos[channel_id]:
                        print(f'New upload found: {title} by {author} (ID: {video_id})')
                        send_notification(author, title)
                        checked_videos[channel_id].append(video_id)

        except requests.RequestException as e:
            print(f'Error fetching data for channel {channel_id}: {e}')

    save_checked_videos(checked_videos)

def main(channel_list=False):
    checked_videos = load_checked_videos()

    if channel_list:
        print("Updating list: Adding video IDs to json file.")
        check_new_videos(checked_videos, channel_list=True)
    else:
        while True:
            check_new_videos(checked_videos, channel_list=False)
            print(f"Checked all channels. Waiting {int(waitTime/60)} minutes until next check.")
            time.sleep(waitTime)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube channel video checker")
    parser.add_argument('--channel_list', action='store_true', help="Makes a JSON file with the existing video IDs.")
    args = parser.parse_args()

    main(channel_list=args.channel_list)
