import socket
import time
import asyncio

async def sendSimpleBulkString():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost',6379))
    print("connected")
    s2.connect(('localhost', 6379))
    print("connected 2")

    s.sendall(b'*1\r\n$4\r\nping\r\n')
    print("sent")
    s2.sendall(b'*5\r\n$3\r\nset\r\n$5\r\nhello\r\n$5\r\nworld\r\n$2\r\npx\r\n$2\r\n10\r\n')
    print("sent")

    s.settimeout(5)
    s2.settimeout(5)

    data = s.recv(1024)
    data2 = s2.recv(1024)

    print(data)
    print(data2)

    s2.sendall(b'*2\r\n$3\r\nget\r\n$5\r\nhello\r\n')
    data2 = s2.recv(1024)
    print(data2)
    await asyncio.sleep(0.5)

    s2.sendall(b'*2\r\n$3\r\nget\r\n$5\r\nhello\r\n')
    data2 = s2.recv(1024)
    print(data2)
    #s.settimeout(5)
    #data = s.recv(1024)
    #print(data)

    #time.sleep(5)
    #s.sendall(b'*2\r\n$4\r\nping\r\n$10\r\nhelloworld\r\n')
    #data = s.recv(1024)
    #print(data)

    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:


if __name__=="__main__":
    asyncio.run(sendSimpleBulkString())
