from .client import Client

class Presence(Client):
    def __init__(self, **kwargs):
        self.super().__init__(**kwargs)
        
    def connect():
        self.super().start()
        
    def update(**kwargs):
        self.super().set_activity(**kwargs)
        
    def close():
        self.super().close()
