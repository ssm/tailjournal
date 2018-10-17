#!/usr/bin/env python

import os
import subprocess
import json
import atexit
import sys
import argparse

# Configuration
JOURNALCTL = '/bin/journalctl'
REMOVE_FIELDS = ('__MONOTONIC_TIMESTAMP', '_SOURCE_MONOTONIC_TIMESTAMP')

# State
cursor = None
statefile = None

def get_journal_events(start_cursor = None):
    """Run journalctl, optionally with a cursor file, and yield lines
    """
    args = [JOURNALCTL, '-f', '-o', 'json']
    if start_cursor is not None:
        args.extend(['--after-cursor', start_cursor])

    try:
        journalctl = subprocess.Popen(args,  stdout=subprocess.PIPE)
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
    if cursor is not None:
        with open (statefile, 'w+') as f:
            f.write("%s\n" % cursor)

def readcursor():
    if os.path.exists(statefile):
        with open(statefile, 'r') as f:
            c = f.readline()
            if len(c) > 0:
                return c
            else:
                return None
    else:
        return None

def handle_arguments():
    parser = argparse.ArgumentParser(description='Tail the systemd journal, with resume state')
    parser.add_argument('statefile', type=str,
                        help="File used for storing the last printed journal event. It is read on start, and this script will resume printing from there.")
    args = parser.parse_args()
    return args

def main():
    args = handle_arguments()
    global statefile
    statefile = args.statefile

    try:
        cursor = readcursor()
        events = get_journal_events(cursor)
        events = convert_to_json(events)
        events = filter_events(events)
        print_events(events)
    except KeyboardInterrupt:
        sys.stderr.write("Shutdown requested, exiting...")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()
