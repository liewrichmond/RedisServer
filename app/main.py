import socket
import asyncio
from .parser import Parser
from .encoder import Encoder

def ping(arg):
    encoder = Encoder()
    if arg == '':
        data = encoder.encodeSimpleString("PONG")
    else:
        data = encoder.encodeSimpleString(arg)
    return data

async def listenForCommands(connection):
    print("listening for commands")
    connection.settimeout(20)
    parser = Parser()
    while True:
        data = connection.recv(1024)

        if data == b'':
            continue

        cmdArray = parser.parseArray(data)
        cmds = parser.parseCommands(cmdArray)
        pingOutput = ping(cmds[0][1])
        connection.sendall(pingOutput)

class RedisServer():
    def __init__(self):
        self.connections = []

    async def listenForClient(self):
        print("listening for client")
        s = socket.create_server(('localhost', 6379), reuse_port = True)
        connection, addr = s.accept()
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
    loop = asyncio.get_event_loop()
    listenTask = asyncio.create_task(server.acceptNewClient())
    while True:
        await asyncio.sleep(0.1)
        if(listenTask.done()):
            listenTask = asyncio.create_task(server.acceptNewClient())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    #asyncio.run(main())
