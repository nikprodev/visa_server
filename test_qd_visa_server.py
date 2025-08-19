from unittest import TestCase
import pyvisa
import time

class TestQDVisaServer(TestCase):
    """
    The tests are run with the visa_server running and the MultiVu launched in simulation mode.
    """

    def setUp(self):
        self.rm = pyvisa.ResourceManager()
        self.qd_inst = self.rm.open_resource('TCPIP::127.0.0.1::inst0')

    def test_get_idn(self):
        idn = self.qd_inst.query("*IDN?")
        from backend.qd_ppms import __VENDOR__, __MODEL__, __SERIAL__, __FIRMWARE__
        resp = ','.join((__VENDOR__, __MODEL__, __SERIAL__, __FIRMWARE__))
        self.assertEqual(idn, resp + '\r\n')

    def test_get_temp(self):
        resp = self.qd_inst.query("TEMP 300,20,0")
        self.assertEqual(resp, 'OK' + '\r\n')
        time.sleep(4.1)
        temp = self.qd_inst.query("TEMP?")
        self.assertEqual(temp, '0,300.0,"K",1,"Stable"' + '\r\n')

    def test_set_temp(self):
        resp = self.qd_inst.query("TEMP 301,20,0")
        self.assertEqual(resp, 'OK' + '\r\n')
        time.sleep(4.1)
        temp = self.qd_inst.query("TEMP?")
        self.assertEqual(temp, '0,301.0,"K",1,"Stable"' + '\r\n')
        resp = self.qd_inst.query("TEMP 300,20,0")
        self.assertEqual(resp, 'OK' + '\r\n')
        time.sleep(4.1)
        temp = self.qd_inst.query("TEMP?")
        self.assertEqual(temp, '0,300.0,"K",1,"Stable"' + '\r\n')

    def test_get_field(self):
        resp = self.qd_inst.query("FIELD 0,10,0,0")
        self.assertEqual(resp, 'OK' + '\r\n')
        time.sleep(1.1)
        field = self.qd_inst.query("FIELD?")
        self.assertEqual(field, '0,0.0,"Oe",1,"Stable"' + '\r\n')

    def test_set_field(self):
        resp = self.qd_inst.query("FIELD 10,10,0,0")
        self.assertEqual(resp, 'OK' + '\r\n')
        time.sleep(1.1)
        field = self.qd_inst.query("FIELD?")
        self.assertEqual(field, '0,10.0,"Oe",1,"Stable"' + '\r\n')
