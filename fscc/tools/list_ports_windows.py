"""
    Copyright (c) 2019 Commtech, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import ctypes
import struct
from array import array
from ctypes.wintypes import DWORD, WORD, BYTE, ULONG


class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', DWORD),
        ('Data2', WORD),
        ('Data3', WORD),
        ('Data4', BYTE*8),
    ]

    def __init__(self, a, b, c, d):
        self.Data1, self.Data2, self.Data3, self.Data4 = a, b, c, d

    def __str__(self):
        return "{%08x-%04x-%04x-%s-%s}" % (
            self.Data1,
            self.Data2,
            self.Data3,
            ''.join(["%02x" % d for d in self.Data4[:2]]),
            ''.join(["%02x" % d for d in self.Data4[2:]]),
        )


# some details of the windows API differ between 32 and 64 bit systems..
def is_64bit():
    """Returns true when running on a 64 bit system"""
    return ctypes.sizeof(ctypes.c_ulong) != ctypes.sizeof(ctypes.c_void_p)

# ULONG_PTR is a an ordinary number, not a pointer and contrary to the name it
# is either 32 or 64 bits, depending on the type of windows...
# so test if this a 32 bit windows...
if is_64bit():
    # assume 64 bits
    ULONG_PTR = ctypes.c_int64
else:
    # 32 bits
    ULONG_PTR = ctypes.c_ulong


class SP_DEVINFO_DATA(ctypes.Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('ClassGuid', GUID),
        ('DevInst', DWORD),
        ('Reserved', ULONG_PTR),
    ]

    def __str__(self):
        return "ClassGuid:%s DevInst:%s" % (self.ClassGuid, self.DevInst)


NULL = 0
DIGCF_PRESENT = 2
DICS_FLAG_GLOBAL = 1
DIREG_DEV = 0x00000001
KEY_READ = 0x20019

setupapi = ctypes.windll.LoadLibrary("setupapi")
advapi32 = ctypes.windll.LoadLibrary("Advapi32")

SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiEnumDeviceInfo = setupapi.SetupDiEnumDeviceInfo
SetupDiGetClassDevs = setupapi.SetupDiGetClassDevsA
SetupDiOpenDevRegKey = setupapi.SetupDiOpenDevRegKey
RegCloseKey = advapi32.RegCloseKey
RegQueryValueEx = advapi32.RegQueryValueExA


def fsccports():
    fscc_guid = GUID(0x4d36e878, 0xe325, 0x11ce,
                     (0xbf, 0xc1, 0x08, 0x00, 0x2b, 0xe1, 0x13, 0x19))

    g_hdi = SetupDiGetClassDevs(ctypes.byref(fscc_guid),
                                None,
                                NULL,
                                DIGCF_PRESENT)

    devinfo = SP_DEVINFO_DATA()
    devinfo.cbSize = ctypes.sizeof(devinfo)
    index = 0

    while SetupDiEnumDeviceInfo(g_hdi, index, ctypes.byref(devinfo)):
        index += 1

        # get the fscc port number
        hkey = SetupDiOpenDevRegKey(g_hdi,
                                    ctypes.byref(devinfo),
                                    DICS_FLAG_GLOBAL,
                                    0,
                                    DIREG_DEV,  # DIREG_DRV for SW info
                                    KEY_READ)

        port_num_buffer = (BYTE * 4)()
        port_num_length = ULONG(ctypes.sizeof(port_num_buffer))

        RegQueryValueEx(hkey,
                        b'PortNumber',
                        None,
                        None,
                        ctypes.byref(port_num_buffer),
                        ctypes.byref(port_num_length))

        RegCloseKey(hkey)

        bytes = array('B', port_num_buffer)
        port_num = struct.unpack('I', bytes)[0]
        port_name = 'FSCC{}'.format(port_num)

        yield port_num, port_name

    SetupDiDestroyDeviceInfoList(g_hdi)
