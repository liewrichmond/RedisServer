import socket

def main():
    print("Your code goes here!")

    s = socket.create_server(("localhost", 6379), reuse_port=True)
    connection, addr= s.accept() # wait for client

    data = connection.recv(4096)
    print(data)







if __name__ == "__main__":
    main()
