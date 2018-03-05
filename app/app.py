import requests

from datetime import datetime

from env import log, config

from entity.database import Database

from service.tracerService import TracerService
from service.chargeEquipmentService import ChargeEquipmentService
from service.sampleService import SampleService

from flask import Flask, jsonify, request, render_template

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


@app.route("/device/monitorredirect", methods=['GET'])
def device_monitorredirect():
    logger.info('device_monitorredirect()')

    params = {'date': '2018-03-04'}

    r = requests.get(
        url='http://192.168.0.100:5000/device/monitor',
        params=params)
    return jsonify(r.json())

@app.route("/device/monitor", methods=['GET'])
def device_monitor():
    logger.info('device_monitor()')

    charge_port = request.headers.get('charge_port', usb_port)
    tracer_service = get_instance_tracer(charge_port)
    sample_service = get_instance_sample(tracer_service)

    param_date = request.args.get('date', None)
    now = datetime.now()
    if(param_date is not None):
        now = datetime.strptime(param_date, '%Y-%m-%d')

    sample = sample_service.get_sample(now=now)
    return jsonify(sample)

    # sample = sample_service.sampling()
    # statistical = sample_service.sample_statistical()
    # rtc = tracer_service.tracer_client.read_rtc()
    # samplejson = sample.to_json()
    # samplejson.setdefault('statistical', statistical.to_json())
    # samplejson.setdefault('rtc', rtc.isoformat())
    #return jsonify(samplejson)


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


@app.route('/')
def home():
    url_context = 'http://{0}:{1}/'.format('192.168.0.1', '5000')
    ip = request.remote_addr
    url = request.url
    return render_template('home.html', url_context=url_context, ip=ip, url=url)


if __name__ == "__main__":
    serve_config = config.get('serve')
    app.run(host=serve_config.get('ip'),
            port=serve_config.get('port'),
            debug=serve_config.get('debug'))
