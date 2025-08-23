from logpipe.parser import parse_json, parse_kv, parse_auto, parse_syslog

def test_json():
    r = parse_json('{"level": "error", "msg": "oh no"}')
    assert r['level'] == 'error'
    assert r['msg'] == 'oh no'

def test_kv():
    r = parse_kv('2025-01-01T12:00:00 level=info msg="hello world" count=42')
    assert r['level'] == 'info'
    assert r['msg'] == 'hello world'
    assert r['count'] == '42'

def test_auto_json():
    r = parse_auto('{"a": 1}')
    assert r == {"a": 1}

def test_auto_kv():
    r = parse_auto('foo=bar baz=123')
    assert r['foo'] == 'bar'

def test_syslog():
    r = parse_syslog('Jan  5 14:23:01 myhost sshd[1234]: Accepted publickey')
    assert r['host'] == 'myhost'
    assert r['process'] == 'sshd'
    assert r['pid'] == '1234'

if __name__ == '__main__':
    test_json()
    test_kv()
    test_auto_json()
    test_auto_kv()
    test_syslog()
    print('ok')
