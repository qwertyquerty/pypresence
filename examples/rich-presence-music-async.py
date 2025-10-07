import asyncio
import time
from pypresence import AioPresence, ActivityType, StatusDisplayType
from pypresence.exceptions import PyPresenceException

client_id = '717091213148160041'  # Fake ID, put your real one here

# Gather inputs synchronously before starting the event loop
song = input("Your favorite song: ")
artist = input("The artist who made it: ")
length = int(input("The length of the song (in seconds): "))


async def main(rpc) -> None:
    await rpc.connect()  # Start the handshake loop (async)

    start = int(time.time())
    await rpc.update(
        activity_type=ActivityType.LISTENING,  # Set the activity to listening
        status_display_type=StatusDisplayType.DETAILS,  # Set the status display type to details
        details=song,
        state=artist,
        start=start,  # Start time is now
        end=start + length,
    )  # Get the user's favorite song!

    try:
        while True:  # Keep the presence alive while the program runs
            await asyncio.sleep(15)  # Can only update rich presence every 15 seconds
    except PyPresenceException:
        pass
if __name__ == "__main__":
    rpc = AioPresence(client_id)
    asyncio.run(main(rpc))
    rpc.close()  # Ensure the connection is closed when done
