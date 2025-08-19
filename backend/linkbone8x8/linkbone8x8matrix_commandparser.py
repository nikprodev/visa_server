from linkbone8x8matrix_instrument import LinkBone8x8MatrixInstrument, LinkBone8x8MatrixInstrumentSim

class LinkBone8x8MatrixCommandParser(object):

    def __init__(self, line_term = '\r\n', ip_address='127.0.0.1', simulate_mode=False):
        self._ip_address = ip_address
        self._line_term = line_term

        self.cmd_list = {
            'MODE': (self.set_mode, None),
            'ON': (self.set_port_on, None),
            'OFF': (self.set_port_off, None),
            'RESET': (self.set_reset, None),
            'STATUS': (None, self.get_status),
        }

        if simulate_mode:
            self._instrument = LinkBone8x8MatrixInstrumentSim()
        else:
            self._instrument = LinkBone8x8MatrixInstrument(ip_address)
            
        
    def parse_cmd(self, data):
        cmd = data.split(' ')[0]
        for test_cmd in self.cmd_list:
            if cmd.find(test_cmd) == 0:
                if cmd.find(test_cmd + '?') == 0:
                    if self.cmd_list[test_cmd][1]:
                        return str(self.cmd_list[test_cmd][1]()) + self._line_term
                else:
                    if test_cmd == 'reset':
                        return self.set_reset()
                    else:
                        try:
                            cmd, arg_string = data.split(' ', 1)
                        except:
                            return 'No argument(s) given for command {0}.'.format(test_cmd) + self._line_term
                        if self.cmd_list[test_cmd][0]:
                            return str(self.cmd_list[test_cmd][0](arg_string))
        return 'Unknown command: {0}.'.format(data) + self._line_term
        
    
    def set_mode(self, arg_string):
        return self._instrument.mode(arg_string)
        
    def set_port_on(self, arg_string):
        port1, port2 = arg_string.split(',')
        return self._instrument.on(port1, port2)
        
    def set_port_off(self, arg_string):
        port1, port2 = arg_string.split(',')
        return self._instrument.off(port1, port2)
        
    def set_reset(self):
        return self._instrument.reset()
        
    def get_status(self):
        return self._instrument.status()
