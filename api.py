from flask import Flask, jsonify
from flask_cors import CORS
from MiRouter import *
import util
import threading
import storage
from Device import *

global api
api = MiRouter()
api.login('adminadmin')
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

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/login")
def login():
    global api
    api.login('adminadmin')
    return jsonify({'success': True})

@app.route("/details")
def details():
    global api
    data = api.get_qos_detail()
    devices = data['data']['list']
    devs = []
    
    for device in devices:
        util.log(device, file=True, mode='w+')
        device_object = Device()
        device_object.from_response(device)
        storage.save_device_detail(device_object)
        stored_device = storage.get_by("mac", device_object.mac)
                
        device_object.details = stored_device['data']['details']
            
        devs.append(device_object.to_dict())
    devs = sorted(devs, reverse = True, key = lambda i: (i['statistics']['downspeed'])) 
    return jsonify(devs)

@app.route("/details/<mac>")
def detail(mac):
    device = storage.get_by("mac", mac)
    return jsonify(device)
app.run(debug=True)