*copy pasted from Qweko Dev Discord - check pins*

Client Authorization Example (For using Client's methods)
```py
import pypresence
c = pypresence.Client(CLIENT_ID)
c.start()
auth = c.authorize(CLIENT_ID, ['rpc'])  # If you need other scopes, add them
code_grant = auth.code
# Exchange code grant for token, rtfd
# Now each time you can use
c.authenticate(oauth2token)
```
You *will* need a redirect URI set in your application. localhost/randomendpoint should work, but you'll also have to listen for any requests sent to it. It'll return an oauth2 code, which you send to the Token URL (read the docs), in return for a Oauth2 token to use with `Client.authenticate(token)` that means they dont need to auth it every time.
