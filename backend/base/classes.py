import abc
import vxi11_server as vxi11

class BaseDevice(vxi11.InstrumentDevice, metaclass=abc.ABCMeta):
    """
    Basic class for the Device
    """

    idn = None
    response = ''
    command = None

    @abc.abstractmethod
    def device_init(self):
        """Initialization function for the Device"""
        raise NotImplemented

    def device_write(self, opaque_data, flags, io_timeout):
        """The device_write RPC is used to write data to the specified device"""
        error = vxi11.Error.NO_ERROR

        commands = opaque_data.decode("ascii").split(";")
        for cmd in commands:
            error = self._process_command(cmd.strip())
            if error != vxi11.Error.NO_ERROR:
                break
        return error

    def device_read(self, request_size, term_char, flags, io_timeout):
        """The device_read RPC is used to read data from the specified device to the controller"""
        error = vxi11.Error.NO_ERROR
        a_str = self.response
        self.response = ""
        reason = vxi11.ReadRespReason.END
        # returns opaque_data!
        return error, reason, a_str.encode("ascii", "ignore")

    def _add_response(self, a_str):
        """Append string to the response"""
        self.response+=a_str

    def _process_command(self, cmd):
        """Send a command to the device and format response"""
        error = vxi11.Error.NO_ERROR

        cmd = cmd.upper()
        if cmd.startswith("*IDN?"):
            self._add_response(','.join(self.idn) + "\r\n")
        else:
            resp = self.command.parse_cmd(cmd)
            self._add_response(resp)
            # error = vxi11.Error.OPERATION_NOT_SUPPORTED
        return error

    def __del__(self):
        """Destroy command"""
        if self.command:
            del self.command
            self.command = None
