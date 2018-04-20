from .client import Client

class Presence(Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def connect():
        super().start()
        
    def update(**kwargs):
        super().set_activity(**kwargs)
        
    def close():
        super().close()
