"""
    Copyright (C) 2013 Commtech, Inc.

    This file is part of pyfscc.

    pyfscc is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyfscc is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pyfscc.  If not, see <http://www.gnu.org/licenses/>.

"""

import struct
import select
import errno
import os

if os.name == 'nt':
    import win32file
    import win32event
else:
    import fcntl


if os.name == 'nt':
    METHOD_BUFFERED = 0
    FILE_ANY_ACCESS = 0

    def CTL_CODE(DeviceType, Function, Method=METHOD_BUFFERED,
                 Access=FILE_ANY_ACCESS):
        return (DeviceType << 16) | (Access << 14) | (Function << 2) | Method

    FSCC_IOCTL_MAGIC = 0x8018

    FSCC_GET_REGISTERS = CTL_CODE(FSCC_IOCTL_MAGIC, 0x800)
    FSCC_SET_REGISTERS = CTL_CODE(FSCC_IOCTL_MAGIC, 0x801)

    FSCC_PURGE_TX = CTL_CODE(FSCC_IOCTL_MAGIC, 0x802)
    FSCC_PURGE_RX = CTL_CODE(FSCC_IOCTL_MAGIC, 0x803)

    FSCC_ENABLE_APPEND_STATUS = CTL_CODE(FSCC_IOCTL_MAGIC, 0x804)
    FSCC_DISABLE_APPEND_STATUS = CTL_CODE(FSCC_IOCTL_MAGIC, 0x805)
    FSCC_GET_APPEND_STATUS = CTL_CODE(FSCC_IOCTL_MAGIC, 0x80D)

    FSCC_SET_MEMORY_CAP = CTL_CODE(FSCC_IOCTL_MAGIC, 0x806)
    FSCC_GET_MEMORY_CAP = CTL_CODE(FSCC_IOCTL_MAGIC, 0x807)

    FSCC_SET_CLOCK_BITS = CTL_CODE(FSCC_IOCTL_MAGIC, 0x808)

    FSCC_ENABLE_IGNORE_TIMEOUT = CTL_CODE(FSCC_IOCTL_MAGIC, 0x80A)
    FSCC_DISABLE_IGNORE_TIMEOUT = CTL_CODE(FSCC_IOCTL_MAGIC, 0x80B)
    FSCC_GET_IGNORE_TIMEOUT = CTL_CODE(FSCC_IOCTL_MAGIC, 0x80F)

    FSCC_SET_TX_MODIFIERS = CTL_CODE(FSCC_IOCTL_MAGIC, 0x80C)
    FSCC_GET_TX_MODIFIERS = CTL_CODE(FSCC_IOCTL_MAGIC, 0x80E)

    FSCC_ENABLE_RX_MULTIPLE = CTL_CODE(FSCC_IOCTL_MAGIC, 0x810)
    FSCC_DISABLE_RX_MULTIPLE = CTL_CODE(FSCC_IOCTL_MAGIC, 0x811)
    FSCC_GET_RX_MULTIPLE = CTL_CODE(FSCC_IOCTL_MAGIC, 0x812)

    FSCC_ENABLE_APPEND_TIMESTAMP = CTL_CODE(FSCC_IOCTL_MAGIC, 0x813)
    FSCC_DISABLE_APPEND_TIMESTAMP = CTL_CODE(FSCC_IOCTL_MAGIC, 0x814)
    FSCC_GET_APPEND_TIMESTAMP = CTL_CODE(FSCC_IOCTL_MAGIC, 0x815)
