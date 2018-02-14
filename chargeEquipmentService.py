
from tracerService import TracerService
from entity.database import Database
from entity.chargeEquipment import ChargeEquipment

class ChargeEquipmentService(object):

	def __init__(self):
		self.database = Database();
		self.tracerService = TracerService()
	
	def register(self):
		device = self.deviceInfo()
		self.database.save(device)

	def deviceInfo(self):
		equipInfo = self.tracerService.deviceInfo()
		equip = ChargeEquipment()
		equip.Model = equipInfo[1]
		equip.Version = equipInfo[2]

		fieldMap = self.createEquipmentMap();
		registerMap = self.tracerService.readProperty(equip, fieldMap)
		
		valueMode = registerMap.get('ChargingMode')
		equip.ChargingModeName = valueMode.register.description.split(',')[valueMode.value]
		return equip
	
	def createEquipmentMap(self):
		fieldMap = {}
		fieldMap['ChargingMode']  = 'Charging mode'
		fieldMap['CurrentOfLoad'] = 'Rated output current of load'
		self.createInputEquipmentMap(fieldMap)
		self.createOutputEquipmentMap(fieldMap)
		return fieldMap
	
	def createInputEquipmentMap(self, fieldMap):
		fieldMap['VoltagePV']   = 'Charging equipment rated input voltage'
		fieldMap['CurrentPV']   = 'Charging equipment rated input current'
		fieldMap['PowerPV']     = 'Charging equipment rated input power'
		fieldMap['PowerLowPV']  = 'Charging equipment rated input power L'
		fieldMap['PowerHighPV'] = 'Charging equipment rated input power H'
		return fieldMap

	def createOutputEquipmentMap(self, fieldMap):
		fieldMap['VoltageBattery']   = 'Charging equipment rated output voltage'
		fieldMap['CurrentBattery']   = 'Charging equipment rated output current'
		fieldMap['PowerBattery']     = 'Charging equipment rated output power'
		fieldMap['PowerLowBattery']  = 'Charging equipment rated output power L'
		fieldMap['PowerHighBattery'] = 'Charging equipment rated output power H'
		return fieldMap
	
	def findByModel(self, model):
		return self.database.find(ChargeEquipment, ChargeEquipment.Model==model)

if __name__ == "__main__":
	service = ChargeEquipmentService()
	#service.register()
	#service.database.drop()
	#service.database.create()
	
