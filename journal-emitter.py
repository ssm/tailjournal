#!/usr/bin/env python

import os
import subprocess
import select
import json
import atexit
import sys
import signal

class GracefulExit(Exception):
    pass

def signal_handler(signum, frame):
    if signum in [signal.SIGCHLD]:
        message="End of input from journalctl, exiting..."
    else:
        message="Shutdown requested, exiting..."
    sys.stdout.write("%s\n" % message)
    raise GracefulExit()

JOURNALCTL = '/bin/journalctl'
cursor = None
remove_fields = ('__REALTIME_TIMESTAMP', '__MONOTONIC_TIMESTAMP')

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

def update_cursor(events):
    """For each event, read the last cursor, and update the global cursor
    variable.
    """
    global cursor
    for event in events:
        cursor = event.pop("__CURSOR", None)

def filter_events(events):
    """Remove unwanted fields.
    """
    for event in events:
        for field in remove_fields:
            event.pop(field, None)
        yield event

def emit_events(events):
    for event in events:
        line = json.dumps(event)
        print(line)
        yield event

@atexit.register
def savecursor():
    open("cursor.txt", "w").write("%s\n" % cursor)

def main():
    try:
        events = get_journal_events()
        events = convert_to_json(events)
        events = filter_events(events)
        events = emit_events(events)
        update_cursor(events)
    except GracefulExit:
        pass
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGCHLD, signal_handler)
    main()
