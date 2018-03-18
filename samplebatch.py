import time
from env import config

from service.chargeEquipmentService import ChargeEquipmentService
from service.sampleService import SampleService
from service.tracerService import TracerService

from entity.database import Database

database = Database.get_instance()

usb_list = config.get('usb')

for usb in usb_list:
    print usb
    trancer_serv = TracerService(serialclient=None, port=usb)
    equipment_serv = ChargeEquipmentService(tracer_service=trancer_serv, database=database)
    equipment_list = equipment_serv.find_by_port(usb)

    chargeEquip = equipment_list[0]

    samplingService = SampleService(tracer_service=trancer_serv, database=database)
    samplingService.register(chargeEquip)

# delay = 1
# for i in range(0, 10, delay):
#     print i
#     for usb in usb_list:
#         print usb
#         trancer_serv = TracerService(serialclient=None, port=usb)
#         equipment_serv = ChargeEquipmentService(tracer_service=trancer_serv, database=database)
#         equipment_list = equipment_serv.find_by_port(usb)
#
#         chargeEquip = equipment_list[0]
#
#         samplingService = SampleService(tracer_service=trancer_serv, database=database)
#         samplingService.register(chargeEquip)
#     print 'sleep'
#     time.sleep(5)
