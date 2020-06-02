from flask import Flask, jsonify
from flask_cors import CORS
from MiRouter import *
import util
import threading
import storage
from Exceptions import LoginError
from Device import *

global api
api = MiRouter('192.168.31.1')
app = Flask(__name__)
CORS(app)
POLLING_TIME = 4


def get_data():
    while 1:
        data = api.get_qos_detail()
        devices = data['data']['list']
        for device in devices:
            device_object = Device()
            device_object.from_response(device)

        time.sleep(POLLING_TIME)

@app.route("/login")
def login():
    global api
    result = api.login('adminadmin')
    
    if(result['success']):
        return success('Login successfully')
    return fail('Login failed')

@app.route("/details")
def details():
    global api
    if(api.login_token is None):
        raise LoginError
    data = api.get_qos_detail()
    devices = data['data']['list']
    devs = []
    
    for device in devices:
        util.log(device, file=True, mode='w+')
        device_object = Device()
        device_object.from_response(device)
        """storage.save_device_detail(device_object)
        stored_device = storage.get_by("mac", device_object.mac)
                
        device_object.details = stored_device['data']['details']"""
            
        devs.append(device_object.to_dict())
    devs = sorted(devs, reverse = True, key = lambda i: (i['statistics']['downspeed'])) 
    return jsonify(devs)

@app.route("/details/<mac>")
def detail(mac):
    global api
    if(api.login_token is None):
        raise LoginError
    device = storage.get_by("mac", mac)
    return jsonify(device)

app.run(debug=True, host='0.0.0.0')