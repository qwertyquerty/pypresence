from pypresence import Presence
import time

client_id = '64567352374564'  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop

print(
    RPC.update(
        state="Lookie Lookie",
        details=(
            "A test of qwertyquerty's Python Discord RPC wrapper, pypresence!"
        )
    )
)  # Set the presence

# The presence will stay on as long as the program is running
while True:
    time.sleep(15)  # Can only update rich presence every 15 seconds
