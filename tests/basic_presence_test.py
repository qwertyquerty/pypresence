import os
import random

from pypresence import Presence

client_id = os.environ["PYPRESENCE_CLIENT_ID"]
RPC = Presence(client_id)  # Initialize the Presence class
RPC.connect()  # Start the handshake loop


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

for i in range(3):
    RPC.update(details="Famous Quote:",
               state=random.choice(quotes))
