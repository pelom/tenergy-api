from pyepsolartracer.client import EPsolarTracerClient

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s %(lineno)d %(levelname)s %(name)s] %(message)s')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

class TracerService(object):
	def __init__(self, serialclient=None, port='/dev/ttyXRUSB0'):
		self.port = port
		self.serialclient = serialclient
		self.createClient()
		
	def createClient(self):
		logger.info('createClient() port: {0}'.format(self.port))
		self.tracerClient = EPsolarTracerClient(serialclient=self.serialclient, port=self.port)
	
	def deviceInfo(self):
		logger.info('deviceInfo() port: {0}'.format(self.port))
		result = self.connect().read_device_info()
		logger.debug('result: {0}'.format(result.information))
		self.disconnect()
		return result.information
	
	def connect(self):
		logger.info('connect() port: {0}'.format(self.port))
		self.tracerClient.connect()
		return self.tracerClient
	
	def disconnect(self):
		logger.info('disconnect() port: {0}'.format(self.port))
		self.tracerClient.close()
		return self.tracerClient
	
	def readProperty(self, ref, paramMap):
		logger.info('readProperty() paramMap: {0}'.format(len(paramMap)))
		registerMap = {}
		for key, value in paramMap.iteritems():
			readValue = self.readValue(value)
			setattr(ref, key, readValue.value)
			registerMap[key] = readValue
		return registerMap
	
	def readValue(self, key):
		#logger.debug('readValue()')
		value = self.tracerClient.read_input(key)
		logger.debug(str(value))
		return value

	def writeValue(self, key, value):
		print 'writeValue() key: ', key, value
		self.tracerClient.write_output(key, value)

if __name__ == "__main__":
	tracer = TracerService()
	print tracer.deviceInfo()
