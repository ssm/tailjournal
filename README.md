tailjournal
===========

Tail the systemd journal, emitting output as json lines.

This script is run with a file name as argument. At exit, the script
will store the cursor of the last printed line to that file.

Stopping the script and starting again will resume at that point.

Installation
------------

The `src/tailjournal/tailjournal.py` file is all you need, the other
files are mostly for development and testing. Download the file,
inspect it for your peace of mind, install it where your log
collectors can run it. If in doubt, install it as
`/usr/local/bin/tailjournal`, and make it executable.

Usage
-----

```console
$ tailjournal -h
usage: tailjournal [-h] statefile

Tail the systemd journal, printing json lines.  On exit, store a reference to
the last line printed, and resume from there on the next invocation.

positional arguments:
  statefile   File used for storing a reference to the last printed journal event.

optional arguments:
  -h, --help  show this help message and exit

```

Example session
---------------

```console
$ tailjournal /var/tmp/journal.state
{"SYSLOG_IDENTIFIER": "dbus-daemon", "_CAP_EFFECTIVE": "0", "_PID": "1234", ...}
{"blablabla": "more blabla"}
```
