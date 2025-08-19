from backend.base.classes import BaseDevice
from . import __VENDOR__, __MODEL__, __FIRMWARE__, __SERIAL__
from qdcommandparser import QdCommandParser

class PPMSVersalab(BaseDevice):

    def device_init(self):
        self.idn = __VENDOR__, __MODEL__, __SERIAL__, __FIRMWARE__

        self.command = QdCommandParser('VERSALAB', line_term='\r\n')

        self.response = ''
        return
