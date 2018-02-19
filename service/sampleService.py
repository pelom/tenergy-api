from tracerService import TracerService

from entity.database import Database

from env import log, config

from entity.sample import Sample
from entity.sampleStatistical import SampleStatistical

from chargeEquipmentService import ChargeEquipmentService


class SampleService(object):
    def __init__(self, tracer_service=None, database=None):
        if tracer_service is None:
            raise ValueError('tracer_service is NULL')

        if database is None:
            raise ValueError('database is NULL')

        self.database = database
        self.tracer_service = tracer_service

    def register(self, charge_equip):
        sample = self.sampling(charge_equip.Id)
        self.database.save(sample)
        return sample

    def sampling(self, charge_equip_id=None):
        self.tracer_service.connect()

        sample = Sample()
        sample.ChargeEquipmentId = charge_equip_id

        field_map = SampleService.sampling_fields()
        register_map = self.tracer_service.read_property(sample, field_map)

        self.set_code_status_equipment(sample, register_map)
        self.set_code_status_battery(sample, register_map)
        self.set_code_status_discharging(sample, register_map)

        self.tracer_service.disconnect()
        return sample

    def register_statistical(self, charge_equip):
        statis = self.sample_statistical(charge_equip.Id)
        self.database.save(statis)
        return statis

    def sample_statistical(self, charge_equip_id=None):
        self.tracer_service.connect()

        sample_statis = SampleStatistical()
        sample_statis.ChargeEquipmentId = charge_equip_id

        field_map = SampleService.statistical_fields()
        self.tracer_service.read_property(sample_statis, field_map)
        self.tracer_service.disconnect()
        return sample_statis

    @staticmethod
    def sampling_fields():
        field_map = dict()
        SampleService.sampling_pv_fields(field_map)
        SampleService.sampling_battery_fields(field_map)
        SampleService.sampling_discharging_fields(field_map)
        SampleService.sampling_status_fields(field_map)
        return field_map

    @staticmethod
    def sampling_pv_fields(field_map):
        field_map['VoltagePV'] = 'Charging equipment input voltage'
        field_map['CurrentPV'] = 'Charging equipment input current'
        field_map['PowerPV'] = 'Charging equipment input power'
        field_map['PowerLowPV'] = 'Charging equipment input power L'
        field_map['PowerHighPV'] = 'Charging equipment input power H'
        return field_map

    @staticmethod
    def sampling_battery_fields(field_map):
        field_map['VoltageBattery'] = 'Charging equipment output voltage'
        field_map['CurrentBattery'] = 'Charging equipment output current'
        field_map['PowerBattery'] = 'Charging equipment output power'
        field_map['PowerLowBattery'] = 'Charging equipment output power L'
        field_map['PowerHighBattery'] = 'Charging equipment output power H'
        return field_map

    @staticmethod
    def sampling_discharging_fields(field_map):
        field_map['VoltageDischarging'] = 'Discharging equipment output voltage'
        field_map['CurrentDischarging'] = 'Discharging equipment output current'
        field_map['PowerDischarging'] = 'Discharging equipment output power'
        field_map['PowerLowDischarging'] = 'Discharging equipment output power L'
        field_map['PowerHighDischarging'] = 'Discharging equipment output power H'
        return field_map

    @staticmethod
    def sampling_status_fields(field_map):
        field_map['TemperatureBattery'] = 'Battery Temperature'
        field_map['TemperatureInsideEquipment'] = 'Temperature inside equipment'
        field_map['TemperaturePowerComponents'] = 'Power components temperature'
        field_map['TemperatureRemoteBattery'] = 'Remote battery temperature'

        field_map['BatterySOC'] = 'Battery SOC'
        field_map['VoltageSystemBattery'] = "Battery's real rated power"

        field_map['CodeStatusBattery'] = 'Battery status'
        field_map['CodeStatusEquipment'] = 'Charging equipment status'
        field_map['CodeStatusDischarging'] = 'Discharging equipment status'
        return field_map

    def set_code_status_discharging(self, sampling, register_map):
        discharging_status = register_map.get('CodeStatusDischarging')
        option_map = self.tracer_service.parse_option(discharging_status.register.description)
        option_value = option_map.get('D0:')
        if option_value is not None:
            sampling.StatusDischarging = option_value.split(',')[discharging_status.value]

    def set_code_status_battery(self, sampling, register_map):
        battery_status = register_map.get('CodeStatusBattery')
        option_map = self.tracer_service.parse_option(battery_status.register.description)
        option_value = option_map.get('D3-D0:')
        if option_value is not None:
            battery_level = 0b1111 & battery_status.value
            sampling.StatusBattery = option_value.split(',')[battery_level]

    def set_code_status_equipment(self, sampling, register_map):
        equip_status = register_map.get('CodeStatusEquipment')
        if equip_status.value >> 4:
            print 'CodeStatusEquipment ERROR'

        option_map = self.tracer_service.parse_option(equip_status.register.description)
        option_value = option_map.get('D3-2:')
        if option_value is not None:
            charge_status = 0b11 & (equip_status.value >> 2)
            option_item = option_value[option_value.find('.') + 1:len(option_value)]
            sampling.CodeStatusCharge = charge_status
            sampling.StatusCharge = option_item.split(',')[charge_status]

    @staticmethod
    def statistical_fields():
        value_fields = dict()
        value_fields['VoltageMaxPV'] = 'Maximum input volt (PV) today'
        value_fields['VoltageMinPV'] = 'Minimum input volt (PV) today'
        value_fields['VoltageMaxBattery'] = 'Maximum battery volt today'
        value_fields['VoltageMinBattery'] = 'Minimum battery volt today'
        value_fields['ConsumedEnergy'] = 'Consumed energy today'
        value_fields['ConsumedEnergyLow'] = 'Consumed energy today L'
        value_fields['ConsumedEnergyHigh'] = 'Consumed energy today H'
        value_fields['GeneratedEnergy'] = 'Generated energy today'
        value_fields['GeneratedEnergyLow'] = 'Generated energy today L'
        value_fields['GeneratedEnergyHigh'] = 'Generated energy today H'
        value_fields['BatteryCurrent'] = 'Battery Current'
        value_fields['BatteryCurrentLow'] = 'Battery Current L'
        value_fields['BatteryCurrentHigh'] = 'Battery Current H'
        value_fields['BatteryTemp'] = 'Battery Temp.'
        value_fields['AmbientTemp'] = 'Ambient Temp.'
        return value_fields


if __name__ == "__main__":
    database = Database.get_instance()

    port = config.get('usb')[0]
    tracer_service = TracerService(serialclient=None, port=port)

    chargeEquipmentService = ChargeEquipmentService(tracer_service=tracer_service, database=database)
    chargeEquipmentService.database.create()
    chargeEquipList = chargeEquipmentService.find_by_model('Tracer4210A')
    chargeEquip = chargeEquipList[0]

    samplingService = SampleService(tracer_service=tracer_service, database=database)
#    samplingService.register_statistical(chargeEquip)
#    samplingService.register(chargeEquip)
#    while True:
#        time.sleep(60 * 60)
