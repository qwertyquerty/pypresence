#!/usr/bin/env python3
# encoding: utf-8

import asyncio
import time

import psutil
from pypresence import Presence

client_id = '64567352374564'  # Fake ID, put your real one here
loop = asyncio.get_event_loop()
RPC = Presence(client_id, loop=loop)  # Initialize the client class

async def main():
    await RPC.connect() # Start the handshake loop

    while True:  # The presence will stay on as long as the program is running
        cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
        mem = psutil.virtual_memory()
        mem_per = round(psutil.virtual_memory().percent,1)
        print(await RPC.update(details="RAM: "+str(mem_per)+"%", state="CPU: "+str(cpu_per)+"%"))  # Set the presence
        await asyncio.sleep(15) # Can only update rich presence every 15 seconds

if __name__ == '__main__':
    loop.run_until_complete(main())
    RPC.close()
    loop.close()
