Activity()
************************

.. |br| raw:: html

   <br />


.. py:class:: Activity(client, **options)

   Creates the Activity ready for usage.

   :param pypresence.Presence client: An instance of a Presence client, for the Activity to use
   :param int pid: the process id of your game
   :param str state: the user's current status
   :param str details: what the player is currently doing
   :param int start: epoch time for game start
   :param int end: epoch time for game end
   :param str large_image: name of the uploaded image for the large profile artwork
   :param str large_text: tooltip for the large image
   :param str small_image: name of the uploaded image for the small profile artwork
   :param str small_text: tootltip for the small image
   :param str party_id: id of the player's party, lobby, or group
   :param list party_size: current size of the player's party, lobby, or group, and the max in this format: ``[1,4]``
   :param str join: unique hashed string for chat invitations and ask to join
   :param str spectate: unique hashed string for spectate button
   :param str match: unique hashed string for spectate and join
   :param bool instance: marks the match as a game session with a specific beginning and end

   Upon initialization, the Activity will update the rich presence. Editing any of the parameters later on will also cause the Activity to auto-update the rich presence.

   **Example:**

   .. code-block:: python

     from pypresence import Presence, Activity
     import time

     client_id = '5834659349'  # Fake ID, put your real one here
     RPC = Presence(client_id)  # Initialize the client class
     RPC.connect() # Start the handshake loop

     ac = Activity(RPC) # Make the activity

     ac.start = int(time.time()) # Setting the start time, auto updates the presence

     while True:  # The presence will stay on as long as the program is running
         time.sleep(15) # Can only update rich presence every 15 seconds


|br|

  .. py:function:: end_in(time_until_end)

     Specify how long until the countdown reaches 0 on your Rich Presence.

     :param int time_until_end: How long (in seconds) it will take before the countdown reaches 0.

|br|
