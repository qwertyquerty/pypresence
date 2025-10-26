from pypresence import Presence
import time

client_id = "client_id"  # Enter your Application ID here.
RPC = Presence(client_id=client_id)
RPC.connect()


RPC.update(buttons=[{"label": "Website", "url": "https://qtqt.cf"}, {"label": "Server", "url": "https://discord.gg/JF3kg77"}]) # Can specify up to 2 buttons

while 1:
    time.sleep(15) #Can only update presence every 15 seconds
