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
        # logger.debug('readValue()')
        value = self.tracerClient.read_input(key)
        logger.debug(str(value))
        return value

    def writeValue(self, key, value):
        print 'writeValue() key: ', key, value
        self.tracerClient.write_output(key, value)

    def parseOptionMap(self, description):
        regex = r"\b((D[0-9]+){1}(\-D?[0-9]+)?: )\b"
        pattern = re.compile(regex)
        resultList = pattern.split(description)
        optionMap = {}
        if len(resultList) < 4:
            return optionMap
        for i in range(0, len(resultList), 4):
            key = resultList[i - 3]
            if key.find(':') > 0:
                optionMap[key.strip()] = resultList[i].strip()

        return optionMap

    def syncRTC(self):
        logger.info('syncRTC()')

        beforeDate = tracer.tracerClient.readRTC()
        syncDate = datetime.now()
        tracer.tracerClient.writeRTC(syncDate)
        afterDate = tracer.tracerClient.readRTC()

        logger.debug('beforeDate: {0}'.format(beforeDate))
        logger.debug('syncDate: {0}'.format(syncDate))
        logger.debug('afterDate: {0}'.format(afterDate))
        return syncDate


if __name__ == "__main__":
    tracer = TracerService()
    tracer.connect()
#   tracer.syncRTC()

    logger.info('Real Time Clocl: {0}'.format(tracer.tracerClient.readRTC()))
#   value = tracer.readValue('Day/Night')
#   value = tracer.readValue('Default Load On/Off in manual mode')
#   value = tracer.readValue('Force the load on/off')

#   value = tracer.readValue('Load controling modes')
#   print 'Load controling modes: {0}'.format(value.register.description.split(',')[value.value])

    tracer.disconnect()
