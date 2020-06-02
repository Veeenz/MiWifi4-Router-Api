class Device(object):

    def __init__(self):
        self.statistics = {
            'downspeed': 0,
            'upspeed': 0
        }
        self.qos = {
            'downspeed': 0,
            'upspeed': 0
        }

        self.details = []

    def from_response(self, response_device):
        self.ip = response_device['ip']
        self.hostname = response_device['name']
        self.mac = response_device['mac']
        
        self.statistics['downspeed'] = response_device['statistics']['downspeed']
        self.statistics['upspeed'] = response_device['statistics']['upspeed']
        self.qos['downspeed'] = response_device['qos']['downmax']
        self.qos['upspeed'] = response_device['qos']['upmax']
    
    


    def to_dict(self):
        return {
            'ip': self.ip,
            'mac': self.mac,
            'hostname': self.hostname,
            'statistics': {
                'downspeed': self.statistics['downspeed'],
                'upspeed': self.statistics['upspeed']
            },
            'qos': {
                'downspeed': self.qos['downspeed'],
                'upspeed': self.qos['upspeed']
            },
            'details': self.details
        }