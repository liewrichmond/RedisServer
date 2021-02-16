from collections import namedtuple

class Parser():
    def parse(self, rawBytes):
        # main function to kick start parsing. Call other parsing methods here maybe?
        return 1

    def getLengthFromStr(self, asciiStr):
        length = 0
        for char in asciiStr:
            length = (length * 10 ) + (ord(char) - ord('0'))
        return length

    def isValidCommand(self, commandStr):
        #TODO
        return 1

    def parseArray(self, rawArray):
        splitStr = rawArray.decode().split('\r\n')

        if (splitStr[0][0] != "*") :
            raise TypeError("Input bytes was not a valid RESP array")

        arrLen  = self.getLengthFromStr(splitStr[0][1:])
        result = []
        for i in range(1, 1 + 2*arrLen):
            item = splitStr[i]
            if(item[0] == "$"):
                result.append(splitStr[i+1])

        return(result)

    def parseCommands(self, strArray):
        commandArr = []
        Command = namedtuple("Command", ["command", "args"])

        i = 0
        while i < len(strArray):
            c = None
            if strArray[i] == 'ping':
                if strArray[i + (i+1 < len(strArray))] != "ping":
                    c = ('ping', strArray[i+1])
                    i += 2
                else:
                    c = ('ping', '')
                    i += 1
            commandArr.append(c)

        return commandArr

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
