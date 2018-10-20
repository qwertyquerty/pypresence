from pypresence import Presence

"""
You need to upload your image(s) here:
https://discordapp.com/developers/applications/<APP ID>/rich-presence/assets
"""

client_id = 64567352374534
RPC = pypresence.Presence(client_id=client_id, pipe=0)
RPC.connect()

# Make sure you are using the same name that you used when uploading the image
RPC.update(large_image="big-image", large_text="Large Text Here!",
            small_image="small-image", small_text="Small Text Here!")
