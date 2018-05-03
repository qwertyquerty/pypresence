class InvalidID(Exception):
    def __init__(self):
        super().__init__('Client ID is Invalid')


class InvalidPipe(Exception):
    def __init__(self):
        super().__init__('Pipe Not Found - Is Discord Running?')


class ServerError(Exception):
    def __init__(self, message):
        super().__init__(message.replace(']','').replace('[','').capitalize())


class ArgumentError(Exception):
    def __init__(self, message):
        super().__init__('Event function can only have one argument.')


class EventNotFound(Exception):
    def __init__(self, event):
        super().__init__('No event with name {0} exists.'.format(event))
