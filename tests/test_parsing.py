from app.parser import Parser
from app.resps import RespBulkString, RespArray
from app.commands import Ping, Echo

def testTest():
    assert True == 1

def testParseBulkString():
    parser = Parser()
    output = parser.parseBulkString(b'$6\r\nfoobar\r\n')
    assert output == "foobar"

def testParseArray():
    parser = Parser()
    el1 = RespBulkString(4, 'ping')
    el2 = RespBulkString(6, 'foobar')
    expected = [el1, el2]
    expected = ['ping', 'foobar']
    output = parser.decodeArray(b'*2\r\n$4\r\nping\r\n$6\r\nfoobar\r\n')
    assert output == expected

def testParseCommands():
    parser = Parser()
    expected = Ping('foobar')
    output = parser.decodeArray(b'*2\r\n$4\r\nping\r\n$6\r\nfoobar\r\n')
    o = parser.parseCommands(output)
    assert o == expected

def testParseArrayEmptyArg():
    parser = Parser()
    output = parser.decodeArray(b'*1\r\n$4\r\nping\r\n')
    expected = Ping('')
    cmdOutput = parser.parseCommands(output)
    assert cmdOutput == expected

def testGetLength():
    parser = Parser()
    output = parser.getLengthFromStr ('100')
    assert output == 100

def testGetLength2():
    parser = Parser()
    output = parser.getLengthFromStr ('42069')
    assert output == 42069

def testParseInt():
    parser = Parser()
    out = parser.decode(b':1\r\n')
    assert out == 1

def testParseInt2():
    parser = Parser()
    out = parser.decode(b':2468\r\n')
    assert out == 2468
