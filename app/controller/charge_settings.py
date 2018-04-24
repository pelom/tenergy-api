from flask import Blueprint

import requests

from env import log, config

from flask import Flask, jsonify, request, render_template, url_for, redirect, abort, app
from flask_login import LoginManager, login_required, login_user, logout_user

logger = log(__name__)

charge_settings = Blueprint('charge_settings', __name__)

@charge_settings.route('/settings', methods=['GET'])
@login_required
def get_settings():
    logger.info('get_settings()')

    url_context = 'http://{0}:{1}/device/settings'.format('192.168.0.100', '3000')

    try:
        res = requests.get(url=url_context,
            # params=params
        )

        if res.status_code is not 200:
            logger.debug('Response ERROR', res)
            return

        setting = res.json()

        print type(setting)

        battery_capacity = setting['BatteryCapacity']

        temp = setting['BatteryRatedVoltage']
        battery_rated_voltage = temp['Values']
        battery_rated_voltage_value = temp['Name']

        temp = setting['BatteryType']
        battery_type = temp['Values']
        battery_type_value = temp['Name']

        temp = setting['ManagementModeBattery']
        management_mode_battery = temp['Values']
        management_mode_battery_value = temp['Name']

        charging_percentage = setting['ChargingPercentage']
        discharging_percentage = setting['DischargingPercentage']

        high_voltage_disconnect = setting['HighVoltageDisconnect']
        high_voltage_reconnect = setting['HighVoltageReconnect']

        low_voltage_disconnect = setting['LowVoltageDisconnect']
        low_voltage_reconnect = setting['LowVoltageReconnect']

        equalization_voltage = setting['EqualizationVoltage']
        boost_voltage = setting['BoostVoltage']
        float_voltage = setting['FloatVoltage']

        charging_limit_voltage = setting['ChargingLimitVoltage']
        discharging_limit_voltage = setting['DischargingLimitVoltage']

        boost_reconnect_voltage = setting['BoostReconnectVoltage']
        under_voltage_recover = setting['UnderVoltageRecover']
        under_voltage_warning = setting['UnderVoltageWarning']

        boost_duration = setting['BoostDuration']
        equalize_duration = setting['EqualizeDuration']

        equalization_charging_cycle = setting['EqualizationChargingCycle']
        temperature_compensation_coefficient = setting['TemperatureCompensationCoefficient']

        return render_template('settings.html', **locals())

    except Exception as e:
        return e


@charge_settings.route('/settings', methods=['POST'])
@login_required
def post_settings():
    logger.info('post_settings()')

    if request.method == 'POST':

        print to_json(request.form)
        battery_capacity = request.form['battery_capacity']
        battery_type_value = request.form['battery_type_value']
        charging_percentage = request.form['charging_percentage']
        equalize_duration = request.form['equalize_duration']
        equalization_charging_cycle = request.form['equalization_charging_cycle']

        print battery_capacity
        print battery_type_value
        print charging_percentage
        print equalize_duration
        print equalization_charging_cycle

        battery_rated_voltage_value = request.form['battery_rated_voltage_value']
        management_mode_battery_value = request.form['management_mode_battery_value']
        discharging_percentage = request.form['discharging_percentage']
        boost_duration = request.form['boost_duration']
        temperature_compensation_coefficient = request.form['temperature_compensation_coefficient']

        print battery_rated_voltage_value
        print management_mode_battery_value
        print discharging_percentage
        print boost_duration
        print temperature_compensation_coefficient

    return get_settings()


def to_json(form):
    return {
        'battery_capacity': int(form['battery_capacity']),
        'battery_type_value': int(form['battery_type_value']),
        'charging_percentage': int(form['charging_percentage']),
        'equalize_duration': int(form['equalize_duration']),
        'equalization_charging_cycle': int(form['equalization_charging_cycle']),

        'battery_rated_voltage_value': int(form['battery_rated_voltage_value']),
        'management_mode_battery_value': int(form['management_mode_battery_value']),
        'discharging_percentage': int(form['discharging_percentage']),
        'boost_duration': int(form['boost_duration']),
        'temperature_compensation_coefficient': float(form['temperature_compensation_coefficient']),
    }