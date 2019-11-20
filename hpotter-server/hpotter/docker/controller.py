import os, docker, re, sys, subprocess, yaml, platform

from hpotter.env import logger
from hpotter.plugins import ssh, telnet
from hpotter.plugins.handler import Plugin, read_in_config, parse_plugins

<<<<<<< HEAD
# # TODO: purge hpotter related containers before startup
# TODO:

MDB = docker.from_env().images.get('mariadb')
HTTPD = docker.from_env().images.get('httpd:latest')
=======
>>>>>>> 69a8424a80e468c251a118a18e2b44b6276e1519

class State():
    def __init__(self):
        self.client = docker.from_env()
        self.config = read_in_config()
        self.available_plugins = parse_plugins(self.config[1])
        self.images = self.get_images()
        self.load_hpot_running_containers()

    def get_images(self):
        image_names = []
        images = []
        for plugin in self.available_plugins:
            if image_names:
                for name in image_names:
                    if not name == plugin.container:
                        image_names.append(plugin.container)
            else:
                image_names.append(plugin.container)

        for name in image_names:
            images.append(self.client.images.get(name))

        return images

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
