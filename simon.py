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

import math
import psutil
from PyObjCTools import AppHelper
from Foundation import NSTimer, NSRunLoop
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, \
    NSEventTrackingRunLoopMode


def bytes2human(n):
    # Credits to /u/cyberspacecowboy on reddit
    # https://www.reddit.com/r/Python/comments/5xukpd/-/dem5k12/
    symbols = (' B', ' KiB', ' MiB', ' GiB', ' TiB', ' PiB', ' EiB', ' ZiB',
               ' YiB')
    i = math.floor(math.log(abs(n)+1, 2) / 10)
    return '%.1f%s' % (n/2**(i*10), symbols[i])


class Simon(NSApplication):

    def finishLaunching(self):
        self._setup_menuBar()

        # Create a timer which fires the update_ method every 1second,
        # and add it to the runloop
        NSRunLoop.currentRunLoop().addTimer_forMode_(
            NSTimer
            .scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                1, self, 'update:', '', True
            ),
            NSEventTrackingRunLoopMode
        )

        print('Simon is now running.')
        print('CTRL+C does not work here.')
        print('You can quit through the menubar (Simon -> Quit).')

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

    def _setup_menuBar(self):
        statusBar = NSStatusBar.systemStatusBar()
        self.statusItem = statusBar.statusItemWithLength_(-1)
        self.menuBar = NSMenu.alloc().init()

        self.statusItem.setTitle_('Simon')

        # Labels/buttons
        self.SYSTEM = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'System', 'doNothing:', ''
        )
        self.DISKIO = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Disk I/O', 'doNothing:', ''
        )
        self.NETWORK = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Network', 'doNothing:', ''
        )
        self.QUIT = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            'Quit', 'terminate:', ''
        )

        # System
        self.CPU_USAGE = self._create_empty_menu_item()
        self.RAM_USAGE = self._create_empty_menu_item()
        self.RAM_AVAILABLE = self._create_empty_menu_item()

        # Disk I/O
        self.DATA_READ = self._create_empty_menu_item()
        self.DATA_WRITTEN = self._create_empty_menu_item()

        # Network
        self.NETWORK_RECV = self._create_empty_menu_item()
        self.NETWORK_SENT = self._create_empty_menu_item()

        '''
        Add our items to the menuBar - yields the following output:

        Simon
            System
                CPU Usage
                RAM Usage
                Available Memory
            Disk I/O
                Read
                Written
            Network
                Received
                Sent
            -----------------------
            Quit
        '''
        self.menuBar.addItem_(self.SYSTEM)  # system label
        self.menuBar.addItem_(self.CPU_USAGE)
        self.menuBar.addItem_(self.RAM_USAGE)
        self.menuBar.addItem_(self.RAM_AVAILABLE)

        self.menuBar.addItem_(self.DISKIO)  # disk I/O label
        self.menuBar.addItem_(self.DATA_READ)
        self.menuBar.addItem_(self.DATA_WRITTEN)

        self.menuBar.addItem_(self.NETWORK)  # network label
        self.menuBar.addItem_(self.NETWORK_RECV)
        self.menuBar.addItem_(self.NETWORK_SENT)

        self.menuBar.addItem_(NSMenuItem.separatorItem())  # seperator
        self.menuBar.addItem_(self.QUIT)  # quit button

        # Add menu to status bar
        self.statusItem.setMenu_(self.menuBar)

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
