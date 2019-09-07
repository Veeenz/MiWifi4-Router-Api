from unittest import TestCase
from MiRouter import MiRouter
class MiRouterTest(TestCase):

    def setUp(self):
        self.api = MiRouter()
        self.api.login('adminadmin')

    def test_device_list(self):
        
        result = self.api.get_device_list()
        self.assertEqual(True, result['success'])
        self.assertGreater(len(result['data']), 0)

    def test_set_qos_status(self):
        status = 1
        result = self.api.set_qos_status(status)
        self.assertEqual('QoS status changed to {}'.format(status), result['message'])
        