else:
    IOCPARM_MASK = 0x7f
    IO_NONE = 0x00000000
    IO_WRITE = 0x40000000
    IO_READ = 0x80000000

    def FIX(x):
        return struct.unpack("i", struct.pack("I", x))[0]

    def _IO(x, y):
        return FIX(IO_NONE | (x << 8) | y)

    def _IOR(x, y, t):
        return FIX(IO_READ | ((t & IOCPARM_MASK) << 16) | (x << 8) | y)

    def _IOW(x, y, t):
        return FIX(IO_WRITE | ((t & IOCPARM_MASK) << 16) | (x << 8) | y)

    def _IOWR(x, y, t):
        return FIX(IO_READ | IO_WRITE | ((t & IOCPARM_MASK) << 16) |
               (x << 8) | y)

    FSCC_IOCTL_MAGIC = 0x18

    FSCC_GET_REGISTERS = _IOR(FSCC_IOCTL_MAGIC, 0, struct.calcsize("P"))
    FSCC_SET_REGISTERS = _IOW(FSCC_IOCTL_MAGIC, 1, struct.calcsize("P"))

    FSCC_PURGE_TX = _IO(FSCC_IOCTL_MAGIC, 2)
    FSCC_PURGE_RX = _IO(FSCC_IOCTL_MAGIC, 3)

    FSCC_ENABLE_APPEND_STATUS = _IO(FSCC_IOCTL_MAGIC, 4)
    FSCC_DISABLE_APPEND_STATUS = _IO(FSCC_IOCTL_MAGIC, 5)
    FSCC_GET_APPEND_STATUS = _IOR(FSCC_IOCTL_MAGIC, 13, struct.calcsize("P"))

    FSCC_SET_MEMORY_CAP = _IOW(FSCC_IOCTL_MAGIC, 6, struct.calcsize("P"))
    FSCC_GET_MEMORY_CAP = _IOR(FSCC_IOCTL_MAGIC, 7, struct.calcsize("P"))

    FSCC_ENABLE_IGNORE_TIMEOUT = _IO(FSCC_IOCTL_MAGIC, 10)
    FSCC_DISABLE_IGNORE_TIMEOUT = _IO(FSCC_IOCTL_MAGIC, 11)
    FSCC_GET_IGNORE_TIMEOUT = _IOR(FSCC_IOCTL_MAGIC, 15, struct.calcsize("P"))

    FSCC_SET_TX_MODIFIERS = _IOW(FSCC_IOCTL_MAGIC, 12, struct.calcsize("i"))
    FSCC_GET_TX_MODIFIERS = _IOR(FSCC_IOCTL_MAGIC, 14, struct.calcsize("P"))

    FSCC_ENABLE_RX_MULTIPLE = _IO(FSCC_IOCTL_MAGIC, 16)
    FSCC_DISABLE_RX_MULTIPLE = _IO(FSCC_IOCTL_MAGIC, 17)
    FSCC_GET_RX_MULTIPLE = _IOR(FSCC_IOCTL_MAGIC, 18, struct.calcsize("P"))

    FSCC_ENABLE_APPEND_TIMESTAMP = _IO(FSCC_IOCTL_MAGIC, 19)
    FSCC_DISABLE_APPEND_TIMESTAMP = _IO(FSCC_IOCTL_MAGIC, 20)
    FSCC_GET_APPEND_TIMESTAMP = _IOR(FSCC_IOCTL_MAGIC, 21,
                                     struct.calcsize("P"))

FSCC_UPDATE_VALUE = -2

XF, XREP, TXT, TXEXT = 0, 1, 2, 4

NOT_SUPPORTED_TEXT = 'This feature isn\'t supported on this port.'


class InvalidPortError(Exception):
    """Exception for the situation where a non FSCC port is opened."""
    def __init__(self, file_name):
        self.file_name = file_name

    def __str__(self):
        return "'%s' is not an FSCC port" % self.file_name


class InvalidRegisterError(Exception):
    """Exception for the situation where an invalid register is modified."""
    def __init__(self, register_name):
        self.register_name = register_name

    def __str__(self):
        return "'%s' is an invalid register" % self.register_name


class ReadonlyRegisterError(InvalidRegisterError):
    """Exception for the situation where a read only register is modified."""
    def __str__(self):
        return "'%s' is a readonly register" % self.register_name


