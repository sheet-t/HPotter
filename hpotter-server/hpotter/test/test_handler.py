import unittest
import docker
import sys
import os
import platform
import subprocess
import tempfile
import socket

from unittest.mock import Mock, MagicMock
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
        #for windows
        #subprocess.call('docker ps -a | xargs -n 1 docker stop', stdin=None, stdout=None, stderr=None, shell=True)
        #subprocess.call('docker ps -a | xargs -n 1 docker rm', stdin=None, stdout=None, stderr=None, shell=True)

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
        path = "hpotter/test/cert.pem"
        create_tls_cert_and_key(path)
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_check_certs(self):
        mock = Mock()
        check_certs(mock)
        self.assertTrue(os.path.exists("/tmp/cert.pem"))

    def test_remove_certs(self):
        remove_certs()
        self.assertFalse(os.path.exists("/tmp/cert.pem"))

    def test_start_services(self):
        #need to come up with a way to test this
        service_config = [Service("ssh","0.0.0.0",22)]
        start_services(service_config)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.assertEqual(s.connect_ex(('0.0.0.0', 22)),0)

    def test_read_in_config(self):
        test = read_in_config()
        self.assertIsNotNone(test)

    def test_parse_services(self):
        data = MagicMock()
        self.assertIsNotNone(parse_services(data))

    def test_parse_plugins(self):
        data = MagicMock()
        self.assertIsNotNone(parse_plugins(data))
