<!---Documatic-section-fixed: top1-start--->
> A Discord Rich Presence Client in Python? Looks like you've come to the right place.

[![GitHub stars](https://img.shields.io/github/stars/qwertyquerty/pypresence.svg?style=for-the-badge&label=Stars)](https://github.com/qwertyquerty/pypresence) [![license](https://img.shields.io/github/license/qwertyquerty/pypresence.svg?style=for-the-badge)](https://github.com/qwertyquerty/pypresence/blob/master/LICENSE) ![GitHub last commit](https://img.shields.io/github/last-commit/qwertyquerty/pypresence.svg?style=for-the-badge) ![GitHub top language](https://img.shields.io/github/languages/top/qwertyquerty/pypresence.svg?style=for-the-badge) ![PyPI](https://img.shields.io/pypi/v/pypresence.svg?style=for-the-badge)

**Last updated:** 2022-01-19\
_Document generation aided by **Documatic**_

## NOTE: Only Python versions 3.8 and above are supported.

### [Documentation](https://qwertyquerty.github.io/pypresence/html/index.html), [Discord Server](https://discord.gg/JF3kg77), [Patreon](https://www.patreon.com/qwertyquerty)

----------

**Use this badge in your project's Readme to show you're using pypresence! The markdown code is below.**

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

```markdown
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
```
<!---Documatic-section-fixed: top1-end--->

<!---Documatic-section-group: helloworld-start--->
## Getting started

<!---Documatic-section-helloworld: setup-start--->

### Requirements

* python 3.8 or greater

<details>
  <summary>Click to see why</summary>

  The code uses f-strings in `pypresence/utils.py`
</details>



`pypresence` is pip-installable.
Clone the repository
and run `pip install -e .` in top-level directory
to install package in locally.
Alternatively,
install from pypi
```
pip install pypresence
```


<!---Documatic-section-helloworld: setup-end--->

<!---Documatic-section-helloworld: entrypoints-start--->


## Entrypoints

There are 5 source code objects in top-level `__main__`/`__init__`:

These entrypoints are broken down into the following modules:

* `pypresence.client` has 2 entrypoints
* `pypresence.presence` has 2 entrypoints
* `pypresence.baseclient` has 1 entrypoints

### pypresence.baseclient.BaseClient

```python
class BaseClient(self, client_id: str, **kwargs)
        Possible kwargs include "pipe", "loop", "handler", "isasync"
        Can raise `PyPresenceError`, `InvalidArgument`
```

`BaseClient` is a base class;
it has child classes:

* `pypresence/client/Client`
* `pypresence/client/AioClient`
* `pypresence/presence/Presence`
* `pypresence/presence/AioPResence`

`BaseClient` has asynchronous methods.

### pypresence.client.Client

```python
class Client(self, *args, **kwargs)
```

`Client` inherits from `pypresence/baseclient/BaseClient`

### pypresence.client.AioClient

```python
class AioClient(self, *args, **kwargs)
```

`AioClient` inherits from `pypresence/baseclient/BaseClient`


### pypresence.presence.Presence

```python
class Presence(self, *args, **kwargs)
```

`Presence` inherits from `pypresence/baseclient/BaseClient`

### pypresence.presence.AioPresence

```python
class AioPresence(self, *args, **kwargs)
```

`AioPresence` inherits from `pypresence/baseclient/BaseClient`


<!---Documatic-section-helloworld: entrypoints-end--->

## Examples

Basic Rich Presence:
```python
from pypresence import Presence
import time

client_id = '64567352374564'  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect() # Start the handshake loop

print(RPC.update(state="Lookie Lookie", details="A test of qwertyquerty's Python Discord RPC wrapper, pypresence!"))  # Set the presence

while True:  # The presence will stay on as long as the program is running
    time.sleep(15) # Can only update rich presence every 15 seconds

```

Rich Presence to show CPU usage:
```python
import psutil
from pypresence import Presence
import time

client_id = '64567352374564'  # Fake ID, put your real one here
RPC = Presence(client_id,pipe=0)  # Initialize the client class
RPC.connect() # Start the handshake loop


while True:  # The presence will stay on as long as the program is running
    cpu_per = round(psutil.cpu_percent(),1) # Get CPU Usage
    mem = psutil.virtual_memory()
    mem_per = round(psutil.virtual_memory().percent,1)
    print(RPC.update(details="RAM: "+str(mem_per)+"%", state="CPU: "+str(cpu_per)+"%"))  # Set the presence
    time.sleep(15) # Can only update rich presence every 15 seconds
```

Rich Presence to loop through quotes:
```python
from pypresence import Presence
import time
import random

client_id = '64567352374564'  # Put your Client ID here, this is a fake ID
RPC = Presence(client_id)  # Initialize the Presence class
RPC.connect()  # Start the handshake loop


quotes = [
    "If you can dream it, you can achieve it.",
    "Either write something worth reading or do something worth writing.",
    "You become what you believe.",
    "Fall seven times and stand up eight.",
    "The best revenge is massive success.",
    "Eighty percent of success is showing up.",
    "Life is what happens to you while you’re busy making other plans.",
    "Strive not to be a success, but rather to be of value.",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Everything you’ve ever wanted is on the other side of fear."
]  # The quotes to choose from


while True:  # The presence will stay on as long as the program is running
    RPC.update(details="Famous Quote:", state=random.choice(quotes)) #Set the presence, picking a random quote
    time.sleep(60) #Wait a wee bit
```


<!---Documatic-section-group: helloworld-end--->

<!--Documatic-section-group: developers-start--->

## Developers

<!---Documatic-section-developers: ci-start--->
The project uses GitHub Actions for CI/CD.

| File | Purpose |
|:-----|:--------|
| .github/workflows/lint_python | Runs on pull request or push on every branch. Runs code linting (black, isort, mypy, bandit) and testing (pytest) |
| .github/workflows/publish-to-pypi | Runs on release. Uploads package to pypi |


<!---Documatic-section-developers: ci-end--->

There are no unit tests for `pypresence`.


<!---Documatic-section-group: developers-end--->

<!---Documatic-section-fixed: bottom2-start--->
----------

<!---Documatic-section-fixed: bottom2-end--->
<!---Documatic-section-fixed: bottom1-start--->
## Documentation

> **NOTE**: You need an **authorized app** to do anything besides rich presence!

####  [pypresence Documentation](https://qwertyquerty.github.io/pypresence/html/index.html)
####  [Discord Rich Presence Documentation](https://discordapp.com/developers/docs/rich-presence/how-to)
####  [Discord RPC Documentation](https://discordapp.com/developers/docs/topics/rpc)
####  [pyresence Discord Support Server](https://discord.gg/JF3kg77)
####  [Discord API Support Server](https://discord.gg/discord-api)



----------
Written by: [qwertyquerty](https://github.com/qwertyquerty)

Notable Contributors: [GiovanniMCMXCIX](https://github.com/GiovanniMCMXCIX), [GhostofGoes](https://github.com/GhostofGoes)
<!---Documatic-section-fixed: bottom1-end--->
