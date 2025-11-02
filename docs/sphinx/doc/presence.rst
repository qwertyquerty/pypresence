Presence
========================

.. autoclass:: pypresence.Presence
   :members:
   :undoc-members:
   :show-inheritance:


AioPresence
========================

.. autoclass:: pypresence.AioPresence
   :members:
   :undoc-members:
   :show-inheritance:


ActivityType Enum
*****************

.. autoclass:: pypresence.types.ActivityType
   :show-inheritance:

The ``ActivityType`` enum specifies what type of activity is being displayed.

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


StatusDisplayType Enum
**********************

.. autoclass:: pypresence.types.StatusDisplayType
   :show-inheritance:

The ``StatusDisplayType`` enum controls which field from your presence is displayed in the user's status.

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
