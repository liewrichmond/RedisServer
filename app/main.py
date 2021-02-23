import socket
import asyncio
import select
import queue
from .parser import Parser
from .encoder import Encoder

def ping(arg):
    encoder = Encoder()
    if arg == '':
        data = encoder.encodeSimpleString("PONG")
    else:
        data = encoder.encodeSimpleString(arg)
    return data

def echo(arg):
    data = encoder.encodeSimpleString(arg)
    return data

class RedisServer():
    def __init__(self):
        self.listenSocket = None
        self.parser = Parser()
        self.connections = []
        self.messageQueue = {}

    def start(self):
         self.listenSocket = socket.create_server(('localhost', 6379), reuse_port = True, backlog = 10)
         self.listenSocket.setblocking(False)

    def serve(self):
        if(self.listenSocket is None):
            raise ValueError("Server hasn't been started yet!")

        maybeReadable = [self.listenSocket]
        maybeWriteable = []

        while True:
            readable, writeable, errors = select.select(maybeReadable, maybeWriteable, [])
            for s in readable:
                if s is self.listenSocket:
                    connection, client = self.listenSocket.accept()
                    connection.setblocking(False)
                    maybeReadable.append(connection)
                    maybeWriteable.append(connection)
            self.read(readable)
            self.write(writeable)

    def read(self, readables):
        for connection in readables:
            if connection is not self.listenSocket:
                data = connection.recv(1024)
                if data == b'':
                    continue

                commands = self.parser.decode(data)
                command = self.parser.parseCommands(commands)

                output = command.encode()

                if(connection not in self.messageQueue):
                    self.messageQueue[connection] = queue.Queue()

                self.messageQueue[connection].put(output)

    def write(self, writeables):
        for connection in writeables:
            if(connection in self.messageQueue):
                if not self.messageQueue[connection].empty():
                    message = self.messageQueue[connection].get_nowait()
                    connection.sendall(message)

async def main():
    print("Starting Server...")
    server = RedisServer()
    server.start()
    server.serve()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    #asyncio.run(main())
