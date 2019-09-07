from util import get_random_mac, get_nonce, get_password_hash, success, fail
import requests



class MiRouter():

    def __init__(self, gateway_url="http://miwifi.com"):
        self.mac_prefix = "e4:46:da"
        self.login_token = ""
        self.gateway_url = gateway_url
        self.random_mac_address = get_random_mac(self.mac_prefix)
        self.nonce = get_nonce(self.random_mac_address)
        self.endpoint_url = "{}/cgi-bin/luci/;stok={}/"
        
    def login(self, psw):
        
        url = "{}/cgi-bin/luci/api/xqsystem/login".format(self.gateway_url)
        req = requests.post(url, {
            "username": "admin",
            "password": get_password_hash(self.nonce, psw),
            "logtype": 2,
            "nonce": self.nonce
        })
        
        if(req.status_code == 200):
            self.login_token = req.json()['token']
            self.endpoint_url = "{}/cgi-bin/luci/;stok={}/".format(self.gateway_url, self.login_token)
            return success(message="Logged in!", data=req.json())
        return fail(message="There was an error while logging in...", data=req.content)

    def get_device_list(self):
        req = requests.get(self.endpoint_url + "/api/misystem/devicelist")
        if(req.status_code == 200):
            return success(message="Device list retrieved!",data=req.json())
        return fail(message="There was an error while getting device list...", data=req.content)
    

    def get_wifi_detail(self):        
        req = requests.get(self.endpoint_url + "/api/xqnetwork/wifi_detail_all")
        if(req.status_code == 200):
            data = req.json()            
            #Setting a ref to "wifiIndex" which can be used for setting the wifi status in the set_wifi method
            for i, wifi_interface in enumerate(data['info']):
                wifi_interface['wifiIndex'] = i + 1 
            return success(message="Wifi interfaces retrieved!", data=data)
                
        return fail(message="There was an error while getting the Wifi details...", data=req.content)
    
    def get_qos_detail(self):
        req = requests.get(self.endpoint_url + "/api/misystem/qos_info")
        if(req.status_code == 200):
            return success(message="QoS info retrieved!", data=req.json())
        return fail(message="There was an error while getting the QoS details...", data=req.content)

    def set_wifi_status(self, wifi_index: int, status=0):
        """ Set the wifi status of a given interface to 0 or 1
        Keyword arguments:
        wifi_index -- Index of interface we want to change the status
        status -- The status of the WiFi interface (default 0)
        """
        if(status != 0 and status != 1):            
            return fail('Invalid status, send 0 for disable, 1 for enable')
        
        wifi_interfaces = self.get_wifi_detail()['data']        
        target_interface = [interface for interface in wifi_interfaces['info'] if interface['wifiIndex'] == wifi_index]
        if len(target_interface) > 0:
            target_interface = target_interface[0]
        else:
            return fail('Target Wifi interface not found')
        payload = {
            'wifiIndex': target_interface['wifiIndex'],
            'on': status,
            'ssid': target_interface['ssid'],
            'pwd': target_interface['password'],
            'encryption': target_interface['encryption'],
            'channel': target_interface['channel'],
            'bandwidth': target_interface['bandwidth'],
            'hidden': target_interface['hidden'],
            'txpwr': target_interface['txpwr']
        }

        req = requests.post(self.endpoint_url + "/api/xqnetwork/set_wifi", payload)
        if(req.status_code == 200):
            return success('Setting the status of WiFi to {}'.format(status), data=req.json())
        return fail('There was an error while setting the status of WiFi to {}'.format(status), data=req.content)

    def set_qos_status(self, status=0):
        if(status != 0 and status != 1):
            return fail('Invalid status, send 0 for disable, 1 for enable')
        req = requests.get(self.endpoint_url + '/api/misystem/qos_switch?on={}'.format(status))
        if(req.status_code == 200):
            return success('QoS status changed to {}'.format(status))
        return fail('There was an error while setting the status of QoS to {}'.format(status))

    def set_qos_band_limit(self, download=-1, upload=-1):
        if(download < 0 and upload < 0):
            return fail("Please send me valid download and/or upload")
        payload = {"manual":1}
        if(download >= 0):
            payload['download'] = download
        if(upload >= 0):
            payload['upload'] = upload
        req = requests.post(self.endpoint_url + "/api/misystem/set_band", payload)
        if(req.status_code == 200 and req.json()['code'] == 0):
            return success("QoS limits have been set!", data=req.json())
        return fail("There was an error while setting the bandwidth")
        

        
    

