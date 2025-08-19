from backend.base.classes import BaseDevice
from . import __IPADDRESS__, __VENDOR__, __MODEL__, __SERIAL__, __FIRMWARE__
from linkbone8x8matrix_commandparser import LinkBone8x8MatrixCommandParser


class LinkBone8x8(BaseDevice):

    def __init__(self, ip=None):
        super(LinkBone8x8, self).__init__()
        self.ip = ip

    def device_init(self):
        self.idn = __VENDOR__, __MODEL__, __SERIAL__, __FIRMWARE__
        self.command = LinkBone8x8MatrixCommandParser(ip_address=__IPADDRESS__)

        self.response = ''
        return
