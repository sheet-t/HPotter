import os, docker, re, sys, subprocess, yaml, platform

from hpotter.env import logger
from hpotter.plugins import ssh, telnet
from hpotter.plugins.handler import Plugin, remove_certs


def start_network(client, name=None, ipr=None, gate=None):
    ipam_pool = docker.types.IPAMPool(
        subnet = ipr + '/24',
        iprange = ipr + '/24',
        #leave gateway empty when constructing a network on localhost
        aux_addresses = None
    )
    ipam_config = docker.types.IPAMConfig (
            pool_configs=[ipam_pool]
    )
    logger.info("Network: %s created", name)

    return client.networks.create (
            name=name,
            driver="bridge",
            ipam=ipam_config
    )

def read_in_config():
    # would like a way to remove this from being global, but we cannot pass a list
    # to the shutdown_hpotter method the way it stands
    global available_plugins
    config = []
    with open('hpotter/plugins/config.yml') as file:
        for data in yaml.load_all(Loader=yaml.FullLoader, stream=file):
            if data:
                for item in data:
                    for k, v in item.items():
                        config.append(v)

    net = load_network(config[0])
    load_services(config[1])
    available_plugins = load_plugins(config[2])
    return net

def load_network(data):
    # would like a way to remove this from being global, but we cannot pass a list
    # to the shutdown_hpotter method the way it stands
    global name
    client = docker.from_env()
    (n, name), (i, ipr), (g, gate) = data.items()
    logger.info('Network info: name= %s   ip-range= %s   gate= %s' % (name, ipr, gate))
    clear_network(client, name)
    if gate:
        return start_network(client, name, ipr, gate)
    else:
        return start_network(client, name, ipr)

def load_services(data):
    for service in data:
        for k, v in service.items():
            if k == 'ssh':
                ssh.start_server(v['address'], v['port'])
            elif k == 'telnet':
                telnet.start_server(v['address'], v['port'])

def load_plugins(data):
    available_plugins = []
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
            available_plugins.append(p)
    return available_plugins

def start_plugin(client, available_plugins, network, name=None, port=None,):
    running_containers = []
    for plugin in available_plugins:
        if port != None:
            if plugin.listen_port == port:
                c = plugin.add_instance(client, network)
        elif name != None:
            if plugin.container == name:
                c = plugin.add_instance(client, network)

def stop_plugin(self, name, available_plugins, client, network):
    for plugin in available_plugins:
        if plugin.name == name:
            plugin.remove_instance(client, network)

def stop_services(self):
    ssh.stop()
    telnet.stop()

def startup_hpotter():
    check_docker()
    client = docker.from_env()
    network = read_in_config()

    for plugin in available_plugins:
        plugin.add_instance(client, network)

def shutdown_hpotter():
    client = docker.from_env()
    network = client.networks.get(name)
    ssh.stop_server()
    telnet.stop_server()

    for plugin in available_plugins:
        plugin.remove_instance(client, network)

def check_docker():
    try:
        s = subprocess.check_output('docker ps', shell=True)
    except subprocess.CalledProcessError:
        print("Ensure Docker is running, and please try again.")
        sys.exit()

def clear_network(client, name):
    try:
        net = client.networks.get(name)

        for container in net.containers:
            net.disconnect(container)
            container.stop()
            container.remove()
            logger.info("removed container %s" % container.id)

        net.remove()

    except docker.errors.NotFound:
        logger.info('no %s network exists' % name)

    except Exception as exc:
        logger.info(type(exc))
        logger.info(exc)
