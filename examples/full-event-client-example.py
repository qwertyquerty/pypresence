import asyncio
import pypresence

CLIENT_ID = 555555555555555555

loop = asyncio.get_event_loop()
c = pypresence.Client(CLIENT_ID, loop=loop)
c.start()

# Prompt user for authorization to do stuff with RPC scopes
auth = c.authorize(str(CLIENT_ID), ['rpc'])
code_grant = auth['data']['code']

'''
Implement the API found here for code/token exchange: 
https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-exchange-example
(NOTE: Redirect URI is needed and should be what's set in your Dev Application's OAuth2 screen)
'''
token = exchange_code(code_grant)  # noqa: F821

# Now authenticate with the token we got (Save to skip authorization later)
c.authenticate(token['access_token'])


def on_new_message(data):
    print("New message: %s" % data['message']['content'])


# Watch for new messages created on channel 444444444444444444
c.register_event('MESSAGE_CREATE', on_new_message, args={'channel_id': '444444444444444444'})
# Find other event types here: https://discord.com/developers/docs/topics/rpc#commands-and-events-rpc-events

loop.run_forever()
