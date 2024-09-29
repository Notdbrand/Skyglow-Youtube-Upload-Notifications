import requests

API_KEY = 'EnterAPIKeyHere'

youtube_handles = input("Enter the handles for all youtube channels you want the ids of (Excluding the @ and separated with a space): ").split()

def get_channel_id_by_handle(handle):
    url = f'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'part': 'snippet',
        'q': f'@{handle}',
        'type': 'channel',
        'key': API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        return data['items'][0]['snippet']['channelId']
    else:
        return None


channel_ids = []

for handle in youtube_handles:
    channel_id = get_channel_id_by_handle(handle)
    if channel_id:
        channel_ids.append(f"'{channel_id}'")
    else:
        channel_ids.append(f"'No channel found for {handle}'")

print(",\n".join(channel_ids))
