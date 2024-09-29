# Youtube notifications for skyglow notifications

Setup:
Step 1:
Using YoutubeHandleToID.py, edit and insert your own Youtube API key. Then when prompted enter all the handle of the channels you want notifications for separated with spaces then press enter and copy the outputed list.
Step 2:
Make sure the skyglow notification port is set correctly.
Step 3:
Open Youtube.py and replace the placeholder list with the generated list.
Step 4:
On first startup or whenever you add another channel ID run this:
python YoutubeBot.py --channel_list
It will then add the video IDs from all channels (This isn't actually all the videos from a channel it's only the 10ish more recent videos)
Step 5:
Now you're setup! Just run youtube.py and now you'll receive notifications about new uploads

Make sure that the notification data is being sent to the correct port that skyglow notifications is hosted on.

Default time to check for new videos is 1800 seconds (30 minutes)

Made for this server
https://github.com/ObscureMosquito/Skyglow-Notifications
