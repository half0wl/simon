import psutil
import math


def bytes2human(n):
    # Credits to /u/cyberspacecowboy on reddit
    # https://www.reddit.com/r/Python/comments/5xukpd/-/dem5k12/
    symbols = (' B', ' KiB', ' MiB', ' GiB', ' TiB', ' PiB', ' EiB', ' ZiB',
               ' YiB')
    i = math.floor(math.log(abs(n)+1, 2) / 10)
    return '%.1f%s' % (n/2**(i*10), symbols[int(i)])


def cpu_usage():
    return psutil.cpu_percent()


def ram_usage():
    return psutil.virtual_memory().percent


def available_memory():
    return bytes2human(psutil.virtual_memory().available)


def disk_read():
    return bytes2human(psutil.disk_io_counters().read_bytes)


def disk_written():
    return bytes2human(psutil.disk_io_counters().write_bytes)


def network_recv():
    return bytes2human(psutil.net_io_counters().bytes_recv)


def network_sent():
    return bytes2human(psutil.net_io_counters().bytes_sent)
