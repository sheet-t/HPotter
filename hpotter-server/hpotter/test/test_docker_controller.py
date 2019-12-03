import unittest, docker
from hpotter.docker.controller import State, stop_hpotter, start_hpotter, clear_network

class TestController(unittest.TestCase):

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

    def testStartHpotter(self):
        state = start_hpotter()
        test_client = docker.from_env()
        self.assertTrue(state.client != None)

        net = test_client.networks.get('network_1')
        self.assertEqual(state.network, net)

        self.assertEqual(len(net.containers), len(state.available_plugins))

        self.assertTrue(state.ssh != None)
        self.assertTrue(state.telnet != None)

    def testStopHpotter(self):
        stop_hpotter()
        test_client = docker.from_env()

        for net in test_client.networks.list():
            self.assertTrue(net.name != 'network_1')
