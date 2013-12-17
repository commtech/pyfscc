import glob
import os


def fsccports():
    devices = glob.glob('/dev/fscc*')
    return ((d, os.path.basename(d), 'n/a') for d in devices)
