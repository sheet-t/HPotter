import unittest
import docker
import platform
import subprocess

from hpotter.plugins.handler import *

client = docker.from_env()

class TestHandler(unittest.TestCase):
    def test_start_network(self):
        n = len(client.networks.list())
        start_network("test")
        n += 1
        self.assertEqual(len(client.networks.list()), n)
        
    def test_stop_network(self):
        n = len(client.networks.list())
        stop_network()
        n -= 1
        self.assertEqual(len(client.networks.list()), n)
   
    def test_start_plugins(self):
        start_plugins()
        test = client.containers.list()
        self.assertTrue(test)

    def test_stop_plugins(self):
        stop_plugins()
        test = client.containers.list()
        self.assertFalse(test)
        subprocess.call('docker stop $(docker ps -aq)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call('docker rm $(docker ps -a -q)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_read_in_config(self):
        test = read_in_config()
        self.assertIsNotNone(test)
