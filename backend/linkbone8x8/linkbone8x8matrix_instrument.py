import socket


class LinkBone8x8MatrixInstrument(object):
    def __init__(self, ip_address='127.0.0.1'):
        self.sock = None
        self.ip_address = ip_address
        
    def query(self, q):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip_address, 23))
        
        # Skip greetings "Hello. Please enter your command:"
        data = self.sock.recv(100).decode('utf-8')
        if data != 'Hello. Please enter your command:\r\n':
            resp = data.rstrip()
            raise RuntimeError("Unexpected greetings: '{}'".format(resp))

        # Send a query
        req = (q + '\r\n').encode('utf-8')

        self.sock.send(req)
        data = self.sock.recv(1024).decode('utf-8')
        
        # Close socket
        self.sock.close()
        
        return data

    def mode(self, mode):
        return self.query('mode {}'.format(mode))
    
    def on(self, port1, port2):
        return self.query('on {}, {}'.format(port1, port2))
        
    def off(self, port1, port2):
        return self.query('off {}, {}'.format(port1, port2))
        
    def reset(self):
        return self.query('reset')
        
    def status(self):
        return self.query('status')
    
class LinkBone8x8MatrixInstrumentSim(object):

    def __init__(self):
        self.mode = 'single'
        self.rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.cols = ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
        self.matrix = [[False for y in range(8)] for x in range(8)]

    def mode(self, mode):
        self.mode = mode
        return 'Done.\r\n'
    
    def on(self, port1, port2):
        
        return 'Done.\r\n'
        
    def off(self, port1, port2):
        return 'Done.\r\n'
        
    def reset(self):
        return 'Done.\r\n'
        
    def status(self):
        result = 'Mode: {}\r\n'.format(self.mode)
        result += '     {}\r\n'.format(self.cols.join('   '))
        return """Mode: single\r
     I   J   K   L   M   N   O   P\r
A - On  Off Off Off Off Off Off Off\r
B - Off On  Off Off Off Off Off Off\r
C - Off Off On  Off Off Off Off Off\r
D - Off Off Off On  Off Off Off Off\r
E - Off Off Off Off On  Off Off Off\r
F - Off Off Off Off Off On  Off Off\r
G - Off Off Off Off Off Off On  Off\r
H - Off Off Off Off Off Off Off On"""
