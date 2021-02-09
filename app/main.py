import socket

def main():
    print("Your code goes here!")

    s = socket.create_server(("localhost", 6379), reuse_port=True)
    connection, addr= s.accept() # wait for client

    connection.rcv(4096)







if __name__ == "__main__":
    main()
