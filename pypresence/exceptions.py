class PyPresenceException(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "An error has occurred within PyPresence"
        super().__init__(message)


class DiscordNotFound(PyPresenceException):
    def __init__(self):
        super().__init__(
            "Could not find Discord installed and running on this machine."
        )


class InvalidID(PyPresenceException):
    def __init__(self):
        super().__init__("Client ID is Invalid")


class InvalidPipe(PyPresenceException):
    def __init__(self):
        super().__init__("Pipe Not Found - Is Discord Running?")


class InvalidArgument(PyPresenceException):
    def __init__(self, expected, received, description: str = None):
        description = f"\n{description}" if description else ""
        super().__init__(
            "Bad argument passed. Expected {} but got {} instead{}".format(
                expected, received, description
            )
        )


class ServerError(PyPresenceException):
    def __init__(self, message: str):
        super().__init__(message.replace("]", "").replace("[", "").capitalize())


class DiscordError(PyPresenceException):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Error Code: {code} Message: {message}")


class ArgumentError(PyPresenceException):
    def __init__(self):
        super().__init__("Supplied function must have one argument.")


class EventNotFound(PyPresenceException):
    def __init__(self, event):
        super().__init__(f"No event with name {event} exists.")
