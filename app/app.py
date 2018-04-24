import requests

from datetime import datetime

from env import log, config

from entity.database import Database

from service.tracerService import TracerService
from service.chargeEquipmentService import ChargeEquipmentService
from service.sampleService import SampleService
from service.user_service import UserService

from flask import Flask, jsonify, request, render_template, url_for, redirect, abort
from flask_login import LoginManager, login_required, login_user, logout_user

from controller.charge_settings import charge_settings

logger = log(__name__)
logger.info('Tenergy Serve')

for key, value in config.iteritems():
    logger.debug('config.json: {0}, {1}'.format(key, value))

database = Database.get_instance()

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)
usb_port = config.get('usb')[0]

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

user_service = UserService(database)

app.register_blueprint(charge_settings)


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
@login_required
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
        #params=params
    )
    print r.content
    return jsonify(r.json())


@app.route("/device/grouphourredirect", methods=['GET'])
def device_grouphourredirect():
    logger.info('grouphourredirect()')

    params = {'date': '2018-03-04'}

    r = requests.get(
        url='http://192.168.0.100:5000/device/grouphour',
        #params=params
    )
    print r.content
    return jsonify(r.json())


@app.route("/device/grouphour", methods=['GET'])
def device_grouphour():
    logger.info('device_monitor()')

    charge_port = request.headers.get('charge_port', usb_port)
    tracer_service = get_instance_tracer(charge_port)
    sample_service = get_instance_sample(tracer_service)

    param_date = request.args.get('date', None)
    now = datetime.now()
    if(param_date is not None):
        now = datetime.strptime(param_date, '%Y-%m-%d')

    sample = sample_service.get_sample_hour(now=now)
    return jsonify(sample)


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
    print sample_service.get_sample_hour(now=now)
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


@app.route('/index')
def index():
    url_context = 'http://{0}:{1}/'.format('192.168.0.1', '5000')
    ip = request.remote_addr
    url = request.url
    return render_template('home.html', url_context=url_context, ip=ip, url=url)

# @app.route('/settings')
# @login_required
# def settings():
#     logger.info('settings()')
#
#     url_context = 'http://{0}:{1}/device/settings'.format('192.168.0.100', '3000')
#     res = requests.get(
#         url=url_context,
#         # params=params
#     )
#
#     setting = res.json()
#     battery_capacity = setting['BatteryCapacity']
#
#     temp = setting['BatteryRatedVoltage']
#     battery_rated_voltage = temp['Values']
#     battery_rated_voltage_value = temp['Name']
#
#     temp = setting['BatteryType']
#     battery_type = temp['Values']
#     battery_type_value = temp['Name']
#
#     temp = setting['ManagementModeBattery']
#     management_mode_battery = temp['Values']
#     management_mode_battery_value = temp['Name']
#
#     charging_percentage = setting['ChargingPercentage']
#     discharging_percentage = setting['DischargingPercentage']
#
#     high_voltage_disconnect = setting['HighVoltageDisconnect']
#     high_voltage_reconnect = setting['HighVoltageReconnect']
#
#     low_voltage_disconnect = setting['LowVoltageDisconnect']
#     low_voltage_reconnect = setting['LowVoltageReconnect']
#
#     equalization_voltage = setting['EqualizationVoltage']
#     boost_voltage = setting['BoostVoltage']
#     float_voltage = setting['FloatVoltage']
#
#     charging_limit_voltage = setting['ChargingLimitVoltage']
#     discharging_limit_voltage = setting['DischargingLimitVoltage']
#
#     boost_reconnect_voltage = setting['BoostReconnectVoltage']
#     under_voltage_recover = setting['UnderVoltageRecover']
#     under_voltage_warning = setting['UnderVoltageWarning']
#
#     boost_duration = setting['BoostDuration']
#     equalize_duration = setting['EqualizeDuration']
#
#     equalization_charging_cycle = setting['EqualizationChargingCycle']
#     temperature_compensation_coefficient = setting['TemperatureCompensationCoefficient']
#
#     return render_template('settings.html', **locals())


@app.route("/login", methods=["GET", "POST"])
def login():
    logger.info('login()')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_session = user_service.login_user(username, password)
        if user_session is not None:
            login_user(user_session)

            next = request.args.get('next')
            return redirect(next or url_for('index'))

        return abort(401)

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logger.info('logout()')
    logout_user()
    return redirect('login')


@app.errorhandler(401)
def page_not_found(e):
    logger.info('page_not_found()', e)
    return redirect(url_for('login', next=request.path))


@login_manager.user_loader
def load_user(session_id):
    logger.info('load_user()')
    return user_service.get_user_by_session(session_id)


if __name__ == "__main__":
    serve_config = config.get('serve')
    app.run(host=serve_config.get('ip'),
            port=serve_config.get('port'),
            debug=serve_config.get('debug'))
