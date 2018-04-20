from .client import Client

class Presence(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def connect():
        self.start()
        
    def update(**kwargs):
        self.set_activity(**kwargs)
        
    def close():
        self.close()
