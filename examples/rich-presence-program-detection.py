import time

import psutil
import pypresence

rpc = pypresence.Presence('0123..')  # Put your Application ID here
data = None

rpc.connect()

while True:
    for proc in psutil.process_iter():
        # This is an example of structural pattern matching added in Python 3.10 | Tutorial: https://www.python.org/dev/peps/pep-0636/
        match proc.name().lower():
            case "virtualbox.exe":
                data = {"state": "On VirtualBox", "details": "Kali Linux"}
                break
            case "itunes.exe":
                data = {"state": "XYZ", "details": "Zoom", "large_image": "foo", "large_text": "bar"}
                break
            case _:
                data = None

    # You don't have to update the status like this, you could do it in the for loop or call a different function to do it.
    if data:
        rpc.update(**data)
    else:
        rpc.clear()

    time.sleep(10)
