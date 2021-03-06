from env import log, config

from entity.database import Database

from service.tracerService import TracerService
from service.chargeEquipmentService import ChargeEquipmentService
from service.sampleService import SampleService

from flask import Flask, jsonify, request

logger = log(__name__)
logger.info('Tenergy Serve')

for key, value in config.iteritems():
    logger.debug('config.json: {0}, {1}'.format(key, value))

database = Database.get_instance()

app = Flask(__name__)

usb_port = config.get('usb')[0]


def get_instance_tracer(charge_port):
    return TracerService(serialclient=None, port=charge_port)


def get_instance_equip(tracer_client):
    return ChargeEquipmentService(tracer_service=tracer_client, database=database)


def get_instance_sample(tracer_client):
    return SampleService(tracer_service=tracer_client, database=database)


@app.route("/device", methods=['GET'])
def device():
    logger.info('device()')

    charge_port = request.headers.get('charge_port', usb_port)
    tracer_service = get_instance_tracer(charge_port)
    charge_equipment_service = get_instance_equip(tracer_service)

    device = charge_equipment_service.device_info()
    return jsonify(device.to_json())


@app.route("/device/settings", methods=['GET'])
def device_settings():
    logger.info('device_settings()')

    charge_port = request.headers.get('charge_port', usb_port)
    tracer_service = get_instance_tracer(charge_port)
    charge_equipment_service = get_instance_equip(tracer_service)

    setting = charge_equipment_service.device_setting()
    return jsonify(setting)


@app.route("/device/sample", methods=['GET'])
def device_sample():
    logger.info('device_sample()')

    charge_port = request.headers.get('charge_port', usb_port)
    tracer_service = get_instance_tracer(charge_port)
    sample_service = get_instance_sample(tracer_service)

    sample = sample_service.sampling()
    return jsonify(sample.to_json())


@app.route("/device/statistical", methods=['GET'])
def device_statistical():
    logger.info('device_statistical()')

    charge_port = request.headers.get('charge_port', usb_port)
    tracer_service = get_instance_tracer(charge_port)
    sample_service = get_instance_sample(tracer_service)

    sample = sample_service.sample_statistical()
    return jsonify(sample.to_json())


@app.route("/chargecontroller/list")
def charge_controller_list():
    logger.info('charge_controller_list()')

    tracer_service = get_instance_tracer(None)
    charge_equipment_service = get_instance_equip(tracer_service)
    result_json = []
    charge_equip_list = charge_equipment_service.find_all()

    for charge in charge_equip_list:
        result_json.append(charge.to_json())
    return jsonify(result_json)


if __name__ == "__main__":
    serve_config = config.get('serve')
    app.run(host=serve_config.get('ip'),
            port=serve_config.get('port'),
            debug=serve_config.get('debug'))
