import pypresence
client_id = '64567352374564' #Put your Client ID here, this is a fake ID
RPC = pypresence.client(client_id) #Initialize the client class
RPC.start() #Start the handshake loop

print(RPC.set_activity(state="Lookie Lookie", details="A test of qwertyquerty's Python Discord RPC wrapper, pypresence!")) #Set the presence

while True: #The presence will stay on as long as the program is running
    pass
