from pypresence import Presence
import time
import random

client_id = '64567352374564'  # Put your Client ID here, this is a fake ID
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


while True:  # The presence will stay on as long as the program is running
    RPC.update(details="Famous Quote:", state=random.choice(quotes)) #Set the presence, picking a random quote
    time.sleep(60) #Wait a wee bit
