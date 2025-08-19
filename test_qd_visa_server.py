from unittest import TestCase
import pyvisa

class TestQDVisaServer(TestCase):

    def setUp(self):
        self.rm = pyvisa.ResourceManager()
        self.qd_inst = self.rm.open_resource('TCPIP::127.0.0.1::inst0')

    def test_get_idn(self):
        idn = self.qd_inst.query("*IDN?")
        from backend.qd_ppms import __VENDOR__, __MODEL__, __SERIAL__, __FIRMWARE__
        resp = ','.join((__VENDOR__, __MODEL__, __SERIAL__, __FIRMWARE__))
        assert idn == resp+'\r\n'

    def test_get_temp(self):
        temp = self.qd_inst.query("TEMP?")
        print("resp: " + temp)
