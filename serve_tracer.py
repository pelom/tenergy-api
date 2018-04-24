import os
import jwt

from service.user_service import UserService
from entity.database import Database

from env import log, config

from flask import Flask, jsonify, request, render_template, url_for, redirect, abort

from service.tracerService import TracerService
from service.chargeEquipmentService import ChargeEquipmentService
from service.sampleService import SampleService

logger = log(__name__)
logger.info('ServeTracer')

app = Flask('ServeTracer')
app.config.update(
    DEBUG=True,
    SECRET_KEY=os.urandom(24))

database = Database.get_instance()
user_service = UserService(database)

def get_instance_tracer(charge_port):
    return TracerService(serialclient=None, port=charge_port)


def get_instance_equip(tracer_client):
    return ChargeEquipmentService(tracer_service=tracer_client, database=None)


def get_instance_sample(tracer_client):
    return SampleService(tracer_service=tracer_client, database=None)


logger.info('loading usb...')

usb_port_list = config.get('usb')
usb_port = usb_port_list[0]

logger.debug('usb_port_list: ', usb_port_list)
logger.debug('usb_port: ', usb_port)


@app.route("/device", methods=['GET'])
def device():
    logger.info('device()')

    charge_port = request.headers.get('charge_port', usb_port)
    tracer_service = get_instance_tracer(charge_port)
    charge_equipment_service = get_instance_equip(tracer_service)

    device_info = charge_equipment_service.device_info()
    return jsonify(device_info.to_json())


@app.route("/device/settings", methods=['GET'])
def device_settings():
    logger.info('device_settings()')
    charge_port = request.headers.get('charge_port', usb_port)
    tracer_service = get_instance_tracer(charge_port)
    charge_equipment_service = get_instance_equip(tracer_service)

    setting = charge_equipment_service.device_setting()
    return jsonify(setting)


@app.route("/device/settings", methods=['POST'])
def device_settings_post():
    logger.info('device_settings_post()')
    content = request.get_json(silent=True)

    charge_port = request.headers.get('charge_port', usb_port)
    authorization = request.headers.get('Authorization', None)

    if authorization is None:
        return jsonify({'code': 401, 'status': 'Not Access'})

    user = UserService.get_user_by_session(authorization)

    if user is None:
        return jsonify({'code': 401, 'status': 'Not Access'})

    logger.info('user: {0}'.format(user))
    try:
        tracer_service = get_instance_tracer(charge_port)
        for param in content:
            print param['key'], param['value']
            #tracer_service.write_value(param['key'], param['value'])

    except Exception, ex:
        return jsonify({'code': 500, 'status': str(ex)})

    return jsonify({'code': 200, 'status': 'Success'})


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


if __name__ == "__main__":
    serve_config = config.get('servetracer')

    app.run(host=serve_config.get('ip'),
            port=serve_config.get('port'),
            debug=serve_config.get('debug'))
