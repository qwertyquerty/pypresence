# pypresence
A Discord rich presence library in python! Wow!

## So you want docs? Fine.


### The Client

`client(client_id)`

* `client_id`: OAuth2 application id `[string]`

----------

`client.authorize(client_id, scopes)`

Used to authenticate a new client with your app. By default this pops up a modal in-app that asks the user to authorize access to your app.

* `client_id`: OAuth2 application id `[string]`
* `scopes`: a list of OAuth scopes as strings `[list]`

----------

`client.authenticate(token)`

Used to authenticate an existing client with your app.

* `token`: OAuth2 access token `[string]`

----------

`client.get_guilds()`

Used to get a list of guilds the client is in.

----------

`client.get_guild(guild_id)`

Used to get a guild the client is in.

* `guild_id`: id of the guild to get `[string]`

----------

`client.get_channels(guild_id)`

Used to get a guild's channels the client is in.

* `guild_id`: id of the guild to get channels for `[string]`

----------

`client.get_channel(channel_id)`

Used to get a channel the client is in.

* `channel_id`: id of the channel to get `[string]`

----------

`client.set_user_voice_settings(user_id, pan_left=None, pan_right=None,volume=None, mute=None)`

Used to change voice settings of users in voice channels.

* `user_id`: user id `[string]`
* `pan_left`: left pan of the user `[float]`
* `pan_right`: right pan of the user `[float]`
* `volume`: the volume of user (defaults to 100, min 0, max 200) `[int]`
* `mute`: the mute state of the user `[bool]`

----------
