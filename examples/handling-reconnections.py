from pypresence import Presence, PipeClosed, DiscordError
import time
import socket

# Somehow eliminates DiscordNotFoundError
def is_discord_running():
    for i in range(6463,6473):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.01)
        try:
            conn = s.connect_ex(('localhost', i))
            s.close()
            if (conn == 0):
                s.close()
                return(True)
        except:
            s.close()
            return(False)
        
client_id = 'ID'  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
if is_discord_running():#check if discord is running before connecting
    RPC.connect() # Start the handshake loop


while True:  # The presence will stay on as long as the program is running
    try:
        print(RPC.update(state="Hello", details="World"))  # Set the presence
    except (PipeClosed, DiscordError):
        if is_discord_running():#check again before connecting
            RPC.connect()
    time.sleep(15) # Can only update rich presence every 15 seconds
