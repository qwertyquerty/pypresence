#!/usr/bin/env python3
# encoding: utf-8

import asyncio
import time

from pypresence import Presence

client_id = '64567352374564'  # Fake ID, put your real one here
loop = asyncio.get_event_loop()
RPC = Presence(client_id, loop=loop)  # Initialize the client class

async def main():
    await RPC.connect() # Start the handshake loop

    print(
        await RPC.update(
            state="Lookie Lookie",
            details="A test of qwertyquerty's Python Discord RPC wrapper, pypresence!"))  # Set the presence

    while True:  # The presence will stay on as long as the program is running
        await asyncio.sleep(15) # Can only update rich presence every 15 seconds

if __name__ == '__main__':
    loop.run_until_complete(main())
    RPC.close()
    loop.close()
