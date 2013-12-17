import glob
import re


def fsccports():
    device_paths = glob.glob('/dev/fscc*')

    for path in device_paths:
        port_num = re.search('(\d+)$', path).group(0)
        yield port_num, path
