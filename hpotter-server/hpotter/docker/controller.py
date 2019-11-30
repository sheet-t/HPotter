import os, docker, re, sys, subprocess, yaml, platform

from hpotter.env import logger
from hpotter.plugins import ssh, telnet
from hpotter.plugins.handler import Plugin, remove_certs

class State():
    def __init__(self):
        check_docker()
        self.client = docker.from_env()
        self.clear_network('network_1')
        self.start_network(name="network_1", ipr='10.3.3.0')
        self.read_in_config()

    def clear_network(self, name):
        for network in self.client.networks.list():
            if network.name == name:
                if network.containers != []:
                    for container in network.containers:
                        container.kill()
                        logger.info("removed container: %s" % container.id)
                network.remove()
                logger.info("removed existing network")
                break

    def start_network(self, name=None, ipr=None, gate=None):
        ipam_pool = docker.types.IPAMPool(
            subnet = ipr + '/24',
            iprange = ipr + '/24',
            #leave gateway empty when constructing a network on localhost
            gateway = gate,
            aux_addresses = None
        )
        ipam_config = docker.types.IPAMConfig (
                pool_configs=[ipam_pool]
        )
        logger.info("Network: %s created", name)

        self.network = self.client.networks.create (
                name=name,
                driver="bridge",
                ipam=ipam_config
        )

    def read_in_config(self):
        config = []
        with open('hpotter/plugins/config.yml') as file:
            for data in yaml.load_all(Loader=yaml.FullLoader, stream=file):
                if data:
                    for item in data:
                        for k, v in item.items():
                            config.append(v)

        self.load_services(config[0])
        self.load_plugins(config[1])

    def load_services(self, data):
        for service in data:
            for k, v in service.items():
                if k == 'ssh':
                    self.ssh = ssh.start_server(v['address'], v['port'])
                elif k == 'telnet':
                    self.telnet = telnet.start_server(v['address'], v['port'])

    def load_plugins(self, data):
        self.available_plugins = []
        for plugins in data:
            for k, v in plugins.items():
                p = Plugin(name=k, setup=v['setup'], \
                          teardown=v['teardown'], container=v['container'], \
                          alt_container=v['alt_container'], \
                          read_only=v['read_only'], detach=v['detach'], \
                          ports=v['ports'], tls=v['tls'],\
                          volumes=v['volumes'], \
                          environment=v['environment'], \
                          listen_address=v['listen_address'], \
                          listen_port=v['listen_port'], table=v['table'], \
                          capture_length=v['capture_length'], request_type=v['request_type'])
                self.available_plugins.append(p)

    def start_plugin(self, name=None, port=None):
        for plugin in self.available_plugins:
            if port != None:
                if plugin.listen_port == port:
                    c = plugin.add_instance(self.client, self.network)
                    self.running_containers.append(c.id)
                    break
            elif name != None:
                if plugin.container == name:
                    c = plugin.add_instance(self.client, self.network)
                    self.running_containers.append(c.id)
                    break

    def stop_plugin(self, name):
        for plugin in self.available_plugins:
            if plugin.name == name:
                plugin.remove_instance(self.client, self.network)

    def stop_services(self):
        self.ssh.stop()
        self.telnet.stop()

def start_hpotter():
    global hpotter_state
    hpotter_state = State()

    for plugin in hpotter_state.available_plugins:
        plugin.add_instance(hpotter_state.client, hpotter_state.network)

    return hpotter_state

def stop_hpotter():
    ssh.stop_server()
    telnet.stop_server()
    remove_certs()

    for plugin in hpotter_state.available_plugins:
        plugin.remove_instance(hpotter_state.client, hpotter_state.network)

    hpotter_state.network.remove()

def check_docker():
    try:
        s = subprocess.check_output('docker ps', shell=True)
    except subprocess.CalledProcessError:
        print("Ensure Docker is running, and please try again.")
        sys.exit()
