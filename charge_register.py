from entity.database import Database

from service.tracerService import TracerService
from service.chargeEquipmentService import ChargeEquipmentService

from env import config

database = Database.get_instance()

port = config.get('usb')[0]
tracer_service = TracerService(serialclient=None, port=port)

# service = ChargeEquipmentService(tracer_service=tracer_service, database=database)
# print service.register()

# tracer_service.read_value('Battery Capacity')
# tracer_service.write_value('Battery Capacity', 220)
# print tracer_service.read_value('Battery Capacity')
tracer_service.sync_rtc()