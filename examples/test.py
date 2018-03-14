import pypresence
client_id = '64567352374564' #Put your Client ID here
RPC = pypresence.client(client_id)
RPC.start()

print(RPC.set_activity(state="ree")) #Set the presence

while True: #The presence will stay on as long as the program is running
    pass
