import socket

def parseBulkString(bulkString):
    if(chr(bulkString[0]) != "$"):
        raise TypeError("Invalid Bulk String formatting")
    length = 0
    strPtr = 1

    while (chr(bulkString[strPtr]) != "\r") :
        length += (length*10) + (bulkString[strPtr]-ord('0'))
        strPtr += 1

    if length > 512:
        raise ValueError("Input Bulk String cannot be longer than 512 bytes!")

    strPtr += 2
    stringValue = bulkString[strPtr:strPtr+length]
    return stringValue.decode()

def main():
    print("Starting Server...")
    s = socket.create_server(("localhost", 6379), reuse_port=True)
    connection, addr= s.accept() # wait for client

    data = connection.recv(4096)
    # Client commands normally array of bulk strings
    print(data)
    inputStr = data
    output = parseBulkString(inputStr)






if __name__ == "__main__":
    main()
