#!/usr/bin/env python

import os
import subprocess
import select
import json
import atexit

JOURNALCTL = '/bin/journalctl'
cursor = None
remove_fields = ('__REALTIME_TIMESTAMP', '__MONOTONIC_TIMESTAMP')

def get_journal_events():
    """Run journalctl, optionally with a cursor file, and yield lines
    """
    journalctl = subprocess.Popen(
        [JOURNALCTL, '-f', '-o', 'json'],
        stdout=subprocess.PIPE)
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
        yield event

def filter_events(events):
    """Remove unwanted fields.
    """
    global remove_fields
    for event in events:
        for field in remove_fields:
            event.pop(field, None)
        yield event

def emit_events(events):
    for event in events:
        line = json.dumps(event)
        print(line)

@atexit.register
def savecursor():
    global cursor
    open("cursor.txt", "w").write("%s" % cursor)

def main():
    events = get_journal_events()
    events = convert_to_json(events)
    events = update_cursor(events)
    events = filter_events(events)
    emit_events(events)

if __name__ == "__main__":
    main()
