import time

import requests  # Needs requests module installed: pip install requests -U
from pypresence import Presence


CLIENT_ID = ''  # Your client ID here


def get_presence_data():
    with requests.get('https://somewebsite.com/api/status') as resp:
        data = resp.json()
    # Use the data in whatever way you want, and return kwargs for the Presence.update() method
    return {'state': data['online'].title(), 'details': 'SomeWebsite Status', 'start': data['start']}


def run():
    presence = Presence(CLIENT_ID)
    presence.connect()
    while True:
        data = get_presence_data()
        presence.update(**data)
        time.sleep(15)
        
        
if __name__ in '__main__':
    run()
