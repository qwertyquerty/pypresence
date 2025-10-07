from pypresence import Presence
import time

"""
You need to upload your image(s) here:
https://discord.com/developers/applications/<APP ID>/rich-presence/assets
"""

client_id = "client_id"  # Enter your Application ID here.
RPC = Presence(client_id=client_id)
RPC.connect()


# Make sure you are using the same name that you used when uploading the image
start_time = (
    time.time()
)  # Using the time that we imported at the start. start_time equals time.
RPC.update(
    large_image="LARGE_IMAGE_HERE",
    large_text="Programming B)",
    small_image="SMALL_IMAGE_HERE",
    small_text="Hello!",
    start=start_time,
)  # We want to apply start time when you run the presence.

while 1:
    time.sleep(15)  # Can only update presence every 15 seconds
