Feel free to contribute to this repository with pull requests! Here are some guidelines:

* Don't contribute to remove something, only to add something.
* Feel free to contribute by cleaning up the code.
* Fix my bad code (there's lots of it.)
* Contributions must be fully tested before you do a PR.

And that's it!


## Running the tests
The Tox tests are currently deprecated as there is no way to run Discord on the test machine. If you want to contribute to testing, you can fake the Discord client and add some tests.

~~Before running the tests, make sure the following are done~~:
1. ~~Install Python 3.8, 3.9 and 3.10~~
2. ~~Add a valid Discord application ID to the environment variable PYPRESENCE_CLIENT_ID (Windows Search -> "Environment variables")~~

```bash
# Install dependencies
pip3 install --user -U setuptools tox codespell flake8

# Run the functional tests
tox

# Check spelling
tox -e spellcheck

# Check code quality and formatting
tox -e flake8
```

