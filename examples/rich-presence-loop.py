#!/usr/bin/env python3
# encoding: utf-8

import asyncio
import random
import time

from pypresence import Presence

client_id = '64567352374564'  # Put your Client ID here, this is a fake ID
loop = asyncio.get_event_loop()
RPC = Presence(client_id, loop=loop)  # Initialize the Presence class

quotes = [
    "If you can dream it, you can achieve it.",
    "Either write something worth reading or do something worth writing.",
    "You become what you believe.",
    "Fall seven times and stand up eight.",
    "The best revenge is massive success.",
    "Eighty percent of success is showing up.",
    "Life is what happens to you while you’re busy making other plans.",
    "Strive not to be a success, but rather to be of value.",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Everything you’ve ever wanted is on the other side of fear."
]  # The quotes to choose from

async def main():
    await RPC.connect()  # Start the handshake loop

    while True:  # The presence will stay on as long as the program is running
        RPC.update(details="Famous Quote:", state=random.choice(quotes)) #Set the presence, picking a random quote
        await asyncio.sleep(60) #Wait a wee bit

if __name__ == '__main__':
    loop.run_until_complete(main())
    RPC.close()
    loop.close()
