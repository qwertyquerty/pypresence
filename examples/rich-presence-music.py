from pypresence import Presence, ActivityType
import time

client_id = '717091213148160041'  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect() # Start the handshake loop

RPC.update(
    activity_type = ActivityType.LISTENING, # Set the activity to listening
    details=input("Your favorite song: "),
    state=input("The artist who made it: "),
    end=int(input("The length of the song (in seconds): ")) + time.time(),
    # At time of writing this, timestamps don't show for listening statuses!
    # ...so this field is pointless lol
) # Get the user's favorite song!

while True:  # The presence will stay on as long as the program is running
    time.sleep(15) # Can only update rich presence every 15 seconds
