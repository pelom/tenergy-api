import datetime

from tracerService import TracerService

from entity.database import Database

from env import config

from entity.sample import Sample
from entity.sampleStatistical import SampleStatistical

from sqlalchemy import func, desc
import sqlalchemy as sa
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

    def get_sample_hour(self, now=datetime.datetime.now()):
        start_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        end_date = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

        session = self.database.create_session()
        query = session.query(func.max(Sample.CreatedDate),
                              func.avg(Sample.VoltageBattery),
                              func.avg(Sample.CurrentBattery),
                              func.avg(Sample.PowerBattery),
                              func.avg(Sample.BatterySOC))
        query = query.filter(Sample.VoltageBattery.isnot(None),
                             Sample.CurrentBattery.isnot(None), Sample.PowerBattery.isnot(None),
                             Sample.CreatedDate >= start_date, Sample.CreatedDate < end_date)
        query = query.order_by(desc(Sample.CreatedDate))
        query = query.group_by(sa.func.strftime("%Y-%m-%d-%H", Sample.CreatedDate))

        #query = query.limit(1)
        sampleHour = query.all()

        result = []
        for it in range(0, len(sampleHour)):
            result.append({
                "CreatedDate": None if not sampleHour[it][0] else sampleHour[it][0].isoformat(),
                "VoltageBattery": sampleHour[it][1],
                "CurrentBattery": sampleHour[it][2],
                "PowerBattery": sampleHour[it][3],
                "BatterySOC": sampleHour[it][4],
            })
        return result

    def get_sample(self, now=datetime.datetime.now()):
        print 'now', now

        start_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        end_date = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

        session = self.database.create_session()
        query = session.query(Sample)
        query = query.order_by(desc(Sample.CreatedDate))
        query = query.limit(1)
        sample = query.first()

        query = session.query(
            func.avg(Sample.PowerLowBattery), func.max(Sample.PowerLowBattery), func.min(Sample.PowerLowBattery),
            func.avg(Sample.CurrentBattery), func.max(Sample.CurrentBattery), func.min(Sample.CurrentBattery),
            func.avg(Sample.VoltageBattery), func.max(Sample.VoltageBattery), func.min(Sample.VoltageBattery))

        query = query.filter(Sample.VoltageBattery > 0,
                             Sample.CreatedDate >= start_date, Sample.CreatedDate < end_date)
        battery = query.first()

        query = session.query(func.min(Sample.CreatedDate), func.max(Sample.CreatedDate),
                              func.avg(Sample.PowerLowPV), func.max(Sample.PowerLowPV), func.min(Sample.PowerLowPV),
                              func.avg(Sample.CurrentPV), func.max(Sample.CurrentPV), func.min(Sample.CurrentPV),
                              func.avg(Sample.VoltagePV), func.max(Sample.VoltagePV), func.min(Sample.VoltagePV)
                              )

        query = query.filter(Sample.PowerLowPV > 0,
                             Sample.CreatedDate >= start_date, Sample.CreatedDate < end_date)
        pv = query.first()

        query = session.query(
                            func.min(Sample.CreatedDate), func.max(Sample.CreatedDate),
                              func.avg(Sample.PowerLowDischarging), func.max(Sample.PowerLowDischarging), func.min(Sample.PowerLowDischarging),
                              func.avg(Sample.CurrentDischarging), func.max(Sample.CurrentDischarging), func.min(Sample.CurrentDischarging),
                              func.avg(Sample.VoltageDischarging), func.max(Sample.VoltageDischarging), func.min(Sample.VoltageDischarging)
                              )
        query = query.filter(Sample.PowerLowDischarging > 0,
                             Sample.CreatedDate >= start_date, Sample.CreatedDate < end_date)
        load = query.first()

        fator = 0
        hour = 0
        minute = 0

        if pv[0] is None:
            pv = ['', '', 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            diff_time = pv[1] - pv[0]
            hour = diff_time.seconds // 3600
            minute = (diff_time.seconds // 60) % 60
            fator = float(hour + (minute / float(60)))

        loadhour = 0

        if load[0] is None:
            load = ['', '', 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            diff_time = load[1] - load[0]
            loadhour = diff_time.seconds // 3600
            #minute = (diff_time.seconds // 60) % 60
            #fator = float(hour + (minute / float(60)))

        return {
            "sample": sample.to_json(),
            "generated": {
                "start": None if not pv[0] else pv[0].isoformat(),
                "end": None if not pv[1] else pv[1].isoformat(),
                "hour": hour,
                "minute": minute,
                "power": {
                    "avg": pv[2],
                    "max": pv[3],
                    "min": pv[4],
                    "total": pv[2] * hour
                },
                "current": {
                    "avg": pv[5],
                    "max": pv[6],
                    "min": pv[7],
                    "total": pv[5] * hour
                },
                "voltage": {
                    "avg": pv[8],
                    "max": pv[9],
                    "min": pv[10]
                }
            },
            "battery": {
                "power": {
                    "avg": battery[0],
                    "max": battery[1],
                    "min": battery[2],
                },
                "current": {
                    "avg": battery[3],
                    "max": battery[4],
                    "min": battery[5],
                },
                "voltage": {
                    "avg": battery[6],
                    "max": battery[7],
                    "min": battery[8]
                }
            },
            "discharging": {
                "start": None if not load[0] else load[0].isoformat(),
                "end": None if not load[1] else load[1].isoformat(),
                "hour": loadhour,
                "power": {
                    "avg": load[2],
                    "max": load[3],
                    "min": load[4],
                    "total": load[2] * hour
                },
                "current": {
                    "avg": load[5],
                    "max": load[6],
                    "min": load[7],
                    "total": load[5] * hour
                },
                "voltage": {
                    "avg": load[8],
                    "max": load[9],
                    "min": load[10]
                }
            }
        }

if __name__ == "__main__":
    database = Database.get_instance()

    port = config.get('usb')[0]
    tracer_service = TracerService(serialclient=None, port=port)
    tracer_service.sync_rtc()
    print tracer_service.read_value('Battery Capacity')
#    tracer_service.write_value('Battery Capacity', 60)
#    print tracer_service.read_value('Battery Capacity')

#    chargeEquipmentService = ChargeEquipmentService(tracer_service=tracer_service, database=database)
#    chargeEquipmentService.database.create()
#    chargeEquipList = chargeEquipmentService.find_by_model('Tracer4210A')
#    chargeEquip = chargeEquipList[0]

#    samplingService = SampleService(tracer_service=tracer_service, database=database)
#    print samplingService.get_sample()
#    samplingService.register_statistical(chargeEquip)
#    samplingService.register(chargeEquip)
#    while True:
#        time.sleep(60 * 60)