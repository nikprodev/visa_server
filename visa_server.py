import sys
import os
import signal
import logging
from  threading import Timer
import time
import vxi11_server as vxi11
from backend.qd_ppms.classes import PPMSVersalab

_logging = logging.getLogger(__name__)

def signal_handler(signal, frame):
    _logging.info('Handling Ctrl+C!')
    instr_server.close()
    sys.exit(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    _logging = logging.getLogger(__name__)
	

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')

    _logging.info('Starting VX11 Server')

	
    instr_server = vxi11.InstrumentServer(ip_address='localhost')
    instr_server.add_device_handler(PPMSVersalab, "inst0")
    #instr_server.add_device_handler(LinkBone8x8Device, "inst1")

    instr_server.listen()

    # sleep (or do foreground work) while the Instrument threads do their job
    while True:
        time.sleep(1)
