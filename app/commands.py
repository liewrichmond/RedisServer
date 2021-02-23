from .encoder import Encoder

class Command():
    PING = "ping"
    ECHO = "echo"

class Ping(Command):
    def __init__(self, payload):
        if payload == '':
            self.payload = 'PONG'
        else:
            self.payload = payload

    def __eq__(self, other):
        if self.payload == other.payload:
            return True
        else:
            return False

    def encode(self):
        return Encoder.encodeBulkString(self.payload)



class Echo(Command):
    def __init__(self, payload):
        self.payload = payload

    def __eq__(self, other):
        if self.payload == other.payload:
            return True
        else:
            return False

    def encode(self):
        return Encoder.encodeBulkString(self.payload)
