##################
Quickstart
##################

.. |br| raw:: html

   <br />


+-------------------------------------------------------------------------------------------------------------------------+
|This page exists for if you have literally no clue what you're doing, or you just need a quick start. (For rich presence)|
+-------------------------------------------------------------------------------------------------------------------------+


**The first thing youll want to do is create a Discord RPC app. Here are the steps:**

- Navigate to `https://discordapp.com/developers/ <https://discordapp.com/developers/>`_
- Click "Create an Application."
- Setup the application how you want, give it the name you want, and give it a good image.
- Right under the name of your application, locate your Client ID. You will need this later.
- Lastly, save your application.

**Next, you need to install pypresence. You will need python 3.5 - 3.7 installed. Here are the steps:**

- Open command prompt
- Type ``pip3 install pypresence`` and hit enter
- It should say something near the end that says something like ``"Successfully installed pypresence"``.

**Now you will need to create the program to set your rich presence. First we need to import what we need, like so:**

.. code-block:: python

 from pypresence import Presence # The simple rich presence client in pypresence
 import time

**Next we need to initialize our Rich Presence client. You'll need that Client ID from earlier:**

.. code-block:: python

 client_id = "ID HERE"  # Put your Client ID in here
 RPC = Presence(client_id)  # Initialize the Presence client

**Now we need to connect our Client to Discord, so it can send presence updates:**

.. code-block:: python

 RPC.connect() # Start the handshake loop

**Now we need to actually set our rich presence. We can use the update() function for this. There are many options we can use, but for this we will use state:**

.. code-block:: python

 RPC.update(state="Rich Presence using pypresence!") # Updates our presence


**Now we need our program to run forever, so we use a while loop.**

.. code-block:: python

 while True:  # The presence will stay on as long as the program is running
     time.sleep(15) # Can only update rich presence every 15 seconds


**Now when you run your program, it should look something like this!**

.. figure:: ../_static/img/quickstart-final.png
   :scale: 150 %
   :alt: Finished Presence
