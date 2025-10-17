import time

from pypresence import Presence

client_id = "717091213148160041"  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop

print(
    RPC.update(
        state="Here it is!",
        details="A working presence, from python!",
        name="Rich Presence Example",
    )
)  # Set the presence

while True:  # The presence will stay on as long as the program is running
    time.sleep(15)  # Can only update rich presence every 15 seconds
