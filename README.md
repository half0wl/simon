# Simon

Simple menubar system monitor for macOS, written in Python with pyobjc.

![Simon Screenshot](screenshots/dark.png)

Only tested on macOS Sierra, should work for El Capitan. Supports Python 2.7
and 3.6, versions in between hasn't been tested.

## Installation & Usage

Install with pip:

```bash
$ pip install simon_mac
```

To run Simon:

```bash
$ simon
Simon is now running.
CTRL+C does not work here.
You can quit through the menubar (Simon -> Quit).
```

To run Simon in the background, use `nohup`:

```bash
$ nohup simon &
```

To quit Simon, quit through the menubar (Simon -> Quit).

## Todo / Upcoming

* More stats - battery, temperature, etc.
* Measure impact on system resources
* Preferences/settings: allow user to set update interval, etc.
* ...

## License

MIT
