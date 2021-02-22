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

class RedisServer():
    def __init__(self):
        self.listenSocket = None
        self.parser = Parser()
        self.connections = []
        self.messageQueue = {}

    def start(self):
         self.listenSocket = socket.create_server(('localhost', 6379), reuse_port = True, backlog = 10)
         self.listenSocket.setblocking(False)

    async def serve(self):
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
                print(data)
                cmdArray = self.parser.parseArray(data)
                cmds = self.parser.parseCommands(cmdArray)
                output = ping(cmds[0][1])

                if(connection not in self.messageQueue):
                    self.messageQueue[connection] = queue.Queue()

                self.messageQueue[connection].put(output)

    def write(self, writeables):
        for connection in writeables:
            if(connection in self.messageQueue):
                if not self.messageQueue[connection].empty():
                    message = self.messageQueue[connection].get_nowait()
                    connection.sendall(message)

    async def listenForClient(self):
        print("listening for client")
        s = socket.create_server(('localhost', 6379), reuse_port = True)
        connection, addr = s.accept()
        connection.setblocking(False)
        return connection

    async def listenForCommands(self, connection):
        print("listeningForCommands")
        connection.settimeout(20)
        parser = Parser()
        while True:
            data = connection.recv(1024)

            if data == b'':
                await asyncio.sleep(0.1)
                continue
            print("got message")
            cmdArray = parser.parseArray(data)
            cmds = parser.parseCommands(cmdArray)
            pingOutput = ping(cmds[0][1])
            connection.sendall(pingOutput)

    async def acceptNewClient(self):
        connection = await self.listenForClient()
        asyncio.create_task(self.listenForCommands(connection))

async def main():
    print("Starting Server...")
    server = RedisServer()
    server.start()
    asyncio.create_task(server.serve())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    #asyncio.run(main())
