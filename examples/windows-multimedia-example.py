import asyncio
import time

from winrt.windows.media.controls import GlobalSystemMediaTransportControlsSessionManager
from pypresence import AioPresence

client_id = '850343059421790218'  # Fake ID, put your real one here

loop = asyncio.get_event_loop()

RPC = AioPresence(client_id=client_id, loop=loop)  # Initialize the asynchronous presence class


async def update_presence():
    # Request a session from the Windows Runtime API
    manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
    multimedia_session = manager.get_current_session()
    # If nothing is playing through it, clear the presence
    if not multimedia_session:
        return await RPC.clear()

    # Attempt to fetch the media's properties.
    # See the winrt documentation for further properties
    current_media = await multimedia_session.try_get_media_properties_async()
    if not current_media:
        return await RPC.clear()
    # Set the presence to the the track title on one line, and the artist on another.
    await RPC.update(state=current_media.title.replace('- Topic', ''), details=current_media.artist)
    # Replace - Topic because YouTube Music appends it to everything


# Continuously check and update the presence
async def main():
    await RPC.handshake()
    while True:
        await update_presence()
        await asyncio.sleep(10)


loop.run_until_complete(main())
