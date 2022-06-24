Presence()
************************

.. |br| raw:: html

   <br />


.. py:class:: Presence(client_id, pipe=0, loop=None, handler=None)

 Creates the Presence client ready for usage.

 :param str client_id: OAuth2 App ID (found `here <https://discord.com/developers/applications/me>`_)
 :param int pipe: Pipe that should be used to connect to the Discord client. Defaults to 0, can be 0-9
 :param asyncio.BaseEventLoop loop: Your own event loop (if you have one) that PyPresence should use. One will be created if not supplied. Information at `https://docs.python.org/3/library/asyncio-eventloop.html <https://docs.python.org/3/library/asyncio-eventloop.html>`_
 :param function handler: The exception handler pypresence should send asynchronous errors to. This can be a coroutine or standard function as long as it takes two arguments (exception, future). Exception will be the exception to handle and future will be an instance of asyncio.Future

|br|

  .. py:function:: connect()

     Initializes the connection - must be done in order to make any updates to Rich Presence.

     :rtype: pypresence.Response


  |br|

  .. py:function:: clear(pid=os.getpid())

    Clears the presence.

    :param int pid: the process id of your game
    :rtype: pypresence.Response


  |br|

  .. py:function:: close()

     Closes the connection.

     :rtype: pypresence.Response


  |br|

  .. py:function:: update(**options)

   Sets the user's presence on Discord.

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
   :param list buttons: list of dicts for buttons on your profile in the format ``[{"label": "My Website", "url": "https://qtqt.cf"}, ...]``, can list up to two buttons
   :param bool instance: marks the match as a game session with a specific beginning and end
   :rtype: pypresence.Response


  |br|
