
from pypresence import Presence
import time

"""
Create an application and get the application id here 
https://discord.com/developers/applications.
I used the giphy website and tenor
"""

client_id = "9786765454547767"  # Enter your Application ID here.
RPC = Presence(client_id=client_id)
RPC.connect()


RPC.update(state="Custom gifs",details="Using pypresence",large_image=("https://media.tenor.com/9c83g4VPctQAAAAi/shaking-eyes-eyes-shaking.gif"), large_text="Watching!",
            small_image=("https://media.giphy.com/media/4UjV5LeD66EPruSG18/giphy.gif"), small_text="Spinning")
while True:
    time.sleep(1)
