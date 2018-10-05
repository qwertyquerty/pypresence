class PyPresenceException(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = 'An error has occured within PyPresence'
        super().__init__(message)


class InvalidID(PyPresenceException):
    def __init__(self):
        super().__init__('Client ID is Invalid')


class InvalidPipe(PyPresenceException):
    def __init__(self):
        super().__init__('Pipe Not Found - Is Discord Running?')


class InvalidArgument(PyPresenceException):
    def __init__(self, expected, received, longdesc: str = None):
        longdesc = '\n{0}'.format(longdesc) if longdesc else ''
        super().__init__('Bad argument passed. Expected {0} but got {1} instead{2}'.format(expected, received, longdesc))


class ServerError(PyPresenceException):
    def __init__(self, message: str):
        super().__init__(message.replace(']', '').replace('[', '').capitalize())


class DiscordError(PyPresenceException):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__('Error Code: {0} Message: {1}'.format(code, message))


class ArgumentError(PyPresenceException):
    def __init__(self):
        super().__init__('Supplied function must have one argument.')


class EventNotFound(PyPresenceException):
    def __init__(self, event):
        super().__init__('No event with name {0} exists.'.format(event))
