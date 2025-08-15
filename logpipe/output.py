import json
import sys

def format_record(record, fields=None, fmt='text'):
    if not record:
        return None

    if fields:
        record = {k: record.get(k, '') for k in fields}

    if fmt == 'json':
        return json.dumps(record)
    elif fmt == 'csv':
        return ','.join(str(v) for v in record.values())
    else:
        # text: key=value pairs
        parts = []
        for k, v in record.items():
            parts.append(f'{k}={v}')
        return ' '.join(parts)

class Output:
    def __init__(self, dest=None):
        if dest and dest != '-':
            self.fp = open(dest, 'a')
        else:
            self.fp = sys.stdout
        self.count = 0

    def write(self, line):
        print(line, file=self.fp)
        self.count += 1

    def close(self):
        if self.fp != sys.stdout:
            self.fp.close()
