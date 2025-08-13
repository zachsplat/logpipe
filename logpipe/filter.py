import re

class Filter:
    def __init__(self, expr):
        self.checks = []
        if not expr:
            return
        # simple: key=value,key=value or key~regex
        for part in expr.split(','):
            part = part.strip()
            if '~' in part:
                k, pattern = part.split('~', 1)
                self.checks.append(('regex', k.strip(), re.compile(pattern.strip())))
            elif '=' in part:
                k, v = part.split('=', 1)
                self.checks.append(('eq', k.strip(), v.strip()))
            elif part.startswith('!'):
                self.checks.append(('missing', part[1:].strip(), None))

    def match(self, record):
        if not record:
            return False
        if not self.checks:
            return True
        for kind, key, val in self.checks:
            rv = record.get(key, '')
            if kind == 'eq' and str(rv) != val:
                return False
            elif kind == 'regex' and not val.search(str(rv)):
                return False
            elif kind == 'missing' and key in record:
                return False
        return True
