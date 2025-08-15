from collections import Counter, defaultdict

class Aggregator:
    def __init__(self, group_by=None):
        self.group_by = group_by
        self.counts = Counter()
        self.total = 0

    def add(self, record):
        self.total += 1
        if self.group_by and record:
            key = record.get(self.group_by, '<missing>')
            self.counts[key] += 1

    def results(self):
        if not self.group_by:
            return f'total: {self.total}'
        lines = [f'total: {self.total}']
        for key, count in self.counts.most_common():
            pct = (count / self.total * 100) if self.total else 0
            lines.append(f'  {key}: {count} ({pct:.1f}%)')
        return '\n'.join(lines)
