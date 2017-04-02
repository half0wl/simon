from Foundation import NSTimer, NSRunLoop
from AppKit import NSApplication, NSStatusBar, NSMenu, NSMenuItem, \
    NSEventTrackingRunLoopMode

from .stats import cpu_usage, ram_usage, available_memory, disk_read, \
    disk_written, network_recv, network_sent


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
        self.CPU_USAGE.setTitle_('CPU Usage: {}%'.format(cpu_usage()))
        self.RAM_USAGE.setTitle_('RAM Usage: {}%'.format(ram_usage()))
        self.RAM_AVAILABLE.setTitle_('Available Memory: {}'.format(
            available_memory())
        )

        # Disk I/O
        self.DATA_READ.setTitle_('Read: {}'.format(disk_read()))
        self.DATA_WRITTEN.setTitle_('Written: {}'.format(disk_written()))

        # Network
        self.NETWORK_RECV.setTitle_('Received: {}'.format(network_recv()))
        self.NETWORK_SENT.setTitle_('Sent: {}'.format(network_sent()))

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
