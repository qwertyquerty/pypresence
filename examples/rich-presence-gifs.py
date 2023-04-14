
from pypresence import Presence
import time

"""
Create an application and get the application id here to get custom name mine is Bombsquad
https://discord.com/developers/applications or just use mine.
I used the giphy website and tenor

"""

client_id = "963434684669382696"  # Enter your Application ID here.
RPC = Presence(client_id=client_id)
RPC.connect()

# Make sure you are using the same name that you used when uploading the image
RPC.update(state="Custom gif's",details="Using pypresence",large_image=("https://media.tenor.com/uAqNn6fv7x4AAAAM/bombsquad-spaz.gif"), large_text="Dancing Spazito!",
            small_image=("https://media.giphy.com/media/4UjV5LeD66EPruSG18/giphy.gif"), small_text="Spinning")
while True:
    time.sleep(1)