

# pypresence
A Discord RPC library in Python? Wow! Looks like you've come to the right place.

[![GitHub stars](https://img.shields.io/github/stars/qwertyquerty/pypresence.svg?style=for-the-badge&label=Stars)](https://github.com/qwertyquerty/pypresence) [![license](https://img.shields.io/github/license/qwertyquerty/pypresence.svg?style=for-the-badge)](https://github.com/qwertyquerty/pypresence/blob/master/LICENSE) ![GitHub last commit](https://img.shields.io/github/last-commit/qwertyquerty/pypresence.svg?style=for-the-badge)

[My Discord Server](https://discordapp.com/invite/uV5y7RY) | [My Patreon](https://www.patreon.com/qwertyquerty)


----------

Use this badge in your project's Readme to show you're using pypresence! The markdown code is below.

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

```markdown
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
```

----------
----------

# Documentation

**NOTE**: You need an authorized app to do anything besides rich presence!

## Installation

Install pypresence with `pip`:

`pip install https://github.com/qwertyquerty/pypresence/archive/master.zip`

or

`pip install pypresence`

----------
----------

## Rich Presence Client

Examples for this can be found in the examples folder.

`pypresence.Presence(client_id, pipe=0, loop=None, handler=None)`

Creates the class ready for usage.

* `client_id`: OAuth2 App ID  (found at https://discordapp.com/developers/applications/me) [string]
* `pipe`: Pipe that should be used to connect to the Discord client. Defaults to 0, can be 0-9. [int]
* `loop`: Your own event loop (if you have one) that PyPresence should use. One will be created if not supplied. Information at https://docs.python.org/3/library/asyncio-eventloop.html [asyncio event loop]
* `handler`: The exception handler PyPresence should send asynchronous errors to. This can be a coroutine or standard function as long as it takes two arguments (exception, future). Exception will be the exception to handle and future will be an instance of [asyncio.Future](https://docs.python.org/3/library/asyncio-task.html#asyncio.Future) [function]

----------

`Presence.connect()`

Initializes the connection - must be done in order to make any updates to Rich Presence.

----------

`Presence.clear(pid=os.getpid())`

Clear the presence.

----------

`Presence.close()`

Closes the connection.

----------

`Presence.update(**options)`

Sets the user's presence on Discord. Takes the following as parameters.

* `pid`: the process id of your game `[int]`
* `state`: the user's current status `[string]`
* `details`: what the player is currently doing`[string]`
* `start`: seconds for game start `[int]` 
* `end`: seconds for game end `[int]` 
* `large_image`: name of the uploaded image for the large profile artwork `[string]` 
* `large_text`: tooltip for the large image `[string]` 
* `small_image`: name of the uploaded image for the small profile artwork `[string]`
* `small_text`: tootltip for the small image `[string]` 
* `party_id`: id of the player's party, lobby, or group `[string]`
* `party_size`: current size of the player's party, lobby, or group, and the max in this format: `[1,4]` `[list]`
* `join`: unique hashed string for chat invitations and ask to join `[string]`
* `spectate`: unique hashed string for spectate button `[string]`
* `match`: unique hashed string for spectate and join `[string]`
* `instance`: marks the match as a game session with a specific beginning and end `[bool]`

----------
----------

## RPC Client

`pypresence.Client(client_id, pipe=0)`

Construct the Client.

* `client_id`: OAuth2 application id `[string]`
* `pipe`: The pipe number to use, usually should be 0, can be 0-9 `[int]`

----------

`Client.start()`

Initializes the connection - must be done in order to run RPC commands.

----------

`Client.close()`

Closes the connection.

----------

`Client.authorize(client_id, scopes, rpc_token=None, username=None)`

Used to authenticate a new client with your app. By default this pops up a modal in-app that asks the user to authorize access to your app.

* `client_id`: OAuth2 application id `[string]`
* `scopes`: a list of OAuth scopes as strings `[list]`
* `rpc_token`: one-time use RPC token `[string]`
* `username`:	username to create a guest account with if the user does not have Discord `[string]`

All the different scopes can be found here: [https://discordapp.com/developers/docs/topics/oauth2](https://discordapp.com/developers/docs/topics/oauth2)

----------

`Client.authenticate(token)`

Used to authenticate an existing client with your app.

* `token`: OAuth2 access token `[string]`

----------

`Client.get_guilds()`

Used to get a list of guilds the client is in.

----------

`Client.get_guild(guild_id)`

Used to get a guild the client is in.

* `guild_id`: id of the guild to get `[string]`

----------

`Client.get_channels(guild_id)`

Used to get a guild's channels the client is in.

* `guild_id`: id of the guild to get channels for `[string]`

----------

`Client.get_channel(channel_id)`

Used to get a channel the client is in.

* `channel_id`: id of the channel to get `[string]`

----------

`Client.set_user_voice_settings(user_id, pan_left=None, pan_right=None, volume=None, mute=None)`

Used to change voice settings of users in voice channels.

* `user_id`: user id `[string]`
* `pan_left`: left pan of the user `[float]`
* `pan_right`: right pan of the user `[float]`
* `volume`: the volume of user (defaults to 100, min 0, max 200) `[int]`
* `mute`: the mute state of the user `[bool]`

----------

`Client.select_voice_channel(channel_id)`

Used to join and leave voice channels, group dms, or dms.

* `channel_id`: channel id to join (or `None` to leave) `[string]`

----------

`Client.get_selected_voice_channel()`

Used to get the client's current voice channel.

----------

`Client.select_text_channel(channel_id)`

Used to join and leave text channels, group dms, or dms.

* `channel_id`: channel id to join (or `None` to leave) `[string]`

----------

`Client.set_activity(pid=os.getpid(), state=None, details=None, start=None, end=None, large_image=None, large_text=None, small_image=None, small_text=None, party_id=None, party_size=None, join=None, spectate=None, match=None, instance=True)`

Used to set the activity shown on Discord profiles and status of users.

* `pid`: the process id of your game `[int]`
* `state`: the user's current status `[string]`
* `details`: what the player is currently doing`[string]`
* `start`: seconds for game start `[int]` 
* `end`: seconds for game end `[int]` 
* `large_image`: name of the uploaded image for the large profile artwork `[string]` 
* `large_text`: tooltip for the large image `[string]` 
* `small_image`: name of the uploaded image for the small profile artwork `[string]`
* `small_text`: tootltip for the small image `[string]` 
* `party_id`: id of the player's party, lobby, or group `[string]`
* `party_size`: current size of the player's party, lobby, or group, and the max in this format: `[1,4]` `[list]`
* `join`: unique hashed string for chat invitations and ask to join `[string]`
* `spectate`: unique hashed string for spectate button `[string]`
* `match`: unique hashed string for spectate and join `[string]`
* `instance`: marks the match as a game session with a specific beginning and end `[bool]`

----------

`Client.clear_activity(pid=os.getpid())`

Clear the activity.

----------

`Client.subscribe(event,args={})`

Used to subscribe to events.

* `event`: event name to subscribe to `[string]`
* `args`: any args to go along with the event `[dict]`

----------

`Client.unsubscribe(event,args={})`

Used to unsubscribe from events.

* `event`: event name to unsubscribe from `[string]`
* `args`: any args to go along with the event `[dict]`

----------

`Client.get_voice_settings()`

Get the user's voice settings.

----------

`Client.set_voice_settings(self, _input=None, output=None, mode=None, automatic_gain_control=None, echo_cancellation=None, noise_suppression=None, qos=None, silence_warning=None, deaf=None, mute=None)`

Set the user's voice settings.

* `_input`: input settings `[dict]`
* `output`: output settings `[dict]`
* `mode`: voice mode settings`[dict]`
* `automatic_gain_control`: state of automatic gain control `[bool]` 
* `echo_cancellation`: state of echo cancellation `[bool]` 
* `noise_suppression`: state of noise suppression `[bool]` 
* `qos`: state of voice quality of service `[bool]` 
* `silence_warning`: state of silence warning notice `[bool]`
* `deaf`: state of self-deafen `[bool]` 
* `mute`: state of self-mute `[bool]`

----------

`Client.capture_shortcut(action)`

Used to capture a keyboard shortcut entered by the user.

* `action`: capture action, either START or STOP `[string]`

----------

`Client.send_activity_join_invite(user_id)`

Used to accept an Ask to Join request.

* `user_id`: user id `[string]`

----------

`Client.close_activity_request(user_id)`

Used to reject an Ask to Join request.

* `user_id`: user id `[string]`

----------

----------

## Events

`Client.register_event(event, func, args={})`

Hook an event to a function. The function will be called whenever Discord sends that event. Will auto subscribe to it.

* `event`: the event to hook `[string]`
* `func`: the function to pair with the event `[function]`
* `args`: optional args used in subscription `[dict]`

----------

`Client.unregister_event(event, args={})`

Unhook an event from a function. Will auto unsubscribe from the event as well.

* `event`: the event to unhook `[string]`
* `args`: optional args used in unsubscription `[dict]`

----------

----------

## Examples

Examples can be found in the [examples](https://github.com/qwertyquerty/pypresence/tree/master/examples) directory, and you can contribute your own examples if you wish, just read [examples.md](https://github.com/qwertyquerty/pypresence/blob/master/examples/examples.md)!

Furthermore, here is a list of repositories that use pypresence:

| Repository | Author |
|:---:|:---:|
| [anime-rpc](https://github.com/cheddar-cheeze/anime-rpc) | cheddar-cheeze |
| [switchcord](https://github.com/TemTemmie/switchcord) | TemTemmie |
| [osu-rpc-linux](https://github.com/diamondburned/osu-rpc-linux) | diamondburned |
| [taiko3-discord-rpc](https://github.com/bui/taiko3-discord-rpc) | bui |
| [HQMediaPlayer](https://github.com/DAgostinateur/HQMediaPlayer) | DAgonstinateur |
| [WowDiscordRichPresence](https://github.com/Arwic/WowDiscordRichPresence) | Arwic |
| [discord-rpc-mpris](https://github.com/RayzrDev/discord-rpc-mpris) | RayzrDev |
| [ss13rp](https://github.com/qwertyquerty/ss13rp) | qwertyquerty |
| [DiscordRPGUI](https://github.com/Elliot-Potts/DiscordRPGUI) | Elliot-Potts |

----------

### Welp, you made it all the way through the docs. If you see any errors or incorrect items, please do make a pull request!
