# MIT License
#
# Copyright (c) 2017 Ray Chen <hcyrnd@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import psutil
from PyObjCTools import AppHelper
from Foundation import NSTimer, NSRunLoop
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, \
    NSEventTrackingRunLoopMode


# https://github.com/giampaolo/psutil/blob/master/scripts/meminfo.py
def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = (' KB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


class Simon(NSApplication):

    def finishLaunching(self):

        # Note: variable names here are camelCased to stay consistent with
        # pyobjc (except menubar items).

        # Create the status & menu bar
        statusBar = NSStatusBar.systemStatusBar()
        self.statusItem = statusBar.statusItemWithLength_(-1)
        self.statusItem.setTitle_('Simon')
        self.menuBar = NSMenu.alloc().init()

        # System
        self.SYSTEM = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'System', 'doNothing:', ''
        )
        self.CPU_USAGE = self._create_empty_menu_item()
        self.RAM_USAGE = self._create_empty_menu_item()
        self.RAM_AVAILABLE = self._create_empty_menu_item()

        self.menuBar.addItem_(self.SYSTEM)
        self.menuBar.addItem_(self.CPU_USAGE)
        self.menuBar.addItem_(self.RAM_USAGE)
        self.menuBar.addItem_(self.RAM_AVAILABLE)

        # Disk I/O
        self.DISKIO = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Disk I/O', 'doNothing:', ''
        )
        self.DATA_READ = self._create_empty_menu_item()
        self.DATA_WRITTEN = self._create_empty_menu_item()

        self.menuBar.addItem_(self.DISKIO)
        self.menuBar.addItem_(self.DATA_READ)
        self.menuBar.addItem_(self.DATA_WRITTEN)

        # Network
        self.NETWORK = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Network', 'doNothing:', ''
        )
        self.NETWORK_RECV = self._create_empty_menu_item()
        self.NETWORK_SENT = self._create_empty_menu_item()

        self.menuBar.addItem_(self.NETWORK)
        self.menuBar.addItem_(self.NETWORK_RECV)
        self.menuBar.addItem_(self.NETWORK_SENT)

        # Quit
        self.QUIT = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Quit', 'terminate:', ''
        )
        self.SEPERATOR = NSMenuItem.separatorItem()
        self.menuBar.addItem_(self.SEPERATOR)
        self.menuBar.addItem_(self.QUIT)

        # Add menu to status bar
        self.statusItem.setMenu_(self.menuBar)

        # Create our timer
        self.timer = \
            NSTimer \
            .scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                1, self, 'update:', '', True
            )

        # Add our timer to the runloop
        NSRunLoop.currentRunLoop().addTimer_forMode_(
            self.timer,
            NSEventTrackingRunLoopMode
        )

        print('Simon is now running.')
        print('CTRL+C does not work here.')
        print('You can quit through the menubar.')

    def update_(self, timer):

        # System
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        avail_mem = bytes2human(psutil.virtual_memory().available)
        self.CPU_USAGE.setTitle_('CPU Usage: {}%'.format(cpu_usage))
        self.RAM_USAGE.setTitle_('RAM Usage: {}%'.format(ram_usage))
        self.RAM_AVAILABLE.setTitle_('Available Memory: {}'.format(avail_mem))

        # Disk I/O
        disk_io = psutil.disk_io_counters()
        disk_data_read = bytes2human(disk_io.read_bytes)
        disk_data_written = bytes2human(disk_io.write_bytes)

        self.DATA_READ.setTitle_('Read: {}'.format(disk_data_read))
        self.DATA_WRITTEN.setTitle_('Written: {}'.format(disk_data_written))

        # Network
        network_io = psutil.net_io_counters()
        network_recv = bytes2human(network_io.bytes_recv)
        network_sent = bytes2human(network_io.bytes_sent)

        self.NETWORK_RECV.setTitle_('Received: {}'.format(network_recv))
        self.NETWORK_SENT.setTitle_('Sent: {}'.format(network_sent))

    def _create_empty_menu_item(self):
        return NSMenuItem \
            .alloc().initWithTitle_action_keyEquivalent_('', '', '')

    def doNothing_(self, sender):
        # hack to enable menuItems by passing them this method as action
        # setEnabled_ isn't working, so this should do for now (achieves
        # the same thing)
        pass


if __name__ == '__main__':
    app = Simon.sharedApplication()
    AppHelper.runEventLoop()
