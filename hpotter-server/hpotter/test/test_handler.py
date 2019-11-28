import unittest
import docker
import sys
import os
import platform
import subprocess
import tempfile

from unittest.mock import MagicMock
from hpotter.plugins.handler import *
from hpotter.plugins.telnet import stop_server
from hpotter.env import logger, stop_shell, close_db

client = docker.from_env()
lock = threading.Lock()

class TestHandler(unittest.TestCase):
    def tearDown(self):
        stop_shell()
        close_db()
        stop_server()
        subprocess.call('docker ps -a | xargs -n 1 docker stop', stdin=None, stdout=None, stderr=None, shell=True)
        subprocess.call('docker ps -a | xargs -n 1 docker rm', stdin=None, stdout=None, stderr=None, shell=True)
    
    def test_start_and_stop_network(self):
        n = len(client.networks.list())
        start_network("test","10.3.3.0")
        self.assertGreater(len(client.networks.list()), n)
        stop_network()
        self.assertEqual(len(client.networks.list()), n)
        
    def test_start_and_stop_plugins(self):
        start_plugins()
        test = client.containers.list()
        self.assertTrue(test)
        stop_plugins()
        test = client.containers.list()
        self.assertFalse(test)
    
    def test_check_platform(self):
        if sys.platform == 'win32':
            self.assertEqual(check_platform(), "temp\\cert.pem")
        else:
            self.assertEqual(check_platform(), "/tmp/cert.pem")

    def test_create_tls_cert_and_key(self):
        create_tls_cert_and_key(MagicMock())
        self.assertTrue(os.path.exists("hpotter/test/cert.pem"))

    def test_read_in_config(self):
        test = read_in_config()
        self.assertIsNotNone(test)
