from pymongo import MongoClient
import util
import time

client = MongoClient()
db = client.mirouter

def save_device_detail(device):
    devices = [device for device in db.devices.find()]
    if(device.mac in [d['mac'] for d in devices]):
        query = {"mac": device.mac}
        device_mongo = device.statistics
        device_mongo['time'] = time.time()
        dev = db.devices.update_one(query, {"$push": { "details": device.statistics}})
        # dev = db.devices.find_one(query)
        # print(dev)
        return util.success('Device pushed')
    else:
        device_mongo = device.to_dict()
        device_mongo['details'] = []
        insert = db.devices.insert_one(device_mongo)
        if(insert):
            print(insert)
            return util.success('Device added successfully')
        else:
            return util.fail('Cannot add device')


def get_by(key, value):
    device = db.devices.find_one({key: value}, {'details': {"$slice": -10}})
    if(device):
        del device["_id"]
        return util.success("Entity found", device)
    else:
        return util.fail("Entity not found")