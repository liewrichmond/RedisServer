from app.commands import Ping, Echo, Set, Get

def test_test():
    assert True == True

def testEmptyPing():
    command = Ping('')
    expected = b'$4\r\nPONG\r\n'
    assert command.encode({}) == expected

def testSet1():
    data = {}
    command = Set('hello', 'world')
    out = command.encode(data, {})
    assert data == {'hello': 'world'}
    assert out == b'$2\r\nOK\r\n'

def testSet2():
    data = {}
    command = Set(1, "1")
    out = command.encode(data, {})
    assert data == {1 : "1"}
    assert out == b'$2\r\nOK\r\n'

def testSet2():
    data = {"hello": "world"}
    command = Set("hello", "world2")
    out = command.encode(data, {})
    assert data =={"hello" : "world2"}
    assert out == b'$2\r\nOK\r\n'

def testSet3():
    data = {"hello" : "world"}
    command = Set("jello", "shot")
    out = command.encode(data, {})
    assert data =={"hello" : "world",
                   "jello" : "shot"}
    assert out == b'$2\r\nOK\r\n'

def testGet1():
    data = {"hello" : "world"}
    command = Get("hello")
    out = command.encode(data)
    assert out == b'$5\r\nworld\r\n'

def testGet2():
    data = {}
    command = Get("hello")
    out = command.encode(data)
    assert out == b'$-1\r\n'
