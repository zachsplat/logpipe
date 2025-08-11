# logpipe

reads logs from stdin or files, filters/transforms them, outputs to
stdout or a file. like a mini version of vector/fluentd for when you
just need something simple.

## install

```
pip install -e .
```

## usage

```bash
# tail a log file, filter for errors
tail -f /var/log/syslog | logpipe --filter 'level=error'

# parse json logs, extract fields
logpipe --input app.log --format json --fields timestamp,message,level

# aggregate counts
logpipe --input access.log --count-by status_code
```
