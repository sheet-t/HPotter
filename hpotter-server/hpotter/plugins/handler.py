import os
import platform
import docker
import re
import sys
import subprocess
import yaml
from OpenSSL import crypto

from hpotter.env import logger
from hpotter.plugins.generic import PipeThread
from hpotter.plugins import ssh, telnet

global set_cert
set_cert = False

class Singletons():
    active_plugins = {}

class Plugin(yaml.YAMLObject):
    yaml_tag = u'!plugin'

    def __init__(self, name=None, setup=None, teardown=None, container=None, alt_container=None, read_only=None, detach=None, ports=None, tls=None, volumes=None, environment=None, listen_address=None, listen_port=None, table=None, capture_length=None, request_type=None, cert=None):
        self.name = name
        self.setup = setup
        self.teardown = teardown
        self.container = container
        self.alt_container = alt_container
        self.read_only = read_only
        self.detach = detach
        self.ports = ports
        self.tls = tls
        self.volumes = volumes
        self.environment = environment
        self.listen_address = listen_address
        self.listen_port = listen_port
        self.table = table
        self.capture_length = capture_length
        self.request_type = request_type
        self.cert = cert

    def __repr__(self):
        return "%s( name: %r \n setup: %r \n teardown: %r \n container: %r\n read_only: %r\n detach: %r\n ports: %r \n tls: %r \n volumes: %r \n environment: %r \n listen_address: %r \n listen_port: %r \n table: %r \n capture_length: %r \n request_type: %r cert: %r \n)" % (
            self.__class__.__name__, self.name, self.setup,
            self.teardown, self.container, self.read_only, self.detach,
            self.ports, self.tls, self.volumes, self.environment, self.listen_address,
            self.listen_port, self.table, self.capture_length, self.request_type, self.cert)

    def contains_volumes(self):
        return self.volumes == []

    def makeports(self):
        return {self.ports["from"] : self.ports["connect_port"]}

    @staticmethod
    def read_in_plugins(container_name):
        present = False
        with open('hpotter/plugins/config.yml') as file:
            for data in yaml.load_all(Loader=yaml.FullLoader, stream=file):
                if (data["name"] == container_name):
                    present = True
                    return Plugin(name=data['name'],
                                  setup=data['setup'],
                                  teardown=data['teardown'],
                                  container=data['container'],
                                  alt_container=data['alt_container'],
                                  read_only=data['read_only'],
                                  detach=data['detach'],
                                  ports=data['ports'],
                                  tls=data['tls'],
                                  volumes=data['volumes'],
                                  environment=data['environment'],
                                  listen_address=data['listen_address'],
                                  listen_port=data['listen_port'],
                                  table=data['table'],
                                  capture_length=data['capture_length'], request_type=data['request_type'],
                                  cert=data['cert'])
            if (present == None):
                print("plugin definintion not present")

    @staticmethod
    def read_in_all_plugins():
        plugins = []
        with open('hpotter/plugins/config.yml') as file:
            for data in yaml.load_all(Loader=yaml.FullLoader, stream=file):
                p = Plugin(name=data['name'], setup=data['setup'],
                           teardown=data['teardown'], container=data['container'],
                           alt_container=data['alt_container'],
                           read_only=data['read_only'], detach=data['detach'],
                           ports=data['ports'], tls=data['tls'],
                           volumes=data['volumes'],
                           environment=data['environment'],
                           listen_address=data['listen_address'],
                           listen_port=data['listen_port'], table=data['table'],
                           capture_length=data['capture_length'], request_type=data['request_type'],
                           cert=data['cert'])
                plugins.append(p)
        return plugins


def start_plugins():
    # ensure Docker is running
    try:
        s = subprocess.check_output('docker ps', shell=True)
    except subprocess.CalledProcessError:
        print("Ensure Docker is running, and please try again.")
        sys.exit()

    ssh.start_server()
    telnet.start_server()

    all_plugins = Plugin.read_in_all_plugins()
    current_thread = None
    current_container = None
    for plugin in all_plugins:
        if plugin is not None:
            try:

                check_certs(plugin.cert)
                client = docker.from_env()

                container = plugin.container
                if platform.machine() == 'armv6l':
                    container = plugin.alt_container

                try:
                    for cmd in plugin.setup['mkdir']:
                        logger.info("%s created the %s directory",
                                    plugin.name, cmd)
                        os.mkdir(cmd)
                except FileExistsError:
                    pass
                except OSError as error:
                    logger.info(error)
                    return

                if (plugin.volumes):
                    current_container = client.containers.run(container, \
                        detach=plugin.detach, ports=plugin.makeports(), \
                        environment=[plugin.environment])

                else:
                    current_container = client.containers.run(container, \
                        detach=plugin.detach, ports=plugin.makeports(), \
                        read_only=True)

                logger.info('Created: %s', plugin.name)

            except OSError as err:

                logger.info(err)
                if current_container:
                    logger.info(current_container.logs())
                    rm_container()
                return

            def di(a): return re.sub(b'([\x00-\x20]|[\x7f-xff])+', b' ', a)

            current_thread = PipeThread((plugin.listen_address, \
                plugin.listen_port), (plugin.ports['connect_address'], \
                plugin.ports['connect_port']), plugin.table, \
                plugin.capture_length, request_type=plugin.request_type, tls=plugin.tls)

            current_thread.start()
            p_dict = {
                "plugin": plugin,
                "container": current_container,
                "thread": current_thread
            }
            Singletons.active_plugins[plugin.name] = p_dict
        else:
            logger.info(
                "yaml configuration seems to be missing some important information")


def stop_plugins():
    ssh.stop_server()
    telnet.stop_server()
    remove_certs()

    for name, item in Singletons.active_plugins.items():
        try:
            for cmd in item["plugin"].teardown['rmdir']:
                logger.info("---%s is removing the %s directory", name, cmd)
                os.rmdir(cmd)
        except FileExistsError:
            pass
        except FileNotFoundError:
            pass
        except OSError as error:
            logger.info(name + ": " + str(error))
            return

        if item["container"] is not None:
            item["thread"].request_shutdown()
        logger.info("--- removing %s container", item["plugin"].name)
        item["container"].stop()
        logger.info("--- %s container removed", item["plugin"].name)

def check_platform():
    if platform.system() == 'Linux' or 'Darwin':
        return '/tmp/cert.pem'
    elif platform.system() == 'Windows':
        return "C:/tmp/cert.pem"
    

def check_certs(yml_cert):
    tmp_file = check_platform()
    if yml_cert != 'None':
        if not os.path.isfile(tmp_file):
            create_tls_cert_and_key(tmp_file)


def remove_certs():
    tmp_file = check_platform()
    try:
        if set_cert:
            os.remove(tmp_file)
            logger.info("removing TLS cert and key")
    except:
        raise FileNotFoundError
        

def create_tls_cert_and_key(tmp_file):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 4096)

    req = crypto.X509Req()
    subject = req.get_subject()
    subject.O = 'org'
    subject.OU = 'orgUnit'
    req.set_pubkey(key)
    req.sign(key, "sha256")

    cert = crypto.X509()
    cert.set_serial_number(1)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(31536000)  # one year
    cert.set_issuer(req.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(key, "sha256")

    logger.info("Created: TLS cert and key")
    with open(tmp_file, "w") as tmp_cert_file:
        tmp_cert_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode("utf-8"))
        tmp_cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    global set_cert
    set_cert = True
