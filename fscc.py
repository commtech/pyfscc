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
import os
import ctypes
import sys

try:
    if os.name == 'nt':
        lib = ctypes.cdll.LoadLibrary('cfscc.dll')
    else:
        lib = ctypes.cdll.LoadLibrary('./libcfscc.so')
except:
    if os.name == 'nt':
        lib = ctypes.cdll.LoadLibrary(os.path.join(sys.prefix,
                                                   'DLLs\cfscc.dll'))
    else:
        lib = ctypes.cdll.LoadLibrary(os.path.join(sys.prefix,
                                                   'local/DLLs/libcfscc.so'))


FSCC_UPDATE_VALUE = -2

XF, XREP, TXT, TXEXT = 0, 1, 2, 4
FSCC_TIMEOUT, FSCC_INCORRECT_MODE, \
    FSCC_BUFFER_TOO_SMALL, FSCC_PORT_NOT_FOUND = 16000, 16001, 16002, 16003

NOT_SUPPORTED_TEXT = 'This feature isn\'t supported on this port.'


class PortNotFoundError(Exception):
    def __init__(self, port_num):
        self.port_num = port_num

    def __str__(self):
        return 'Port not found'


class TimeoutError(Exception):
    def __str__(self):
        return 'Port timed out'


class BufferTooSmallError(Exception):
    def __str__(self):
        return 'Buffer too small'


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
        register_names = ['FIFOT', 'CMDR', 'STAR', 'CCR0', 'CCR1', 'CCR2',
                          'BGR', 'SSR', 'SMR', 'TSR', 'TMR', 'RAR', 'RAMR',
                          'PPR', 'TCR', 'VSTR', 'IMR', 'DPLLR', 'FCR']

        readonly_register_names = ['STAR', 'VSTR']
        writeonly_register_names = ['CMDR']

        editable_register_names = [r for r in register_names if r not in
                                   ['STAR', 'VSTR']]

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
                setattr(self, '_%s' % register, FSCC_UPDATE_VALUE)
                self._get_registers()

            return getattr(self, '_%s' % register)

        def _set_register(self, register, value):
            """Sets the value of a register."""
            if self.port:
                self._clear_registers()

            setattr(self, '_%s' % register, value)

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

            fmt = 'q' * len(registers)
            regs = self.port._ctypes_get_struct(lib.fscc_get_registers, fmt,
                                                registers)

            for i, register in enumerate(registers):
                if register != -1:
                    self._set_register_by_index(i, regs[i])

        def _set_registers(self):
            """Sets all of the register values."""
            if not self.port:
                return

            registers = list(self)

            fmt = 'q' * len(registers)
            buf = struct.pack(fmt, *registers)
            e = lib.fscc_set_registers(self.port._handle, buf)

            if e == 0:
                pass
            elif e == FSCC_TIMEOUT:
                raise TimeoutError()
            else:
                raise Exception(e)

        def _set_register_by_index(self, index, value):
            """Sets the value of a register by it's index."""
            data = [('FIFOT', 2), ('CMDR', 5), ('STAR', 6), ('CCR0', 7),
                    ('CCR1', 8), ('CCR2', 9), ('BGR', 10), ('SSR', 11),
                    ('SMR', 12), ('TSR', 13), ('TMR', 14), ('RAR', 15),
                    ('RAMR', 16), ('PPR', 17), ('TCR', 18), ('VSTR', 19),
                    ('IMR', 21), ('DPLLR', 22), ('FCR', 23)]

            for r, i in data:
                if i == index:
                    setattr(self, '_%s' % r, value)

        # Note: clears registers
        def import_from_file(self, import_file):
            """Reads and stores the register values from a file."""
            import_file.seek(0, os.SEEK_SET)

            for line in import_file:
                try:
                    line = str(line, encoding='utf8')
                except:
                    pass

                if line[0] != '#':
                    d = line.split('=')
                    reg_name, reg_val = d[0].strip().upper(), d[1].strip()

                    if reg_name not in self.register_names:
                        raise InvalidRegisterError(reg_name)

                    if reg_name not in self.editable_register_names:
                        raise ReadonlyRegisterError(reg_name)

                    if reg_val[0] == '0' and reg_val[1] in ['x', 'X']:
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
                    export_file.write('%s = 0x%08x\n' % (register_name, value))

    class MemoryCap(object):

        def __init__(self, port=None):
            self.port = port

        def _set_memcap(self, input_memcap, output_memcap):
            """Sets the value of the memory cap setting."""
            fmt = 'i' * 2
            buf = struct.pack(fmt, input_memcap, output_memcap)
            lib.fscc_set_memory_cap(self.port._handle, buf)

        def _get_memcap(self):
            """Gets the value of the memory cap setting."""
            return self.port._ctypes_get_struct(lib.fscc_get_memory_cap,
                                                'i' * 2, (-1, -1))

        def _set_imemcap(self, memcap):
            """Sets the value of the input memory cap setting."""
            self._set_memcap(memcap, -1)

        def _get_imemcap(self):
            """Gets the value of the output memory cap setting."""
            return self._get_memcap()[0]

        input = property(fset=_set_imemcap, fget=_get_imemcap)

        def _set_omemcap(self, memcap):
            """Sets the value of the output memory cap setting."""
            self._set_memcap(-1, memcap)

        def _get_omemcap(self):
            """Gets the value of the output memory cap setting."""
            return self._get_memcap()[1]

        output = property(fset=_set_omemcap, fget=_get_omemcap)

    def __init__(self, port_num, append_status=True, append_timestamp=True):
        self._handle = ctypes.c_void_p()

        e = lib.fscc_connect(port_num, ctypes.byref(self._handle))

        if e == 0:
            pass
        elif e == FSCC_PORT_NOT_FOUND:
            raise PortNotFoundError()
        else:
            raise Exception(e)

        self._handle = self._handle.value

        self.registers = Port.Registers(self)
        self.memory_cap = Port.MemoryCap(self)

        self.append_status = append_status
        self.append_timestamp = append_timestamp

    def purge(self, tx=True, rx=True):
        """Removes unsent and/or unread data from the card."""
        e = lib.fscc_purge(self._handle, tx, rx)

        if e == 0:
            pass
        elif e == FSCC_TIMEOUT:
            raise TimeoutError()
        else:
            raise Exception(e)

    def _set_append_status(self, status):
        """Sets the value of the append status setting."""
        return self._ctypes_set_bool(lib.fscc_enable_append_status,
                                     lib.fscc_disable_append_status,
                                     status)

    def _get_append_status(self):
        """Gets the value of the append status setting."""
        return self._ctypes_get_bool(lib.fscc_get_append_status)

    append_status = property(fset=_set_append_status, fget=_get_append_status)

    def _set_append_timestamp(self, status):
        """Sets the value of the append timestamp setting."""
        return self._ctypes_set_bool(lib.fscc_enable_append_timestamp,
                                     lib.fscc_disable_append_timestamp,
                                     status)

    def _get_append_timestamp(self):
        """Gets the value of the append timestamp setting."""
        return self._ctypes_get_bool(lib.fscc_get_append_timestamp)

    append_timestamp = property(fset=_set_append_timestamp,
                                fget=_get_append_timestamp)

    def _set_ignore_timeout(self, status):
        """Sets the value of the ignore timeout setting."""
        return self._ctypes_set_bool(lib.fscc_enable_ignore_timeout,
                                     lib.fscc_disable_ignore_timeout,
                                     status)

    def _get_ignore_timeout(self):
        """Gets the value of the ignore timeout setting."""
        return self._ctypes_get_bool(lib.fscc_get_ignore_timeout)

    ignore_timeout = property(fset=_set_ignore_timeout,
                              fget=_get_ignore_timeout)

    def _set_tx_modifiers(self, value):
        """Sets the value of the transmit modifiers setting."""
        lib.fscc_set_tx_modifiers(self._handle, value)

    def _get_tx_modifiers(self):
        """Gets the value of the transmit modifiers setting."""
        return self._ctypes_get_uint(lib.fscc_get_tx_modifiers)

    tx_modifiers = property(fset=_set_tx_modifiers, fget=_get_tx_modifiers)

    def _set_rx_multiple(self, status):
        """Sets the value of the rx multiple setting."""
        return self._ctypes_set_bool(lib.fscc_enable_rx_multiple,
                                     lib.fscc_disable_rx_multiple,
                                     status)

    def _get_rx_multiple(self):
        """Gets the value of the ignore timeout setting."""
        return self._ctypes_get_bool(lib.fscc_get_rx_multiple)

    rx_multiple = property(fset=_set_rx_multiple, fget=_get_rx_multiple)

    def _set_clock_frequency(self, frequency):
        """Sets the value of the clock frequency setting."""
        lib.fscc_set_clock_frequency(self._handle, frequency)

    clock_frequency = property(fset=_set_clock_frequency)

    def _ctypes_set_bool(self, enable_func, disable_func, status):
        if status:
            enable_func(self._handle)
        else:
            disable_func(self._handle)

    def _ctypes_get_bool(self, func):
        return True if self._ctypes_get_uint(func) else False

    def _ctypes_get_uint(self, func):
        status = ctypes.c_uint()
        func(self._handle, ctypes.byref(status))
        return status.value

    def _ctypes_get_struct(self, func, fmt, initial):
        buf = struct.pack(fmt, *initial)
        func(self._handle, buf)
        return struct.unpack(fmt, buf)

    def __parse_output(self, packet):
        if not packet:
            return (None, None, None)

        _append_status = self.append_status
        _append_timestamp = self.append_timestamp

        status, timestamp, data = None, None, packet

        if os.name == 'nt':
            if (_append_status and _append_timestamp):
                status = packet[-10:-8]
                timestamp = struct.unpack('q', packet[-8:])[0]
                data = packet[:-10]
            elif (_append_status):
                status = packet[-2:]
                data = packet[:-2]
            elif (_append_timestamp):
                timestamp = struct.unpack('q', packet[-8:])[0]
                data = packet[:-8]

            if timestamp:
                timestamp = timestamp / 10000000 - 11644473600
        else:
            if (_append_status and _append_timestamp):
                status = packet[-18:-16]
                timestamp = struct.unpack('ll', packet[-16:])
                data = packet[:-18]
            elif (_append_status):
                status = packet[-2:]
                data = packet[:-2]
            elif (_append_timestamp):
                timestamp = struct.unpack('ll', packet[-16:])
                data = packet[:-16]

            if timestamp:
                timestamp = timestamp[0] + (float(timestamp[1]) / 1000000)

        return (data, status, timestamp)

    def read(self, timeout=None, size=4096):
        """Reads data from the card."""
        bytes_read = ctypes.c_uint()
        data = bytes(size)

        if timeout:
            #TODO
            if os.name != 'nt':
                raise NotImplementedError()

            e = lib.fscc_read_with_timeout(self._handle, data, size,
                                           ctypes.byref(bytes_read), timeout)

            if e == 0 or e == 997:
                pass
            elif e == FSCC_BUFFER_TOO_SMALL:
                raise BufferTooSmallError()
            else:
                raise Exception(e)
        else:
            e = lib.fscc_read_with_blocking(self._handle, data, size,
                                            ctypes.byref(bytes_read))

            if e == 0:
                pass
            elif e == FSCC_BUFFER_TOO_SMALL:
                raise BufferTooSmallError()
            else:
                raise Exception(e)

        return self.__parse_output(data[:bytes_read.value])

    def write(self, data):
        bytes_written = ctypes.c_uint()
        e = lib.fscc_write_with_blocking(self._handle, data, len(data),
                                         ctypes.byref(bytes_written))

        if e == 0:
            pass
        elif e == FSCC_BUFFER_TOO_SMALL:
            raise BufferTooSmallError()
        elif e == FSCC_TIMEOUT:
            raise TimeoutError()
        else:
            raise Exception(e)

        return bytes_written.value

    def close(self):
        lib.fscc_disconnect(self._handle)

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
    print("Input Memory Cap", p.memory_cap.input)
    print("Output Memory Cap", p.memory_cap.output)
    print("Ignore Timeout", p.ignore_timeout)
    print("Transmit Modifiers", p.tx_modifiers)
    print("RX Multiple", p.rx_multiple)

    print('CCR0', hex(p.registers.CCR0))
    print('CCR1', hex(p.registers.CCR1))
    print('CCR2', hex(p.registers.CCR2))
    print('BGR', hex(p.registers.BGR))

    p.append_status = True
    p.append_timestamp = True
    p.memory_cap.input = 1000000
    p.memory_cap.output = 1000000
    p.ignore_timeout = False
    p.tx_modifiers = 0
    p.rx_multiple = False
    p.clock_frequency = 18432000

    p.purge()

    p.write(b'U')
    print(p.read(100))

    p.close()
