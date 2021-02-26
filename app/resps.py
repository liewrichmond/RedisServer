CRLFS = {
    "*" : 1,
    "$" : 2,
    ":" : 1
}

class RespArray():
    def calculateLength(data):
        self. length = 0
        #while data <
        for char in data:
            length = (length * 10 ) + (ord(char) - ord('0'))

    def __init__(self, length, elements):
        self.elements = elements
        self.length = length
        if(len(elements) != length):
            raise ValueError("Incompatible Lengths")

    def __str__(self):
        string = "["
        for element in self.elements:
            string += str(element)
            if element != self.elements[-1] :
                string += ", "
        string += "]"
        return string

    def __eq__(self, other):
        if self.length == other.length and self.elements == other.elements:
            return True
        else:
            return False

class RespBulkString():
    def __init__(self, length, payload):
        if len(payload) != length :
            raise ValueError("Incompatible Lengths")
        self.payload = payload
        self.length = length

    def __str__(self):
        return self.payload

    def __eq__(self, other):
        if self.length == other.length and self.payload == other.payload:
            return True
        else:
            return False

class RespInteger():
    def __init__(self, payload):
        self.payload = payload

    def __str__(self):
        return str(self.payload)

    def __eq__(self, other):
        if self.payload == other.payload:
            return True
        else:
            return False



