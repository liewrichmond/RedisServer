
class Encoder():
    @classmethod
    def getLengthInStr(cls, length):
        temp = []
        while length >= 1:
            temp.append(length % 10)
            length = length//10

        res = ""
        for num in reversed(temp):
            res += chr(num + ord('0'))
        return res

    @classmethod
    def encodeBulkString(cls, string):
        length = cls.getLengthInStr(len(string))
        strOutput = "$" + length + "\r\n" + string + "\r\n"
        return strOutput.encode('utf-8')

    @classmethod
    def encodeSimpleString(cls, string):
        strOutput = "+" + string + "\r\n"
        return strOutput.encode('utf-8')
