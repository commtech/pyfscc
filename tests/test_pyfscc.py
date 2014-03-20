import unittest

from fscc import Port


class FsccTestCase(unittest.TestCase):
    def setUp(self):
        self.port = Port(0, 'r+b')

        self.port.append_status = True
        self.port.append_timestamp = True
        self.port.input_memory_cap = 1000000
        self.port.output_memory_cap = 1000000
        self.port.ignore_timeout = False
        self.port.tx_modifiers = 0
        self.port.rx_multiple = False

        self.port.purge()


class AttrTestCase(FsccTestCase):
    def boolean_attr_test(self, name=None):
        if name:
            # Test the attribute exists
            getattr(self.port, name)

            # Tests the attribute retains it's values
            setattr(self.port, name, True)
            self.assertTrue(getattr(self.port, name), True)
            setattr(self.port, name, False)
            self.assertFalse(getattr(self.port, name), False)

    def test_append_status(self):
        self.boolean_attr_test('append_status')

    def test_append_timestamp(self):
        self.boolean_attr_test('append_timestamp')

    def test_ignore_timeout(self):
        self.boolean_attr_test('ignore_timeout')

    def test_rx_multiple(self):
        self.boolean_attr_test('rx_multiple')

    def test_imemcap(self):
            # Test the attribute exists
            self.port.input_memory_cap

            # Tests the attribute retains it's values
            self.port.input_memory_cap = 10000
            self.assertEqual(self.port.input_memory_cap, 10000)

    def test_omemcap(self):
            # Test the attribute exists
            self.port.output_memory_cap

            # Tests the attribute retains it's values
            self.port.output_memory_cap = 10000
            self.assertEqual(self.port.output_memory_cap, 10000)

    def test_tx_modifiers(self):
            # Test the attribute exists
            self.port.input_memory_cap

            # Tests the attribute retains it's values
            self.port.input_memory_cap = 0
            self.assertEqual(self.port.input_memory_cap, 0)


class RWTestCase(FsccTestCase):

    def test_read_dataonly(self):
        self.port.write(b'U')
        self.port.append_status = False
        self.port.append_timestamp = False
        data = self.port.read()
        self.assertEqual(data[0], b'U')
        self.assertIsNone(data[1])
        self.assertIsNone(data[2])

    def test_read_append_timestamp(self):
        self.port.write(b'U')
        self.port.append_status = False
        self.port.append_timestamp = True
        data = self.port.read()
        self.assertEqual(data[0], b'U')
        self.assertIsNone(data[1])
        self.assertIsNotNone(data[2])

    def test_read_append_status(self):
        self.port.write(b'U')
        self.port.append_status = True
        self.port.append_timestamp = False
        data = self.port.read()
        self.assertEqual(data[0], b'U')
        self.assertEqual(len(data[1]), 2)
        self.assertIsNone(data[2])

    def test_read_append_both(self):
        self.port.write(b'U')
        self.port.append_status = True
        self.port.append_timestamp = True
        data = self.port.read()
        self.assertEqual(data[0], b'U')
        self.assertEqual(len(data[1]), 2)
        self.assertIsNotNone(data[2])


class RegisterTestCase(FsccTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = None
        self.readonly = False
        self.writeonly = False

    def test_writeonly(self):
        if self.reg_name:
            if self.writeonly:
                self.assertFalse(hasattr(self.port.registers, self.reg_name))
            else:
                self.assertTrue(hasattr(self.port.registers, self.reg_name))

    def test_readonly(self):
        if self.reg_name:
            try:
                reg_val = getattr(self.port.registers, self.reg_name)
            except AttributeError:
                reg_val = 0

            if self.readonly:
                with self.assertRaises(AttributeError):
                    setattr(self.port.registers, self.reg_name, reg_val)
            else:
                setattr(self.port.registers, self.reg_name, reg_val)


class FIFOT_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'FIFOT'


class CMDR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'CMDR'
        self.writeonly = True


class STAR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'STAR'
        self.readonly = True


class CCR0_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'CCR0'


class CCR1TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'CCR1'


class CCR2_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'CCR2'


class BGR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'BGR'


class SSR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'SSR'


class SMR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'SMR'


class TSR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'TSR'


class TMR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'TMR'


class RAR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'RAR'


class RAMR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'RAMR'


class PPR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'PPR'


class TCR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'TCR'


class VSTR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'VSTR'
        self.readonly = True


class IMR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'IMR'


class DPLLR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'DPLLR'


class FCR_TestCase(RegisterTestCase):
    def setUp(self):
        super().setUp()
        self.reg_name = 'FCR'


if __name__ == '__main__':
    unittest.main()
