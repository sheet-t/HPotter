import unittest
import docker
import platform
import subprocess

from hpotter.plugins.handler import *

client = docker.from_env()

class TestPluginHandler(unittest.TestCase):

    def check_platform(self):
        if platform.system() == 'Linux' or platform.system() == 'Darwin':
            check = '/tmp/cert.pem'
        elif platform.system() == 'Windows':
            # os.mkdir('temp')
            check = "temp\\cert.pem"

        self.assertTrue(check, check_platform())
