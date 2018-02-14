import time

from tracerService import TracerService

from entity.database import Database
from entity.chargeEquipment import ChargeEquipment
from entity.sample import Sample

from chargeEquipmentService import ChargeEquipmentService

class SamplingService(object):
    def __init__(self):
        self.database = Database();
        self.tracerService = TracerService()

    def register(self, chargeEquip):
        sample = self.sampling(chargeEquip.Id)
        self.database.save(sample)
        return sample

    def sampling(self, chargeEquipId=None):
        self.tracerService.connect();

        sample = Sample()
        sample.ChargeEquipmentId = chargeEquipId

        fieldMap = self.createSamplingFieldMap();
        registerMap = self.tracerService.readProperty(sample, fieldMap)

        self.setCodeStatusEquipment(sample, registerMap)
        self.setCodeStatusBattery(sample, registerMap)
        self.setCodeStatusDischarging(sample, registerMap)

        self.tracerService.disconnect()
        return sample

    def createSamplingFieldMap(self):
        fieldMap = {}
        self.setSamplingFieldPv(fieldMap)
        self.setSamplingFieldBattery(fieldMap)
        self.setSamplingFieldDischarging(fieldMap)
        self.setSamplingFieldStatus(fieldMap)
        return fieldMap

    def setSamplingFieldPv(self, fieldMap):
        fieldMap['VoltagePV']   = 'Charging equipment input voltage'
        fieldMap['CurrentPV']   = 'Charging equipment input current'
        fieldMap['PowerPV']     = 'Charging equipment input power'
        fieldMap['PowerLowPV']  = 'Charging equipment input power L'
        fieldMap['PowerHighPV'] = 'Charging equipment input power H'
        return fieldMap

    def setSamplingFieldBattery(self, fieldMap):
        fieldMap['VoltageBattery']   = 'Charging equipment output voltage'
        fieldMap['CurrentBattery']   = 'Charging equipment output current'
        fieldMap['PowerBattery']     = 'Charging equipment output power'
        fieldMap['PowerLowBattery']  = 'Charging equipment output power L'
        fieldMap['PowerHighBattery'] = 'Charging equipment output power H'
        return fieldMap

    def setSamplingFieldDischarging(self, fieldMap):
        fieldMap['VoltageDischarging']   = 'Discharging equipment output voltage'
        fieldMap['CurrentDischarging']   = 'Discharging equipment output current'
        fieldMap['PowerDischarging']     = 'Discharging equipment output power'
        fieldMap['PowerLowDischarging']  = 'Discharging equipment output power L'
        fieldMap['PowerHighDischarging'] = 'Discharging equipment output power H'
        return fieldMap

    def setSamplingFieldStatus(self, fieldMap):
        fieldMap['TemperatureBattery']         = 'Battery Temperature'
        fieldMap['TemperatureInsideEquipment'] = 'Temperature inside equipment'
        fieldMap['TemperaturePowerComponents'] = 'Power components temperature'
        fieldMap['TemperatureRemoteBattery']   = 'Remote battery temperature'

        fieldMap['BatterySOC']                 = 'Battery SOC'
        fieldMap['VoltageSystemBattery']       = "Battery's real rated power"

        fieldMap['CodeStatusBattery']     = 'Battery status'
        fieldMap['CodeStatusEquipment']   = 'Charging equipment status'
        fieldMap['CodeStatusDischarging'] = 'Discharging equipment status'
        return fieldMap

    def setCodeStatusDischarging(self, sampling, registerMap):
        dischargingStatus = registerMap.get('CodeStatusDischarging')
        optionMap = self.tracerService.parseOptionMap(dischargingStatus.register.description)
        optionValue = optionMap.get('D0:')
        if optionValue != None:
            sampling.StatusDischarging = optionValue.split(',')[dischargingStatus.value]

    def setCodeStatusBattery(self, sampling, registerMap):
        batteryStatus = registerMap.get('CodeStatusBattery')
        optionMap = self.tracerService.parseOptionMap(batteryStatus.register.description)
        optionValue = optionMap.get('D3-D0:')
        if optionValue != None:
            batteryLevel = 0b1111 & batteryStatus.value
            sampling.StatusBattery = optionValue.split(',')[batteryLevel]

    def setCodeStatusEquipment(self, sampling, registerMap):
        equipStatus = registerMap.get('CodeStatusEquipment')
        if equipStatus.value >> 4:
            print 'CodeStatusEquipment ERROR'

        optionMap = self.tracerService.parseOptionMap(equipStatus.register.description)
        optionValue = optionMap.get('D3-2:')
        if optionValue != None:
            chargeStatus = 0b11 & (equipStatus.value >> 2)
            optionItem = optionValue[optionValue.find('.') + 1:len(optionValue)]
            sampling.CodeStatusCharge = chargeStatus
            sampling.StatusCharge = optionItem.split(',')[chargeStatus]

