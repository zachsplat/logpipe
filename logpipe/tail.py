"""tail a file, yield new lines as they appear"""

import time
import os

def tail_file(path, poll_interval=0.5):
    with open(path, 'r') as f:
        # seek to end
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                time.sleep(poll_interval)
