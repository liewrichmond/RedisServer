
class Encoder():
    def getLengthInStr(self, length):
        temp = []
        while length >= 1:
            temp.append(length % 10)
            length = length//10

        res = ""
        for num in reversed(temp):
            res += chr(num + ord('0'))
        return res

    def encodeBulkString(self, string):
        length = self.getLengthInStr(len(string))
        strOutput = "$" + length + "\r\n" + string + "\r\n"
        return strOutput.encode('utf-8')

    def encodeSimpleString(self, string):
        strOutput = "+" + string + "\r\n"
        return strOutput.encode('utf-8')
