from pyepsolartracer.client import EPsolarTracerClient

import re
import datetime

from service.env import log

logger = log(__name__)


class TracerService(object):
    def __init__(self, serialclient=None, port='/dev/ttyXRUSB0'):
        self.port = port
        self.tracer_client = TracerService.create_client(serialclient, port)

    @staticmethod
    def create_client(serial, port):
        logger.info('create_client() port: {0}'.format(port))

        tracer_client = EPsolarTracerClient(serialclient=serial, port=port)
        return tracer_client

    def device_info(self):
        logger.info('device_info() port: {0}'.format(self.port))

        self.connect()
        result = self.tracer_client.read_device_info()
        logger.debug('result: {0}'.format(result.information))
        self.disconnect()
        return result.information

    def connect(self):
        logger.info('connect() port: {0}'.format(self.port))

        self.tracer_client.connect()
        return self.tracer_client

    def disconnect(self):
        logger.info('disconnect() port: {0}'.format(self.port))

        self.tracer_client.close()
        return self.tracer_client

    def read_property(self, ref, param):
        logger.info('readProperty() param: {0}'.format(len(param)))

        register_map = dict()
        for key, value in param.iteritems():
            read_value = self.read_value(value)
            setattr(ref, key, read_value.value)
            register_map[key] = read_value
        return register_map

    def read_value(self, key):
        # logger.debug('readValue()')
        value = self.tracer_client.read_input(key)
        logger.debug(str(value))
        return value

    def write_value(self, key, value):
        logger.info('write_value() key: {0}, value: {1}'.format(key, value))

        self.tracer_client.write_output(key, value)

    def parse_option(self, description):
        logger.info('parse_option() description: {0}'.format(description))

        regex = r"\b((D[0-9]+){1}(\-D?[0-9]+)?: )\b"
        pattern = re.compile(regex)
        result_list = pattern.split(description)

        option_map = dict()
        if len(result_list) < 4:
            return option_map

        for i in range(0, len(result_list), 4):
            key = result_list[i - 3]
            if key.find(':') > 0:
                option_map[key.strip()] = result_list[i].strip()

        return option_map

    def sync_rtc(self):
        logger.info('sync_rtc()')

        before_date = self.tracer_client.read_rtc()
        sync_date = datetime.datetime.now()

        self.tracer_client.write_rtc(sync_date)
        after_date = self.tracer_client.read_rtc()

        logger.debug('before_date: {0}'.format(before_date))
        logger.debug('sync_date: {0}'.format(sync_date))
        logger.debug('after_date: {0}'.format(after_date))

        return sync_date


if __name__ == "__main__":
    tracer = TracerService()
    tracer.connect()
#    tracer.sync_rtc()

    logger.info('Real Time Clocl: {0}'.format(tracer.tracer_client.read_rtc()))
    value = tracer.read_value('Day/Night')
    value = tracer.read_value('Charging equipment input voltage')
    #value = tracer.read_value('Night TimeThreshold Volt.(NTTV)')
    #value = tracer.read_value('Light signal startup (night) delay time')

    #tracer.write_value('Manual control the load', 0)
    #   value = tracer.readValue('Default Load On/Off in manual mode')
    #   value = tracer.readValue('Force the load on/off')

    #   value = tracer.readValue('Load controling modes')
    #   print 'Load controling modes: {0}'.format(value.register.description.split(',')[value.value])

    tracer.disconnect()
