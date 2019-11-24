import os, docker, re, sys, subprocess, yaml, platform

from hpotter.env import logger
from hpotter.plugins import ssh, telnet
from hpotter.plugins.handler import Plugin

# # TODO: purge hpotter related containers before startup
# TODO:
class State():
    def __init__(self):
        self.client = docker.from_env()
        self.read_in_config()
        self.load_plugins(self.config[1])
        # self.load_images()
        # self.load_hpot_running_containers()

    def load_images(self):
        self.images = Set([])
        for plugin in self.available_plugins:
            i = self.client.images.get(plugin.container)
            if i not in images:
                self.images.add(i)

    def load_hpot_running_containers(self):
        self.running_containers = []
        for container in self.client.containers.list():
            for image in self.images:
                if container.image == image:
                    self.running_containers.append({'name': container.name, 'id': container.id})

    def start(self, name):
        for plugin in self.available_plugins:
            if plugin.container == name:
                self.run_container(plugin)
                break

    def stop(self, name=None):
        if name:
            self.remove_container(name)
        else:
            for active in self.running_containers:
                container = self.client.containers.get(active['id'])
                container.stop()
                container.remove()
                # logger.info("removed a %s container" % active['name'])
                print("removed a %s container" % active['name'])

    def run_container(self, plugin):
        c = plugin.run(self.client)
        info = {'name': c.name, 'id': c.id}
        self.running_containers.append(info)

    def remove_container(self, image):
        for active in self.running_containers:
            if active['name'] == image:
                container = self.client.containers.get(active['id'])
                container.stop()
                container.remove()
                # logger.info("removed a %s container" % image)
                self.running_containers.remove({'name': container.name, 'id': container.id})
                print("removed a %s container" % image)
                break

    def start_container_from_port(self, port):
        for plugin in self.available_plugins:
            if plugin.ports['connect_port'] == port:
                self.run_container(plugin)


    def get_container_instance(self, id):
        for container in self.running_containers:
            if container.id == id:
                return container
            else:
                return None

    def read_in_config(self):
        self.config = []
        with open('hpotter/plugins/config.yml') as file:
            for data in yaml.load_all(Loader=yaml.FullLoader, stream=file):
                for item in data:
                    self.config.append(data)

    def load_plugins(self, data):
        list = []
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
                list.append(p)
        self.available_plugins = list
