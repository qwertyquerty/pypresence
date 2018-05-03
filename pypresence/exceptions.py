class InvalidID(Exception):
    def __init__(self):
        super().__init__('Client ID is Invalid')


class InvalidPipe(Exception):
    def __init__(self):
        super().__init__('Pipe Not Found - Is Discord Running?')


class ServerError(Exception):
    def __init__(self, message):
        super().__init__(message.replace(']','').replace('[','').capitalize())


class DiscordError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__('Error Code: {0} Message: {1}'.format(code, message))


class ArgumentError(Exception):
    def __init__(self):
        super().__init__('Event function must have one argument.')


class EventNotFound(Exception):
    def __init__(self, event):
        super().__init__('No event with name {0} exists.'.format(event))
