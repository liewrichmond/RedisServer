from app.encoder import Encoder

def testTest():
    assert True == True

def testEncodeBulkString1():
    out = Encoder.encodeBulkString("hello")
    assert out == b'$5\r\nhello\r\n'

def testEncodeBulkString2():
    out = Encoder.encodeBulkString("helloworld")
    assert out == b'$10\r\nhelloworld\r\n'

def testGetLengthInStr():
    out = Encoder.getLengthInStr(15)
    assert out == "15"

def testEncodeSimpleString1():
    encoder = Encoder()
    out = Encoder.encodeSimpleString("helloWorld")
    assert out == b'+helloWorld\r\n'

def testEncodeSimpleString2():
    out = Encoder.encodeSimpleString("HeLLOComPUTER")
    assert out == b'+HeLLOComPUTER\r\n'

def testEncodeBulkStringWithSpaces():
    out = Encoder.encodeBulkString("Hello World This is MoM")
    assert out == b'$23\r\nHello World This is MoM\r\n'

def testEncodeNullBulkString():
    out = Encoder.encodeBulkString("")
    assert out == b'$-1\r\n'
