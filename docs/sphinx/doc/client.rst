Client()
************************

.. |br| raw:: html

   <br />


.. py:class:: Client(client_id, pipe=0, loop=None, handler=None)

 Creates the RPC client ready for usage.

 :param str client_id: OAuth2 App ID (found at https://discord.com/developers/applications/me)
 :param int pipe: Pipe that should be used to connect to the Discord client. Defaults to 0, can be 0-9
 :param asyncio.BaseEventLoop loop: Your own event loop (if you have one) that PyPresence should use. One will be created if not supplied. Information at https://docs.python.org/3/library/asyncio-eventloop.html
 :param function handler: The exception handler pypresence should send asynchronous errors to. This can be a coroutine or standard function as long as it takes two arguments (exception, future). Exception will be the exception to handle and future will be an instance of asyncio.Future

|br|

  .. py:function:: start()

    Initializes the connection - must be done in order to run RPC commands.

    :rtype: pypresence.Response


  |br|

  .. py:function:: close()

    Closes the connection.


  |br|

  .. py:function:: authorize(client_id, scopes, rpc_token=None, username=None)

     Used to authenticate a new client with your app. By default this pops up a modal in-app that asks the user to authorize access to your app.

     :param str client_id: OAuth2 application id
     :param list scopes: a list of OAuth scopes as strings
     :param str rpc_token: one-time use RPC token
     :param str username: username to create a guest account with if the user does not have Discord
     :rtype: pypresence.Response

     All the different scopes can be found `here <https://discord.com/developers/docs/topics/oauth2>`_


  |br|

  .. py:function:: authenticate(token)

   Used to authenticate an existing client with your app.

   :param int token: OAuth2 access token
   :rtype: pypresence.Response


  |br|

  .. py:function:: get_guilds()

    Used to get a list of guilds the client is in.

    :rtype: pypresence.Response


  |br|

  .. py:function:: get_channels()

    Used to get a guild's channels the client is in.

    :rtype: pypresence.Response


  |br|

  .. py:function:: channel_id()

    Used to get a channel the client is in.

    :param str channel_id: id of the channel to get
    :rtype: pypresence.Response


  |br|


  .. py:function:: set_user_voice_settings(user_id, **options)

    Used to get a channel the client is in.

    :param str user_id: user id
    :param float pan_left: left pan of the user
    :param float pan_right: right pan of the user
    :param int volume: the volume of user (defaults to 100, min 0, max 200)
    :param bool mute: the mute state of the user
    :rtype: pypresence.Response


  |br|


  .. py:function:: select_voice_channel(channel_id)

    Used to join and leave voice channels, group dms, or dms.

    :param str channel_id: channel id to join (or ``None`` to leave)
    :rtype: pypresence.Response


  |br|


  .. py:function:: get_selected_voice_channel()

    Used to get the client's current voice channel.

    :rtype: pypresence.Response


  |br|



  .. py:function:: select_text_channel(channel_id)

    Used to join and leave text channels, group dms, or dms.

    :param str channel_id: channel id to join (or ``None`` to leave)
    :rtype: pypresence.Response


  |br|


  .. py:function:: set_activity(**options)

   Used to set the activity shown on Discord profiles and status of users. Takes the following as parameters.

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


  .. py:function:: clear_activity(pid=os.getpid())

   Clear the activity.

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
   :rtype: pypresence.Response


  |br|


  .. py:function:: subscribe(event,args={})

    Used to subscribe to events.

    :param str event: event name to subscribe to
    :param dict args: any args to go along with the event
    :rtype: pypresence.Response


  |br|


  .. py:function:: unsubscribe(event,args={})

    Used to unsubscribe from events.

    :param str event: event name to unsubscribe from
    :param dict args: any args to go along with the event
    :rtype: pypresence.Response


  |br|



  .. py:function:: get_voice_settings()

    Get the user's voice settings.

    :rtype: pypresence.Response


  |br|


  .. py:function:: set_voice_settings(**options)

    Set the user's voice settings.

    :param dict _input: input settings
    :param dict output: output settings
    :param dict mode: voice mode settings
    :param bool automatic_gain_control: state of automatic gain control
    :param bool echo_cancellation: state of echo cancellation
    :param bool noise_suppression: state of noise suppression
    :param bool qos: state of voice quality of service
    :param bool silence_warning: state of silence warning notice
    :param bool deaf: state of self-deafen
    :param bool mute: state of self-mute
    :rtype: pypresence.Response


  |br|


  .. py:function:: capture_shortcut(action)

    Used to capture a keyboard shortcut entered by the user.

    :param string action: capture action, either ``'START'`` or ``'STOP'``
    :rtype: pypresence.Response


  |br|


  .. py:function:: send_activity_join_invite(user_id)

    Used to accept an Ask to Join request.

    :param str user_id: user id
    :rtype: pypresence.Response


  |br|


  .. py:function:: close_activity_request(user_id)

    Used to reject an Ask to Join request.

    :param str user_id: user id
    :rtype: pypresence.Response


  |br|


  .. py:function:: register_event(event, func, args={})

    Hook an event to a function. The function will be called whenever Discord sends that event. Will auto subscribe to it.

    :param str event: the event to hook
    :param function func: the function to pair with the event
    :param dict args: optional args used in subscription
    :rtype: pypresence.Response


  |br|


  .. py:function:: unregister_event(event, args={})

    Unhook an event from a function. Will auto unsubscribe from the event as well.

    :param str event: the event to unhook
    :param dict args: optional args used in unsubscription
    :rtype: pypresence.Response


  |br|
