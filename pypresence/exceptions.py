class PyPresenceException(Exception):
    def __init__(self, message=None):
        if message is None: message = 'An error has occured within PyPresence'
        super().__init__(message)

class InvalidID(PyPresenceException):
    def __init__(self):
        super().__init__('Client ID is Invalid')


class InvalidPipe(PyPresenceException):
    def __init__(self):
        super().__init__('Pipe Not Found - Is Discord Running?')


class ServerError(PyPresenceException):
    def __init__(self, message):
        super().__init__(message.replace(']','').replace('[','').capitalize())


class DiscordError(PyPresenceException):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__('Error Code: {0} Message: {1}'.format(code, message))

class ArgumentError(PyPresenceException):
    def __init__(self):
        super().__init__('Supplied function must have one argument.')


class EventNotFound(PyPresenceException):
    def __init__(self, event):
        super().__init__('No event with name {0} exists.'.format(event))
