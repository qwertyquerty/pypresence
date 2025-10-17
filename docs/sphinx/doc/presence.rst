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
   :param ActivityType activity_type: the type of activity (PLAYING, LISTENING, WATCHING, or COMPETING). See :ref:`activity-types` for more details. Defaults to PLAYING if not specified.
   :param StatusDisplayType status_display_type: which field to display in the status (NAME, STATE, or DETAILS). See :ref:`status-display-types` for more details. Defaults to NAME if not specified.
   :param str state: the user's current status
   :param str state_url: URL to make the state text clickable (opens when state is clicked)
   :param str details: what the player is currently doing
   :param str details_url: URL to make the details text clickable (opens when details is clicked)
   :param str name: directly set what discord will display in places like the user list
   :param int start: epoch time for game start (in seconds, will be converted to milliseconds)
   :param int end: epoch time for game end (in seconds, will be converted to milliseconds)
   :param str large_image: name of the uploaded image for the large profile artwork
   :param str large_text: tooltip for the large image
   :param str large_url: URL to make the large image clickable (opens when large image is clicked)
   :param str small_image: name of the uploaded image for the small profile artwork
   :param str small_text: tootltip for the small image
   :param str small_url: URL to make the small image clickable (opens when small image is clicked)
   :param str party_id: id of the player's party, lobby, or group
   :param list party_size: current size of the player's party, lobby, or group, and the max in this format: ``[1,4]``
   :param str join: unique hashed string for chat invitations and ask to join
   :param str spectate: unique hashed string for spectate button
   :param str match: unique hashed string for spectate and join
   :param list buttons: list of dicts for buttons on your profile in the format ``[{"label": "My Website", "url": "https://qtqt.cf"}, ...]``, can list up to two buttons
   :param bool instance: marks the match as a game session with a specific beginning and end
   :rtype: pypresence.Response


  |br|


.. _activity-types:

ActivityType Enum
*****************

The ``ActivityType`` enum specifies what type of activity is being displayed. It is imported from ``pypresence.types``.

Available values:

- ``ActivityType.PLAYING`` (0) - Shows "Playing {game name}" (default)
- ``ActivityType.LISTENING`` (2) - Shows "Listening to {name}"
- ``ActivityType.WATCHING`` (3) - Shows "Watching {name}"
- ``ActivityType.COMPETING`` (5) - Shows "Competing in {name}"

Example usage::

    from pypresence import Presence
    from pypresence.types import ActivityType

    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(
        activity_type=ActivityType.LISTENING,
        details="My Favorite Song",
        state="By My Favorite Artist"
    )

Note: Discord only supports activity types 0, 2, 3, and 5. Types 1 (STREAMING) and 4 (CUSTOM) are not available via Rich Presence.

|br|


.. _status-display-types:

StatusDisplayType Enum
**********************

The ``StatusDisplayType`` enum controls which field from your presence is displayed in the user's status. It is imported from ``pypresence.types``.

Available values:

- ``StatusDisplayType.NAME`` (0) - Displays the application name (default)
- ``StatusDisplayType.STATE`` (1) - Displays the ``state`` field
- ``StatusDisplayType.DETAILS`` (2) - Displays the ``details`` field

Example usage::

    from pypresence import Presence
    from pypresence.types import StatusDisplayType

    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(
        status_display_type=StatusDisplayType.STATE,
        state="Custom Status Message",
        details="What I'm doing"
    )

This allows you to control what appears in the user's Discord status bar while maintaining all information in the full Rich Presence display.

|br|


.. _clickable-urls:

Clickable URLs
**************

The URL parameters (``state_url``, ``details_url``, ``large_url``, ``small_url``) allow you to make text and images in your Rich Presence clickable. When a user clicks on the associated element, Discord will open the specified URL.

**Available URL Parameters:**

- ``state_url`` - Makes the state text clickable
- ``details_url`` - Makes the details text clickable
- ``large_url`` - Makes the large image clickable
- ``small_url`` - Makes the small image clickable

**Example: Clickable State and Details**::

    from pypresence import Presence

    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(
        state="Playing an Awesome Game",
        state_url="https://example.com/game",
        details="In the Main Menu",
        details_url="https://example.com/game/menu"
    )

**Example: Clickable Images**::

    RPC.update(
        large_image="game_logo",
        large_text="My Game",
        large_url="https://example.com/game",
        small_image="status_icon",
        small_text="Online",
        small_url="https://example.com/status"
    )

**Example: Combining URLs with Buttons**::

    RPC.update(
        state="Building Something Cool",
        state_url="https://github.com/username",
        details="pypresence with URL support",
        details_url="https://github.com/qwertyquerty/pypresence",
        large_image="project_logo",
        large_url="https://project-website.com",
        buttons=[
            {"label": "View Project", "url": "https://github.com/username/project"},
            {"label": "Documentation", "url": "https://docs.project.com"}
        ]
    )

**Notes:**

- URLs work independently - you can set a URL even without the corresponding text/image field
- URLs must be valid HTTP/HTTPS URLs
- Clicking on the element will open the URL in the user's default browser
- This feature enhances interactivity beyond the traditional button limit (max 2 buttons)

|br|
