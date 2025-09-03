import argparse
import sys
from .parser import parse_auto
from .filter import Filter
from .output import format_record, Output
from .aggregate import Aggregator

def main():
    ap = argparse.ArgumentParser(description='log filtering tool')
    ap.add_argument('--input', '-i', help='input file (default stdin)')
    ap.add_argument('--output', '-o', help='output file (default stdout)')
    ap.add_argument('--filter', '-f', help='filter expr: key=val,key~regex')
    ap.add_argument('--fields', help='comma-separated fields to output')
    ap.add_argument('--format', default='text', choices=['text', 'json', 'csv'])
    ap.add_argument('--count-by', help='aggregate counts by field')
    ap.add_argument('--tail', action='store_true', help='follow input (like tail -f)')
    args = ap.parse_args()

    filt = Filter(args.filter)
    fields = args.fields.split(',') if args.fields else None
    out = Output(args.output)
    agg = Aggregator(args.count_by) if args.count_by else None

    if args.input:
        fp = open(args.input)
    else:
        fp = sys.stdin

    try:
        for line in fp:
            record = parse_auto(line)
            if not filt.match(record):
                continue
            if agg:
                agg.add(record)
            else:
                formatted = format_record(record, fields, args.format)
                if formatted:
                    out.write(formatted)
    except KeyboardInterrupt:
        pass
    finally:
        if agg:
            print(agg.results())
        out.close()
        if fp != sys.stdin:
            fp.close()

if __name__ == '__main__':
    main()

# TODO: add --rate flag to show events/sec
# TODO: add --sample N to only process every Nth line
