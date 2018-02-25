from tracerService import TracerService

from entity.chargeEquipment import ChargeEquipment

from entity.database import Database

from service.env import config


class ChargeEquipmentService(object):
    def __init__(self, tracer_service=None, database=None):
        if tracer_service is None:
            raise ValueError('tracer_service is NULL')

        if database is None:
            raise ValueError('database is NULL')

        self.database = database
        self.tracer_service = tracer_service

    def register(self):
        device = self.device_info()
        self.database.save(device)

    def device_info(self):
        equip_info = self.tracer_service.device_info()

        equip = ChargeEquipment()
        equip.Model = equip_info[1]
        equip.Version = equip_info[2]
        equip.Port = self.tracer_service.port

        field_map = self.equipment_fields()
        register_map = self.tracer_service.read_property(equip, field_map)

        value_mode = register_map.get('ChargingMode')
        equip.ChargingModeName = value_mode.register.description.split(',')[value_mode.value]
        return equip

    def device_setting(self):
        self.tracer_service.connect()

        value_map = dict()

        time_clock = self.tracer_service.tracer_client.read_rtc()
        value_map.setdefault('TimeClock', time_clock.isoformat())

        value = self.tracer_service.read_value('Battery Type')
        value_map.setdefault('BatteryType', ChargeEquipmentService.define_option(value))

        value = self.tracer_service.read_value('Battery Capacity')
        value_map.setdefault('BatteryCapacity', value.value)

        value = self.tracer_service.read_value('Management modes of battery charging and discharging')
        value.register.description = '0-Voltage Compensation,1-SOC'
        value_map.setdefault('ManagementModeBattery', ChargeEquipmentService.define_option(value))

        value = self.tracer_service.read_value('Battery rated voltage code')
        value_map.setdefault('BatteryRatedVoltage', ChargeEquipmentService.define_option(value))

        value = self.tracer_service.read_value('Temperature compensation coefficient')
        value_map.setdefault('TemperatureCompensationCoefficient', value.value)

        value = self.tracer_service.read_value('Equalize duration')
        value_map.setdefault('EqualizeDuration', value.value)

        value = self.tracer_service.read_value('Boost duration')
        value_map.setdefault('BoostDuration', value.value)

        value = self.tracer_service.read_value('Equalization voltage')
        value_map.setdefault('EqualizationVoltage', value.value)

        value = self.tracer_service.read_value('Boost voltage')
        value_map.setdefault('BoostVoltage', value.value)

        value = self.tracer_service.read_value('Float voltage')
        value_map.setdefault('FloatVoltage', value.value)

        value = self.tracer_service.read_value('Charging limit voltage')
        value_map.setdefault('ChargingLimitVoltage', value.value)

        value = self.tracer_service.read_value('Discharging limit voltage')
        value_map.setdefault('DischargingLimitVoltage', value.value)

        value = self.tracer_service.read_value('Charging percentage')
        value_map.setdefault('ChargingPercentage', value.value)

        value = self.tracer_service.read_value('Discharging percentage')
        value_map.setdefault('DischargingPercentage', value.value)

        value = self.tracer_service.read_value('Low voltage reconnect')
        value_map.setdefault('LowVoltageReconnect', value.value)

        value = self.tracer_service.read_value('Low voltage disconnect')
        value_map.setdefault('LowVoltageDisconnect', value.value)

        value = self.tracer_service.read_value('Over voltage reconnect')
        value_map.setdefault('HighVoltageReconnect', value.value)

        value = self.tracer_service.read_value('High Volt.disconnect')
        value_map.setdefault('HighVoltageDisconnect', value.value)

        value = self.tracer_service.read_value('Boost reconnect voltage')
        value_map.setdefault('BoostReconnectVoltage', value.value)

        value = self.tracer_service.read_value('Under voltage recover')
        value_map.setdefault('UnderVoltageRecover', value.value)

        value = self.tracer_service.read_value('Under voltage warning')
        value_map.setdefault('UnderVoltageWarning', value.value)

        value = self.tracer_service.read_value('Equalization charging cycle')
        value_map.setdefault('EqualizationChargingCycle', value.value)

        value = self.tracer_service.read_value('Load controling modes')
        value_map.setdefault('LoadControlingModes', ChargeEquipmentService.define_option(value))

        value = self.tracer_service.read_value('Night TimeThreshold Volt.(NTTV)')
        value_map.setdefault('NightTimeThresholdVolt', value.value)
        value = self.tracer_service.read_value('Light signal startup (night) delay time')
        value_map.setdefault('NightTimeThresholdDelay', value.value)

        value = self.tracer_service.read_value('Day Time Threshold Volt.(DTTV)')
        value_map.setdefault('DayTimeThresholdVolt', value.value)
        value = self.tracer_service.read_value('Light signal turn off(day) delay time')
        value_map.setdefault('DayTimeThresholdDelay', value.value)

        self.tracer_service.disconnect()

        return value_map

    @staticmethod
    def define_option(value):
        values = value.register.description.split(',')

        object_map = dict()
        object_map.setdefault('Code', value.value)
        object_map.setdefault('Name', values[value.value])
        object_map.setdefault('Values', values)
        return object_map

    @staticmethod
    def equipment_fields():
        field_map = dict()
        field_map['ChargingMode'] = 'Charging mode'
        field_map['CurrentOfLoad'] = 'Rated output current of load'
        ChargeEquipmentService.input_equipment_fields(field_map)
        ChargeEquipmentService.output_equipment_fields(field_map)
        return field_map

    @staticmethod
    def input_equipment_fields(field_map):
        field_map['VoltagePV'] = 'Charging equipment rated input voltage'
        field_map['CurrentPV'] = 'Charging equipment rated input current'
        field_map['PowerPV'] = 'Charging equipment rated input power'
        field_map['PowerLowPV'] = 'Charging equipment rated input power L'
        field_map['PowerHighPV'] = 'Charging equipment rated input power H'
        return field_map

    @staticmethod
    def output_equipment_fields(field_map):
        field_map['VoltageBattery'] = 'Charging equipment rated output voltage'
        field_map['CurrentBattery'] = 'Charging equipment rated output current'
        field_map['PowerBattery'] = 'Charging equipment rated output power'
        field_map['PowerLowBattery'] = 'Charging equipment rated output power L'
        field_map['PowerHighBattery'] = 'Charging equipment rated output power H'
        return field_map

    def find_by_model(self, model):
        return self.database.find(ChargeEquipment, ChargeEquipment.Model == model)

    def find_by_port(self, port):
        return self.database.find(ChargeEquipment, ChargeEquipment.Port == port)

    def find_all(self):
        return self.database.find(ChargeEquipment)


if __name__ == "__main__":
    database = Database.get_instance()

    port = config.get('usb')[0]
    tracer_service = TracerService(serialclient=None, port=port)

    service = ChargeEquipmentService(tracer_service=tracer_service, database=database)
    print service.register()
