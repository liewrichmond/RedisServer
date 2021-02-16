import socket
from parser import Parser
from encoder import Encoder

def ping(arg):
    encoder = Encoder()
    if arg == '':
        data = encoder.encodeSimpleString("PONG")
    else:
        data = encoder.encodeSimpleString(arg)
    return data

def main():
    #print("Starting Server...")
    s = socket.create_server(("localhost", 6379), reuse_port=True)
    connection, addr= s.accept() # wait for client

    data = connection.recv(4096)
    parser = Parser()
    cmdArray = parser.parseArray(data)
    cmds = parser.parseCommands(cmdArray)
    pingOutput = ping(cmds[0][1])
    connection.sendall(pingOutput)
    # Client commands normally array of bulk strings
    # Sample Input :   b'*1\r\n$4\r\nping\r\n'

if __name__ == "__main__":
    main()
