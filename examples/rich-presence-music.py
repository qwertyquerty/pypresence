import time

from pypresence import ActivityType, Presence, StatusDisplayType

client_id = "717091213148160041"  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect()  # Start the handshake loop

RPC.update(
    activity_type=ActivityType.LISTENING,  # Set the activity to listening
    status_display_type=StatusDisplayType.DETAILS,  # Set the status display type to details
    details=input("Your favorite song: "),
    state=input("The artist who made it: "),
    start=int(time.time()),  # Start time is now
    end=int(input("The length of the song (in seconds): ")) + int(time.time()),
)  # Get the user's favorite song!

while True:  # The presence will stay on as long as the program is running
    time.sleep(15)  # Can only update rich presence every 15 seconds
