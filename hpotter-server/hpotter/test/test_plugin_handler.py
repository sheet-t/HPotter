import unittest
import docker
import platform
import subprocess

from hpotter.plugins.handler import *

client = docker.from_env()

class TestPluginHandler(unittest.TestCase):
    def test_start_server(self):
        self.assertFalse(Singletons.active_plugins)
        start_plugins()
        test = Singletons.active_plugins
        self.assertTrue(test)

    def test_stop_server(self):
        stop_plugins()
        test = Singletons.active_plugins
        self.assertFalse(test)
        subprocess.call('docker stop $(docker ps -q)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call('docker rm $(docker ps -a -q)', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_read_in_config(self):
        test = read_in_config()
        self.assertIsNotNone(test)