class Port(object):
    """Commtech FSCC port."""
    class Registers(object):
        """Registers on the FSCC port."""
        register_names = ["FIFOT", "CMDR", "STAR", "CCR0", "CCR1", "CCR2",
                          "BGR", "SSR", "SMR", "TSR", "TMR", "RAR", "RAMR",
                          "PPR", "TCR", "VSTR", "IMR", "DPLLR", "FCR"]

        readonly_register_names = ["STAR", "VSTR"]
        writeonly_register_names = ["CMDR"]

        editable_register_names = [r for r in register_names if r not in
                                   ["STAR", "VSTR"]]

        def __init__(self, port=None):
            self.port = port
            self._clear_registers()

            for register in self.register_names:
                self._add_register(register)

        def __iter__(self):
            registers = [-1, -1, self._FIFOT, -1, -1, self._CMDR, self._STAR,
                         self._CCR0, self._CCR1, self._CCR2, self._BGR,
                         self._SSR, self._SMR, self._TSR, self._TMR, self._RAR,
                         self._RAMR, self._PPR, self._TCR, self._VSTR, -1,
                         self._IMR, self._DPLLR, self._FCR]

            for register in registers:
                yield register

        def _add_register(self, register):
            """Dynamically add a way to edit a register to the port."""
            if register not in self.writeonly_register_names:
                fget = lambda self: self._get_register(register)
            else:
                fget = None

            if register not in self.readonly_register_names:
                fset = lambda self, value: self._set_register(register, value)
            else:
                fset = None

            setattr(self.__class__, register, property(fget, fset, None, ""))

        def _get_register(self, register):
            """Gets the value of a register."""
            if self.port:
                self._clear_registers()
                setattr(self, "_%s" % register, FSCC_UPDATE_VALUE)
                self._get_registers()

            return getattr(self, "_%s" % register)

        def _set_register(self, register, value):
            """Sets the value of a register."""
            if self.port:
                self._clear_registers()

            setattr(self, "_%s" % register, value)

            if self.port:
                self._set_registers()

        def _clear_registers(self):
            """Clears the stored register values."""
            for register in self.register_names:
                setattr(self, "_%s" % register, -1)

        def _get_registers(self):
            """Gets all of the register values."""
            if not self.port:
                return

            registers = list(self)

            fmt = "q" * len(registers)
            regs = self.port._ioctl_get_struct(FSCC_GET_REGISTERS, fmt,
                                               registers)

            for i, register in enumerate(registers):
                if register != -1:
                    self._set_register_by_index(i, regs[i])

        def _set_registers(self):
            """Sets all of the register values."""
            if not self.port:
                return

            registers = list(self)

            fmt = "q" * len(registers)
            value = struct.pack(fmt, *registers)
            self.port._ioctl_set_struct(FSCC_SET_REGISTERS, fmt, value)

        def _set_register_by_index(self, index, value):
            """Sets the value of a register by it's index."""
            data = [("FIFOT", 2), ("CMDR", 5), ("STAR", 6), ("CCR0", 7),
                    ("CCR1", 8), ("CCR2", 9), ("BGR", 10), ("SSR", 11),
                    ("SMR", 12), ("TSR", 13), ("TMR", 14), ("RAR", 15),
                    ("RAMR", 16), ("PPR", 17), ("TCR", 18), ("VSTR", 19),
                    ("IMR", 21), ("DPLLR", 22), ("FCR", 23)]

            for r, i in data:
                if i == index:
                    setattr(self, "_%s" % r, value)

        # Note: clears registers
        def import_from_file(self, import_file):
            """Reads and stores the register values from a file."""
            import_file.seek(0, os.SEEK_SET)

            for line in import_file:
                try:
                    line = str(line, encoding='utf8')
                except:
                    pass

                if line[0] != "#":
                    d = line.split("=")
                    reg_name, reg_val = d[0].strip().upper(), d[1].strip()

                    if reg_name not in self.register_names:
                        raise InvalidRegisterError(reg_name)

                    if reg_name not in self.editable_register_names:
                        raise ReadonlyRegisterError(reg_name)

                    if reg_val[0] == "0" and reg_val[1] in ["x", "X"]:
                        reg_val = int(reg_val, 16)
                    else:
                        reg_val = int(reg_val)

                    setattr(self, reg_name, reg_val)

        def export_to_file(self, export_file):
            """Writes the current register values to a file."""
            for register_name in self.editable_register_names:
                if register_name in self.writeonly_register_names:
                    continue

                value = getattr(self, register_name)

                if value >= 0:
                    export_file.write("%s = 0x%08x\n" % (register_name, value))

    def __init__(self, port_num, append_status=True, append_timestamp=True):

        if os.name == 'nt':
            file_name = '\\\\.\\fscc' + str(port_num)

            self.hComPort = win32file.CreateFile(
                file_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,  # exclusive access
                None,  # no security
                win32file.OPEN_EXISTING,
                win32file.FILE_ATTRIBUTE_NORMAL |
                win32file.FILE_FLAG_OVERLAPPED,
                0)
        else:
            file_name = '/dev/fscc' + str(port_num)

            self.fd = os.open(file_name, os.O_RDWR)

        self.registers = Port.Registers(self)

        try:
            self.append_status = append_status
        except IOError:
            raise InvalidPortError(file_name)

        self.append_timestamp = append_timestamp

    def _ioctl_action(self, ioctl_name):
        if os.name == 'nt':
            try:
                win32file.DeviceIoControl(self.hComPort, ioctl_name, None, 0,
                                          None)
            except win32file.error as e:
                if e.winerror == 50:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                else:
                    raise
        else:
            try:
                fcntl.ioctl(self.fd, ioctl_name)
            except IOError as e:
                if e.errno == errno.EPROTONOSUPPORT:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                else:
                    raise

    def _ioctl_set_boolean(self, ioctl_enable, ioctl_disable, value):
        ioctl_name = ioctl_enable if value else ioctl_disable
        self._ioctl_action(ioctl_name)

    def _ioctl_get_boolean(self, ioctl_name):
        if os.name == 'nt':
            buf_size = struct.calcsize('?')
            try:
                buf = win32file.DeviceIoControl(self.hComPort, ioctl_name,
                                                None, buf_size, None)
            except win32file.error as e:
                if e.winerror == 50:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                else:
                    raise
        else:
            try:
                buf = fcntl.ioctl(self.fd, ioctl_name, struct.pack('?', 0))
            except IOError as e:
                if e.errno == errno.EPROTONOSUPPORT:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                else:
                    raise

        value = struct.unpack('?', buf)

        return True if value[0] else False

    def _ioctl_set_integer(self, ioctl_name, value, fmt='i'):
        if os.name == 'nt':
            try:
                value = struct.pack(fmt, value)
                win32file.DeviceIoControl(self.hComPort, ioctl_name, value, 0,
                                          None)
            except win32file.error as e:
                if e.winerror == 50:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                elif e.winerror == 87:
                    raise ValueError('The argument is out of range.')
                else:
                    raise
        else:
            try:
                fcntl.ioctl(self.fd, ioctl_name, value)
            except IOError as e:
                if e.errno == errno.EPROTONOSUPPORT:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                elif e.errno == errno.EINVAL:
                    raise ValueError('The argument is out of range.')
                else:
                    raise

    def _ioctl_set_uinteger(self, ioctl_name, value):
        self._ioctl_set_integer(ioctl_name, value, 'I')

    def _ioctl_get_integer(self, ioctl_name, fmt='i'):
        if os.name == 'nt':
            buf_size = struct.calcsize(fmt)
            try:
                buf = win32file.DeviceIoControl(self.hComPort, ioctl_name,
                                                None, buf_size, None)
            except win32file.error as e:
                if e.winerror == 50:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                else:
                    raise
        else:
            try:
                buf = fcntl.ioctl(self.fd, ioctl_name, struct.pack(fmt, 0))
            except IOError as e:
                if e.errno == errno.EPROTONOSUPPORT:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                else:
                    raise

        value = struct.unpack(fmt, buf)
        return value[0]

    def _ioctl_get_uinteger(self, ioctl_name):
        return self._ioctl_get_integer(ioctl_name, 'I')

    def _ioctl_set_struct(self, ioctl_name, fmt, value):
        if os.name == 'nt':
            buf_size = struct.calcsize(fmt)
            try:
                win32file.DeviceIoControl(self.hComPort, ioctl_name, value,
                                          buf_size, None)
            except win32file.error as e:
                if e.winerror == 50:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                elif e.winerror == 87:
                    raise ValueError('The argument is out of range.')
                else:
                    raise
        else:
            try:
                fcntl.ioctl(self.fd, ioctl_name, value)
            except IOError as e:
                if e.errno == errno.EPROTONOSUPPORT:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                elif e.errno == errno.EINVAL:
                    raise ValueError('The argument is out of range.')
                else:
                    raise

    def _ioctl_get_struct(self, ioctl_name, fmt, initial):
        if os.name == 'nt':
            buf_size = struct.calcsize(fmt)
            try:
                buf = win32file.DeviceIoControl(self.hComPort, ioctl_name,
                                                struct.pack(fmt, *initial),
                                                buf_size, None)
            except win32file.error as e:
                if e.winerror == 50:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                else:
                    raise
        else:
            try:
                buf = fcntl.ioctl(self.fd, ioctl_name,
                                  struct.pack(fmt, *initial))
            except IOError as e:
                if e.errno == errno.EPROTONOSUPPORT:
                    raise AttributeError(NOT_SUPPORTED_TEXT)
                else:
                    raise

        value = struct.unpack(fmt, buf)

        return value

    def purge(self, tx=True, rx=True):
        """Removes unsent and/or unread data from the card."""
        if (tx):
            self._ioctl_action(FSCC_PURGE_TX)

        if (rx):
            self._ioctl_action(FSCC_PURGE_RX)

    def _set_append_status(self, append_status):
        """Sets the value of the append status setting."""
        self._ioctl_set_boolean(FSCC_ENABLE_APPEND_STATUS,
                                FSCC_DISABLE_APPEND_STATUS,
                                append_status)

    def _get_append_status(self):
        """Gets the value of the append status setting."""
        return self._ioctl_get_boolean(FSCC_GET_APPEND_STATUS)

    append_status = property(fset=_set_append_status, fget=_get_append_status)

    def _set_append_timestamp(self, append_timestamp):
        """Sets the value of the append timestamp setting."""
        self._ioctl_set_boolean(FSCC_ENABLE_APPEND_TIMESTAMP,
                                FSCC_DISABLE_APPEND_TIMESTAMP,
                                append_timestamp)

    def _get_append_timestamp(self):
        """Gets the value of the append timestamp setting."""
        return self._ioctl_get_boolean(FSCC_GET_APPEND_TIMESTAMP)

    append_timestamp = property(fset=_set_append_timestamp,
                                fget=_get_append_timestamp)

    def _set_memcap(self, input_memcap, output_memcap):
        """Sets the value of the memory cap setting."""
        fmt = 'i' * 2
        value = struct.pack(fmt, input_memcap, output_memcap)
        self._ioctl_set_struct(FSCC_SET_MEMORY_CAP, fmt, value)

    def _get_memcap(self):
        """Gets the value of the memory cap setting."""
        fmt = 'i' * 2
        return self._ioctl_get_struct(FSCC_GET_MEMORY_CAP, fmt, (-1, -1))

    def _set_imemcap(self, memcap):
        """Sets the value of the input memory cap setting."""
        self._set_memcap(memcap, -1)

    def _get_imemcap(self):
        """Gets the value of the output memory cap setting."""
        return self._get_memcap()[0]

    input_memory_cap = property(fset=_set_imemcap, fget=_get_imemcap)

    def _set_omemcap(self, memcap):
        """Sets the value of the output memory cap setting."""
        self._set_memcap(-1, memcap)

    def _get_omemcap(self):
        """Gets the value of the output memory cap setting."""
        return self._get_memcap()[1]

    output_memory_cap = property(fset=_set_omemcap, fget=_get_omemcap)

    def _set_ignore_timeout(self, ignore_timeout):
        """Sets the value of the ignore timeout setting."""
        self._ioctl_set_boolean(FSCC_ENABLE_IGNORE_TIMEOUT,
                                FSCC_DISABLE_IGNORE_TIMEOUT,
                                ignore_timeout)

    def _get_ignore_timeout(self):
        """Gets the value of the ignore timeout setting."""
        return self._ioctl_get_boolean(FSCC_GET_IGNORE_TIMEOUT)

    ignore_timeout = property(fset=_set_ignore_timeout,
                              fget=_get_ignore_timeout)

    def _set_tx_modifiers(self, tx_modifiers):
        """Sets the value of the transmit modifiers setting."""
        self._ioctl_set_uinteger(FSCC_SET_TX_MODIFIERS, tx_modifiers)

    def _get_tx_modifiers(self):
        """Gets the value of the transmit modifiers setting."""
        return self._ioctl_get_uinteger(FSCC_GET_TX_MODIFIERS)

    tx_modifiers = property(fset=_set_tx_modifiers, fget=_get_tx_modifiers)

    def _set_rx_multiple(self, rx_multiple):
        """Sets the value of the ignore timeout setting."""
        self._ioctl_set_boolean(FSCC_ENABLE_RX_MULTIPLE,
                                FSCC_DISABLE_RX_MULTIPLE,
                                rx_multiple)

    def _get_rx_multiple(self):
        """Gets the value of the ignore timeout setting."""
        return self._ioctl_get_boolean(FSCC_GET_RX_MULTIPLE)

    rx_multiple = property(fset=_set_rx_multiple, fget=_get_rx_multiple)

    def read(self, timeout=1000):
        """Reads data from the card."""
        _append_status = self.append_status
        _append_timestamp = self.append_timestamp

        if os.name == 'nt':
            ol = win32file.OVERLAPPED()
            ol.hEvent = win32event.CreateEvent(None, 0, 0, None)
            buffer = win32file.AllocateReadBuffer(0xFFFF)
            win32file.ReadFile(self.hComPort, buffer, ol)
            r = win32event.WaitForSingleObject(ol.hEvent, timeout)

            if r == win32event.WAIT_TIMEOUT:
                win32file.CancelIo(self.hComPort)

            if r == win32event.WAIT_TIMEOUT or \
               r == win32event.WAIT_ABANDONED or \
               r == win32event.WAIT_FAILED:
                win32file.CloseHandle(ol.hEvent)
                return (None, None, None)

            num_bytes = win32file.GetOverlappedResult(self.hComPort, ol, True)
            data = bytes(buffer[0:num_bytes])
            win32file.CloseHandle(ol.hEvent)
        else:
            data = os.read(self.fd, 4096)

        status, timestamp = None, None

        if os.name == 'nt':
            if (_append_status and _append_timestamp):
                status = data[-10:-8]
                timestamp = struct.unpack('q', data[-8:])[0]
                data = data[:-10]
            elif (_append_status):
                status = data[-2:]
                data = data[:-2]
            elif (_append_timestamp):
                timestamp = struct.unpack('q', data[-8:])[0]
                data = data[:-8]

            if timestamp:
                timestamp = timestamp / 10000000 - 11644473600
        else:
            if (_append_status and _append_timestamp):
                status = data[-18:-16]
                timestamp = struct.unpack('ll', data[-16:])
                data = data[:-18]
            elif (_append_status):
                status = data[-2:]
                data = data[:-2]
            elif (_append_timestamp):
                timestamp = struct.unpack('ll', data[-16:])
                data = data[:-16]

            if timestamp:
                timestamp = timestamp[0] + (float(timestamp[1]) / 1000000)

        return (data, status, timestamp)

    def write(self, data):
        if os.name == 'nt':
            ol = win32file.OVERLAPPED()
            ol.hEvent = win32event.CreateEvent(None, 0, 0, None)
            win32file.WriteFile(self.hComPort, data, ol)
            win32file.GetOverlappedResult(self.hComPort, ol, True)
            win32file.CloseHandle(ol.hEvent)
        else:
            os.write(self.fd, data)

    def close(self):
        if os.name == 'nt':
            win32file.CloseHandle(self.hComPort)
        else:
            os.close(self.fd)

    def can_read(self, timeout=100):
        """Checks whether there is data available to read."""
        poll_obj = select.poll()
        poll_obj.register(self, select.POLLIN)

        poll_data = poll_obj.poll(timeout)

        poll_obj.unregister(self)

        if poll_data and (poll_data[0][1] | select.POLLIN):
            return True
        else:
            return False

    def can_write(self, timeout=100):
        """Checks whether there is room available to write additional data."""
        poll_obj = select.poll()
        poll_obj.register(self, select.POLLOUT)

        poll_data = poll_obj.poll(timeout)

        poll_obj.unregister(self)

        if poll_data and (poll_data[0][1] | select.POLLOUT):
            return True
        else:
            return False

if __name__ == '__main__':
    p = Port(0)

    print("Append Status", p.append_status)
    print("Append Timestamp", p.append_timestamp)
    print("Input Memory Cap", p.input_memory_cap)
    print("Output Memory Cap", p.output_memory_cap)
    print("Ignore Timeout", p.ignore_timeout)
    print("Transmit Modifiers", p.tx_modifiers)
    print("RX Multiple", p.rx_multiple)

    print("CCR0", hex(p.registers.CCR0))
    print("CCR1", hex(p.registers.CCR1))
    print("CCR2", hex(p.registers.CCR2))
    print("BGR", hex(p.registers.BGR))

    p.append_status = True
    p.append_timestamp = True
    p.input_memory_cap = 1000000
    p.output_memory_cap = 1000000
    p.ignore_timeout = False
    p.tx_modifiers = 0
    p.rx_modifiers = False

    p.purge()

    p.write(b'U')
    print(p.read())

    p.close()
