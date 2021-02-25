from .encoder import Encoder

class Command():
    PING = "ping"
    ECHO = "echo"
    SET = "set"
    GET = "get"

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

    def encode(self, target):
        return Encoder.encodeBulkString(self.payload)



class Echo(Command):
    def __init__(self, payload):
        self.payload = payload

    def __eq__(self, other):
        if self.payload == other.payload:
            return True
        else:
            return False

    def encode(self, target):
        return Encoder.encodeBulkString(self.payload)

class Set(Command):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def encode(self, target):
        target[self.key] = self.value
        return Encoder.encodeBulkString("OK")

class Get(Command):
    def __init__(self, key):
        self.key = key

    def encode(self, target):
        try:
            value = target[self.key]
        except KeyError:
            value = ""

        return Encoder.encodeBulkString(value)


