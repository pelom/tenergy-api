from pyepsolartracer.client import EPsolarTracerClient

import re
import logging
import datetime, time

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

	def parseOptionMap(self, description):
		regex = r"\b((D[0-9]+){1}(\-D?[0-9]+)?: )\b"
		pattern = re.compile(regex)
		resultList =  pattern.split(description)
		optionMap = {}
		if len(resultList) < 4:
			return optionMap
		for i in range(0, len(resultList), 4):
			key = resultList[i-3]
			if key.find(':') > 0:
				optionMap[key.strip()] = resultList[i].strip()

		return optionMap

from datetime import datetime

if __name__ == "__main__":
	tracer = TracerService()
	tracer.connect()

	dt = datetime(2018, 2, 23, 12, 53, 0)
	rtc1 = int( (dt.minute << 8) | dt.second)
	rtc2 = int( (dt.day << 8) | (dt.hour))
	rtc3 = int( (dt.year-2000 << 8) | (dt.month))

	#tracer.tracerClient.readTest([rtc1, rtc2, rtc3])
	valueTime = tracer.readValue('Real time clock 1')
	valueTime2 = tracer.readValue('Real time clock 2')
	valueTime3 = tracer.readValue('Real time clock 3')
	seg = (0xff & valueTime.value)
	min = valueTime.value >> 8
	hor = (0xff & valueTime2.value)
	day = valueTime2.value >> 8
	mot = (0xff & valueTime3.value)
	yea = valueTime3.value >> 8
	print datetime(2000+yea, mot, day, hor, min, seg)

	#tracer.writeValue('Real time clock 3', 18)
	#tracer.writeValue('Real time clock 3', 2)
	#tracer.writeValue('Real time clock 2', 14)
	#tracer.writeValue('Real time clock 2', 0)
	#tracer.writeValue('Real time clock 1', 20)
	#tracer.writeValue('Real time clock 1', 0)
	tracer.disconnect()
