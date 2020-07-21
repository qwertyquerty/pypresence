try:
    from pypresence import Presence
    import time
    import json
    import os
    import re
    import datetime
    import crayons
    import sys
    
# checks if all modules installed    
except ModuleNotFoundError as e:
    print(e)
    print('pip install -r requirements.txt might fix it')
    exit()
# for HaltException
# check if config.json exists, if not create one with default values
try:
    if not os.path.isfile('./config.json'):
        data = {
            'CLIENT_ID': '123456789123456789',
            'State': 'Advanced Discord RPC',
            'Details': 'kaaaxcreators.de',
            'LImage': 'zero',
            'LTooltip': 'zero',
            'SImage': 'zero',
            'STooltip': 'zero',
            'Debug': 'False',
        }
        jstr = json.dumps(data, indent=4)
        f= open("config.json","w+")
        f.write(jstr)
        print(crayons.red('CONFIG.JSON has been created! EDIT IT'))
        print(crayons.red('CONFIG.JSON has been created! EDIT IT'))
        print(crayons.red('CONFIG.JSON has been created! EDIT IT'))
        raise Exception('exit')
except:
    print(crayons.red('CONFIG.JSON has been created! EDIT IT'))       

# loads config.json as variable
with open('config.json') as f:
    data = json.load(f)
    details = data['Details']
    state = data['State']
    client_id = data['CLIENT_ID']
    limage = data['LImage']
    ltooltip = data['LTooltip']
    simage = data['SImage']
    stooltip = data['STooltip']
    start = datetime.datetime.now().timestamp()
    debug = data['Debug']
    
# start the rpc client
RPC = Presence(client_id)
RPC.connect()
try:
    if data['Debug'] == "True":
        print(RPC.update(details=details, state=state, large_image=limage, large_text=ltooltip, small_image=simage, small_text=stooltip, start=int(start)))

    if data['Debug'] == "False":
        # Set the presence              
        RPC.update(details=details, state=state, large_image=limage, large_text=ltooltip, small_image=simage, small_text=stooltip, start=int(start))

        # prints every setting
        print("Details:", details,"; \nState:", state,"; \nClient-ID:", client_id,"; \nLarge_Image:", limage,"; \nLarge_Tooltip:", ltooltip,"; \nSmall_Image:", simage,"; \nSmall_Tooltip:", stooltip, ";")
except:
    print(crayons.red('Have you edited config.json properly?'))

# sets date for file-change-detection system
olddate = os.stat("./config.json")[8]

while True: # The presence will stay on as long as the program is running
    moddate = os.stat("./config.json")[8] # gets attribute from file
    
    # check if config.json has changed
    if moddate != olddate:
        print()
        print(crayons.magenta('config.json has been changed'))
        print()
        
        # reloads config.json
        with open('config.json') as g:
            data = json.load(g)
            details = data['Details']
            state = data['State']
            client_id = data['CLIENT_ID']
            limage = data['LImage']
            ltooltip = data['LTooltip']
            simage = data['SImage']
            stooltip = data['STooltip']
            start = datetime.datetime.now().timestamp()
        
        if data['Debug'] == "True":
            print(RPC.update(details=details, state=state, large_image=limage, large_text=ltooltip, small_image=simage, small_text=stooltip, start=int(start)))

        if data['Debug'] == "False":
            # Re-Set the presence              
            RPC.update(details=details, state=state, large_image=limage, large_text=ltooltip, small_image=simage, small_text=stooltip, start=int(start))

            # prints every setting
            print("Details:", details,"; \nState:", state,"; \nClient-ID:", client_id,"; \nLarge_Image:", limage,"; \nLarge_Tooltip:", ltooltip,"; \nSmall_Image:", simage,"; \nSmall_Tooltip:", stooltip, ";")
        # sets date for file-change-detection system
        olddate = os.stat("./config.json")[8] # gets attribute from file
    
    
    
    
