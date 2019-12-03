import unittest, docker
from hpotter.docker.controller import *
class TestController(unittest.TestCase):

    def testStartNetwork(self):
        test_client = docker.from_env()
        start_network(test_client, name='test_network', ipr='10.0.0.0')

        check = test_client.networks.get('test_network')
        self.assertTrue(check != None)

        check.remove()

    def testClearNetwork(self):
        test_client = docker.from_env()
        init_nets = test_client.networks.list()
        test_net = test_client.networks.create(name='test_network', driver='bridge')
        test_cont = test_client.containers.run('httpd:latest', detach=True)
        test_net.connect(test_cont)
        after_nets = test_client.networks.list()

        self.assertTrue(len(after_nets) > len(init_nets))

        clear_network(test_client, 'test_network')

        final_nets = test_client.networks.list()

        self.assertEqual(len(final_nets), len(init_nets))

    def testStartupHpotter(self):
        test_client = docker.from_env()
        startup_hpotter()

        net = test_client.networks.get('hpotter')
        self.assertTrue(net != None)

        containers = net.containers

        # should only spinup 4 containers
        self.assertTrue(len(containers) == 4)

        self.assertTrue(ssh != None)
        self.assertTrue(telnet != None)

    def testStopHpotter(self):
        shutdown_hpotter()
        test_client = docker.from_env()

        for net in test_client.networks.list():
            self.assertFalse(net.name == 'hpotter')
