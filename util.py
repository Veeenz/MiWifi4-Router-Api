import hashlib
import random
import time
import json

from Exceptions import *

KEY = "a2ffa5c9be07488bbb04a3a47d3c5f6a" #Stands for xiaoqiang

def sha1(string):
    return hashlib.sha1(string.encode()).hexdigest()

def get_random_mac(prefix):
    return prefix+':'.join("%02x"%random.randint(0, 255) for _ in range(3))


def get_nonce(mac_address):
    return "0_{}_{}_9999".format(mac_address, int(time.time()), )

def get_password_hash(nonce, psw):
    return sha1(nonce + sha1(psw + KEY))

def success(message, data=[]):
    return {
        'success': True,
        'message': message,
        'data': data
    }

def fail(message, data=[]):
    return {
        'success': False,
        'message': message,
        'data': data
    }

def log(message, file=False, filename='log.json', mode='a+'): 
    if(file):
        with open(filename, mode) as target:
            json.dump(message, target)
    
    print(message)
