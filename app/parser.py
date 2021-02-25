from collections import namedtuple
from .resps import CRLFS, RespArray, RespBulkString
from .commands import Command, Echo, Ping, Set, Get

class Parser():
    def getLengthFromStr(self, asciiStr):
        length = 0
        for char in asciiStr:
            length = (length * 10 ) + (ord(char) - ord('0'))
        return length

    def isValidCommand(self, commandStr):
        #TODO
        return 1

    def decode(self, data):
        respType = chr(data[0])

        if respType == "*" :
            return self.decodeArray(data)
        elif respType == "$":
            return self.decodeBulkString(data)
        else:
            raise TypeError("Haven't implemented decoding that type")

    def decodeBulkString(self, data):
        asString = data.decode().split('\r\n')
        length = self.getLengthFromStr(asString[0][1:])
        payload = asString[-2]
        return payload

    def decodeArray(self, data):
        elements = []

        arrayLength = 0
        i = 1
        while chr(data[i]) != "\r":
            arrayLength = (arrayLength * 0) + (data[i] - ord('0'))
            i += 1
        i += 2

        l = i
        r = i
        while r < len(data):
            crlfCount = 0
            respType = chr(data[l])
            crlfTarget = CRLFS[respType]
            while crlfCount < crlfTarget and r < len(data):
                r+=1
                if (chr(data[r]) == "\r"):
                    crlfCount += 1
            if (r + 2 <= len(data)):
                r += 2
            element = data[l:r]
            elements.append(self.decode(element))
            l = r

        if len(elements) != arrayLength:
            raise ValueError("Badly formatted array!")
        return elements

    def parseCommands(self, array):
        commands = []

        i = 0
        # Assumes that array is either length 1 or 2 - has argument or does not have argument
        command = None
        if len(array) < 2:
            if(array[0] != Command.PING):
                raise ValueError("Invalid number of arguments for ECHO commands")
            else:
                command = Ping('')
        else:
            if(array[0] == Command.PING):
                command = Ping(array[1])
            elif (array[0] == Command.ECHO):
                command = Echo(array[1])
            elif (array[0] == Command.GET):
                command = Get(array[1])
            elif (array[0] == Command.SET):
                if(len(array) == 3):
                    command = Set(array[1], array[2])
            else:
                raise ValueError("Haven't implemented command")

        return command

    def parseBulkString(self, bulkString):
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
