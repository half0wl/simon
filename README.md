# Simon

Simple macOS menubar system monitor, written in Python.

![Simon Screenshot](screenshots/dark.png)

Only tested on **macOS Sierra 10.12.3** and **Python 3.6**.

## Installation & Usage

Simon depends on `pyobjc` and `psutil`.

```bash
$ git clone https://github.com/hcyrnd/simon.git
$ cd simon
$ virtualenv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
$ python simon.py
Simon is now running.
CTRL+C does not work here.
You can quit through the menubar (Simon -> Quit).
```

To run Simon in the background, use `nohup`:

```bash
$ nohup python simon.py &
```

To quit Simon, quit through the menubar.

## Todo / Upcoming

* Standalone .app
* More stats - battery, temperature, etc.
* Measure impact on system resources
* Preferences/settings: allow user to set update interval, etc.
* ...

## License

MIT
