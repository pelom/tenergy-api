from chargeEquipmentService import ChargeEquipmentService

from flask import Flask, jsonify, request

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s %(lineno)d %(levelname)s %(name)s] %(message)s')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

app = Flask(__name__)


@app.route("/chargecontroller/list")
def charge_controller_list():
    logger.info('charge_controller_list()')

    charge_equipment_service = ChargeEquipmentService()
    result_json = []
    charge_equip_list = charge_equipment_service.find_all()
    for charge in charge_equip_list:
        result_json.append(charge.to_json())
    return jsonify(result_json)


@app.route("/device", methods=['GET'])
def device():
    logger.info('device()')

    charge_port = request.headers.get('charge_port')
#   charge_port = request.args.get('port')

    charge_equipment_service = ChargeEquipmentService(charge_port)
    device = charge_equipment_service.device_info()
    return jsonify(device.to_json())


@app.route("/device/settings", methods=['GET'])
def device_settings():
    logger.info('device_settings()')

    charge_port = request.headers.get('charge_port')
    charge_equipment_service = ChargeEquipmentService(charge_port)
    setting = charge_equipment_service.device_setting()
    return jsonify(setting)


if __name__ == "__main__":
    app.run(debug=True)
