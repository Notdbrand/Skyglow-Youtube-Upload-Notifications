# Youtube notifications for skyglow notifications

# Setup:
Step 1:<br />
Using YoutubeHandleToID.py, edit and insert your own Youtube API key. Then when prompted enter all the handle of the channels you want notifications for separated with spaces then press enter and copy the outputed list.<br /><br />
Step 2:<br />
Make sure the skyglow notification port is set correctly.<br /><br />
Step 3:<br />
Open Youtube.py and replace the placeholder list with the generated list.<br /><br />
Step 4:<br />
On first startup or whenever you add another channel ID run this:<br />
python YoutubeBot.py --channel_list<br />
It will then add the video IDs from all channels (This isn't actually all the videos from a channel it's only the 10ish more recent videos)<br /><br />
Step 5:<br />
Now you're setup! Just run youtube.py and now you'll receive notifications about new uploads<br /><br />

# Other info
Make sure that the notification data is being sent to the correct port that skyglow notifications is hosted on.

Default time to check for new videos is 1800 seconds (30 minutes)

Made for this server
https://github.com/ObscureMosquito/Skyglow-Notifications
