# -*- coding: iso-8859-15 -*-

# import the server implementation
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.mei_message import *
from pyepsolartracer.registers2 import registerByName

#---------------------------------------------------------------------------#
# Logging
#---------------------------------------------------------------------------#
import logging
_logger = logging.getLogger(__name__)

class EPsolarTracerClient:
    ''' EPsolar Tracer client
    '''

    def __init__(self, unit = 1, serialclient = None, **kwargs):
        ''' Initialize a serial client instance
        '''
        self.unit = unit

        if serialclient == None:
            port = kwargs.get('port', '/dev/ttyXRUSB0')
            baudrate = kwargs.get('baudrate', 115200)
            self.client = ModbusClient(method = 'rtu', port = port, baudrate = baudrate, kwargs = kwargs)
        else:
            self.client = serialclient

    def connect(self):
        ''' Connect to the serial
        :returns: True if connection succeeded, False otherwise
        '''
        return self.client.connect()

    def close(self):
        ''' Closes the underlying connection
        '''
        return self.client.close()

    def read_device_info(self):
        request = ReadDeviceInformationRequest (unit = self.unit)
        response = self.client.execute(request)
        return response

    def read_input(self, name):
        register = registerByName(name)
        if register.is_coil():
            response = self.client.read_coils(register.address, register.size, unit = self.unit)
        elif register.is_discrete_input():
            response = self.client.read_discrete_inputs(register.address, register.size, unit = self.unit)
        elif register.is_input_register():
            response = self.client.read_input_registers(register.address, register.size, unit = self.unit)
        else:
            response = self.client.read_holding_registers(register.address, register.size, unit = self.unit)
        return register.decode(response)

    def write_output(self, name, value):
        register = registerByName(name)
        values = register.encode(value)
        response = False
        if register.is_coil():
            self.client.write_coil(register.address, values, unit = self.unit)
            response = True
        elif register.is_discrete_input():
            _logger.error("Cannot write discrete input " + repr(name))
            pass
        elif register.is_input_register():
            _logger.error("Cannot write input register " + repr(name))
            pass
        else:
            self.client.write_registers(register.address, values, unit = self.unit)
            response = True
        return response

    def readTest(self, values):
        register = registerByName('Real time clock 1')
        print values

        self.client.write_registers(0x9013, values, unit=1)


        result = self.client.read_holding_registers(0x9013, 3, unit=1)

        secmin = result.registers[0]
        print secmin
        secs = (secmin & 0xff)
        minuits = secmin >> 8

        hrday = result.registers[1]
        print hrday
        hr = (hrday & 0xff)
        day = hrday >> 8

        monthyear = result.registers[2]
        print monthyear
        month = (monthyear & 0xff)
        year = monthyear >> 8

        print year, month
        print day, hr
        print minuits, secs

    def encode(self, value):
        # FIXME handle 2 word registers
        rawvalue = int(value * self.times)
        if rawvalue < 0:
            rawvalue = (-rawvalue - 1) ^ 0xffff
            #print rawvalue
        return rawvalue

__all__ = [
    "EPsolarTracerClient",
]
