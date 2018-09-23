#!/usr/bin/env python

import os
import subprocess
import json
import atexit
import sys
import signal

# Configuration
JOURNALCTL = '/bin/journalctl'
REMOVE_FIELDS = ('__MONOTONIC_TIMESTAMP', '_SOURCE_MONOTONIC_TIMESTAMP')

# State
cursor = None

class GracefulExit(Exception):
    pass

def signal_handler(signum, frame):
    if signum in [signal.SIGCHLD]:
        message="End of input from journalctl, exiting..."
    else:
        message="Shutdown requested, exiting..."
    sys.stdout.write("%s\n" % message)
    raise GracefulExit()

def get_journal_events():
    """Run journalctl, optionally with a cursor file, and yield lines
    """
    try:
        journalctl = subprocess.Popen(
            [JOURNALCTL, '-f', '-o', 'json'],
            stdout=subprocess.PIPE)
    except OSError as e:
        sys.exit("Failed to execute program '%s': %s" % (JOURNALCTL, str(e)))

    while True:
        line = journalctl.stdout.readline()
        if not line:
            break
        yield line

def convert_to_json(lines):
    """For each line on input, parse it as json, and convert to a hash
    """
    for line in lines:
        event = json.loads(line)
        yield event

def filter_events(events):
    """Remove unwanted fields.
    """
    for event in events:
        for field in REMOVE_FIELDS:
            event.pop(field, None)
        yield event

def print_events(events):
    """Print events to stdout, and store the cursor of the last printed event.
    """
    global cursor
    for event in events:
        _cursor = event.pop("__CURSOR", None)
        line = json.dumps(event)
        print(line)
        cursor = _cursor

@atexit.register
def savecursor():
    open("cursor.txt", "w").write("%s\n" % cursor)

def main():
    try:
        events = get_journal_events()
        events = convert_to_json(events)
        events = filter_events(events)
        print_events(events)
    except GracefulExit:
        pass
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGCHLD, signal_handler)
    main()
