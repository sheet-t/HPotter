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
        subprocess.call('docker stop $(docker ps -aq)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call('docker rm $(docker ps -a -q)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def tearDown(self):
    #    subprocess.check_call('docker stop $(docker ps -aq)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #stop_plugins()
        stop_shell()
        close_db()
        stop_server()
        subprocess.check_call('docker system prune -f', shell=True)
    
    def test_start_network(self):
        n = len(client.networks.list())
        start_network("test")
        n += 1
        self.assertEqual(len(client.networks.list()), n)
        stop_network()
        
    def test_stop_network(self):
        start_network("test1")
        n = len(client.networks.list())
        stop_network()
        n -= 1
        self.assertEqual(len(client.networks.list()), n)
   
    def test_start_plugins(self):
        start_plugins()
        test = client.containers.list()
        self.assertTrue(test)
        #stop_plugins()

    def test_stop_plugins(self):
        #start_plugins()
        stop_plugins()
        test = client.containers.list()
        self.assertFalse(test)
        #subprocess.call('docker stop $(docker ps -aq)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #subprocess.call('docker rm $(docker ps -a -q)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_read_in_config(self):
        test = read_in_config()
        self.assertIsNotNone(test)
