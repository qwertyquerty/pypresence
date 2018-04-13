import psutil
from pypresence import Client
import time

client_id = '64567352374564'  # Fake ID, put your real one here
RPC = Client(client_id,pipe=1)  # Initialize the client class
RPC.start() # Start the handshake loop


while True:  # The presence will stay on as long as the program is running
    cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
    mem = psutil.virtual_memory()
    mem_per = round(psutil.virtual_memory().percent,1)
    print(RPC.set_activity(details="RAM: "+str(mem_per)+"%", state="CPU: "+str(cpu_per)+"%"))  # Set the presence
    time.sleep(15) # Wait
