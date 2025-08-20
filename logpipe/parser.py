import json
import re
from datetime import datetime

def parse_json(line):
    try:
        return json.loads(line.strip())
    except json.JSONDecodeError:
        return None

def parse_kv(line):
    """parse key=value pairs from a log line"""
    result = {}
    # get timestamp if it looks like one
    ts_match = re.match(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})', line)
    if ts_match:
        result['timestamp'] = ts_match.group(1)

    for m in re.finditer(r'(\w+)=("(?:[^"\\]|\\.)*"|\S+)', line):
        key = m.group(1)
        val = m.group(2).strip('"')
        result[key] = val
    return result if result else None

def parse_auto(line):
    """try json first, fall back to kv"""
    line = line.strip()
    if not line:
        return None
    if line.startswith('{'):
        return parse_json(line)
    return parse_kv(line)

def parse_syslog(line):
    """basic syslog format: Mon DD HH:MM:SS host process[pid]: message"""
    m = re.match(
        r'(\w+ +\d+ \d+:\d+:\d+) (\S+) (\S+?)(?:\[(\d+)\])?: (.+)',
        line.strip()
    )
    if not m:
        return None
    return {
        'timestamp': m.group(1),
        'host': m.group(2),
        'process': m.group(3),
        'pid': m.group(4) or '',
        'message': m.group(5),
    }
