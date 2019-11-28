import unittest
import docker
import platform
import subprocess

from hpotter.plugins.handler import *
from hpotter.plugins.telnet import *
from hpotter.env import logger, stop_shell, close_db

client = docker.from_env()
lock = threading.Lock()

class TestHandler(unittest.TestCase):
    def setUp(self):
        subprocess.call('docker ps -a | xargs -n 1 docker stop', stdin=None, stdout=None, stderr=None, shell=True)
        subprocess.call('docker ps -a | xargs -n 1 docker rm', stdin=None, stdout=None, stderr=None, shell=True)

    def tearDown(self):
        stop_shell()
        close_db()
        stop_server()
        subprocess.call('docker ps -a | xargs -n 1 docker stop', stdin=None, stdout=None, stderr=None, shell=True)
        subprocess.call('docker ps -a | xargs -n 1 docker rm', stdin=None, stdout=None, stderr=None, shell=True)
    
    def test_start_and_stop_network(self):
        n = len(client.networks.list())
        start_network("test","10.3.3.0")
        n += 1
        self.assertEqual(len(client.networks.list()), n)
        stop_network()
        n -= 1
        self.assertEqual(len(client.networks.list()), n)
        
    def test_start_and_stop_plugins(self):
        start_plugins()
        test = client.containers.list()
        self.assertTrue(test)
        stop_plugins()
        test = client.containers.list()
        self.assertFalse(test)

    def test_read_in_config(self):
        test = read_in_config()
        self.assertIsNotNone(test)
