import pypresence
import time

client_id = '64567352374564' #Put your Client ID here, this is a fake ID
RPC = pypresence.client(client_id) #Initialize the client class
RPC.start() #Start the handshake loop


while True: #The presence will stay on as long as the program is running
    time.sleep(60) #Wait a wee bit
    print(RPC.set_activity(state="Click for quote!", details=random.choice(quotes))) #Set the presence, picking a random quote