if __name__ == "__main__":
    chargeEquipmentService = ChargeEquipmentService()
    chargeEquipList = chargeEquipmentService.findByModel('Tracer4210A')

    chargeEquip = chargeEquipList[0]

    samplingService = SamplingService()
    sampling = samplingService.register(chargeEquip)

    print 'CHARGE EQUIPMENT'
    print 'chargeEquip.Model: ', chargeEquip.Model
    print 'chargeEquip.Version: ', chargeEquip.Version
    print 'chargeEquip.ChargingModeName: ', chargeEquip.ChargingModeName
    print 'chargeEquip.CurrentOfLoad: ', chargeEquip.CurrentOfLoad
    print 'chargeEquip.VoltageBattery: ', chargeEquip.VoltageBattery
    print 'chargeEquip.PowerPV: ', chargeEquip.PowerPV
    print 'PV'
    print 'sampling.VoltagePV: ', sampling.VoltagePV
    print 'sampling.CurrentPV: ', sampling.CurrentPV
    print 'sampling.PowerPV: ', sampling.PowerPV
    print 'sampling.PowerLowPV: ', sampling.PowerLowPV
    print 'sampling.PowerHighPV: ', sampling.PowerHighPV
    print 'BATTERY'
    print 'sampling.VoltageBattery: ', sampling.VoltageBattery
    print 'sampling.CurrentBattery: ', sampling.CurrentBattery
    print 'sampling.PowerBattery: ', sampling.PowerBattery
    print 'sampling.PowerLowBattery: ', sampling.PowerLowBattery
    print 'sampling.PowerHighBattery: ', sampling.PowerHighBattery

    print 'LOAD'
    print 'sampling.VoltageDischarging: ', sampling.VoltageDischarging
    print 'sampling.CurrentDischarging: ', sampling.CurrentDischarging
    print 'sampling.PowerDischarging: ', sampling.PowerDischarging
    print 'sampling.PowerLowDischarging: ', sampling.PowerLowDischarging
    print 'sampling.PowerHighDischarging: ', sampling.PowerHighDischarging

    print 'TEMPERATURE'
    print 'sampling.TemperatureBattery: ', sampling.TemperatureBattery
    print 'sampling.TemperatureRemoteBattery: ', sampling.TemperatureRemoteBattery
    print 'sampling.TemperaturePowerComponents: ', sampling.TemperaturePowerComponents
    print 'sampling.TemperatureInsideEquipment: ', sampling.TemperatureInsideEquipment

    print 'STATUS'
    print 'sampling.BatterySOC: ', sampling.BatterySOC
    print 'sampling.VoltageSystemBattery: ', sampling.VoltageSystemBattery

    print 'sampling.CodeStatusBattery: ', sampling.CodeStatusBattery
    print 'sampling.StatusBattery: ', sampling.StatusBattery
    print 'sampling.CodeStatusEquipment: ', sampling.CodeStatusEquipment

    print 'sampling.CodeStatusCharge: ', sampling.CodeStatusCharge
    print 'sampling.StatusCharge: ', sampling.StatusCharge

    print 'sampling.CodeStatusDischarging: ', sampling.CodeStatusDischarging
    print 'sampling.StatusDischarging: ', sampling.StatusDischarging

#    while True:
#    time.sleep(60*5)
