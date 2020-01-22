import unittest
import ipaddress
from hpotter.env import getLocalRemote

class TestEnv (unittest.TestCase):
    def test_localRemote(self):
        
        #Don't know if I should relabel the outputs from getLocalRemote to Private and Global instead
        
        self.assertEqual(getLocalRemote(ipaddress.ip_address('103.11.49.181')), "Remote")
        self.assertEqual(getLocalRemote(ipaddress.ip_address('67.174.103.180')), "Remote")
        self.assertEqual(getLocalRemote(ipaddress.ip_address('127.0.0.1')), "Local")
        self.assertEqual(getLocalRemote(ipaddress.ip_address('123.207.40.81')), "Remote")
        self.assertEqual(getLocalRemote(ipaddress.ip_address('192.168.1.2')), "Local")

if __name__ == '__main__':
    unittest.main()