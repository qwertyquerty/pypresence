class InvalidID(Exception):
    def __init__(self):
        super().__init__('Client ID is Invalid')
        
class InvalidPipe(Exception):
    def __init__(self):
        super().__init__('Pipe Not Found - Is Discord Running?')
