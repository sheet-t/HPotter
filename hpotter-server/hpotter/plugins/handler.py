import os
import platform
import docker
import re
import sys
import subprocess
import yaml
import threading
from OpenSSL import crypto

from hpotter.env import logger
from hpotter.plugins.generic import PipeThread

global set_cert
set_cert = False

class Plugin:
    def __init__(self, name=None, setup=None, teardown=None, container=None, \
                   alt_container=None, read_only=None, detach=None, \
                   ports=None, tls=None, volumes=None, environment=None, \
                   listen_address=None, listen_port=None, table=None, \
                   capture_length=None, request_type=None, cert=None):
        self.total_active = 0
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
        self.instances = []

    def __repr__(self):
        return "%s( name: %r \n setup: %r \n teardown: %r \n container: %r\n read_only: %r\n detach: %r\n ports: %r \n tls: %r \n volumes: %r \n environment: %r \n listen_address: %r \n listen_port: %r \n table: %r \n capture_length: %r \n request_type: %r cert: %r \n)" % (
            self.__class__.__name__, self.name, self.setup,
            self.teardown, self.container, self.read_only, self.detach,
            self.ports, self.tls, self.volumes, self.environment, self.listen_address,
            self.listen_port, self.table, self.capture_length, self.request_type, self.cert)

    def makeports(self):
        return {self.ports["from"] : self.ports["connect_port"]}

    def connect_to_hpotter(self):
        thread = PipeThread((self.listen_address, \
            self.listen_port), (self.ports['connect_address'], \
            self.ports['connect_port']), self.table, \
            self.capture_length, request_type=self.request_type, tls=self.tls)
        thread.start()
        return thread

    def create_support_file_structure(self):
        try:
            for cmd in self.setup:
                os.mkdir(cmd)
                logger.info("%s created the %s directory",
                            self.name, cmd)
        except FileExistsError:
            logger.info("temp directory %s already exists", self.name)
            pass
        except OSError as error:
            logger.info(error)
            return

    def remove_support_file_structure(self):
        try:
            for cmd in self.teardown:
                logger.info("%s is removing the %s directory", self.name, cmd)
                os.rmdir(cmd)
        except FileExistsError:
            pass
        except FileNotFoundError:
            pass
        except OSError as error:
            logger.info(name + ": " + str(error))
            return

    def run(self, client, network):
        if (self.total_active + 1) <= 10:
            try:
                self.check_certs(check_platform())

                image = self.container
                if platform.machine() == 'armv6l':
                    image = self.alt_container

                if self.volumes:
                    c = client.containers.run(image, \
                        detach=self.detach, ports=self.makeports(), \
                        environment=[self.environment])
                else:
                    c = client.containers.run(image, \
                        detach=self.detach, ports=self.makeports(), \
                        read_only=self.read_only)

                network.connect(c)

                self.total_active += 1

                return c

            except OSError as err:

                logger.info(err)
                if current_container:
                    logger.info(current_container.logs())
                    # rm_container()
            return
        else:
            logger.info("max number of %s containers are active" % self.name)

    def add_instance(self, client, network):
        if not self.instances:
            self.create_support_file_structure()

        c = self.run(client, network)
        t = self.connect_to_hpotter()

        self.instances.append((c, t))
        logger.info('added a %s container' % self.name)

    def remove_instance(self, client, network):
        if self.total_active > 0:
            c, t = self.instances.pop(0)
            if not self.instances:
                self.remove_support_file_structure()

            c.stop()
            c.remove()
            logger.info("stoped and removed %s container" % self.name)
            t.request_shutdown()
        else:
            logger.info("there are no %s containers to shutdown")

    def check_certs(self, dir):
        if self.cert != 'None':
            if not os.path.isfile(dir):
                create_tls_cert_and_key(dir)

def create_tls_cert_and_key(tmp_file):
    """ Generate a cert and place it into the tmp_file location.

    Parameters
    ----------
    tmp_file : String
        The path to were the generated cert should be placed.

    """
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

def check_platform():
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        return '/tmp/cert.pem'
    elif platform.system() == 'Windows':
        # os.mkdir('temp')
        return "temp\\cert.pem"

def remove_certs():
    tmp_file = check_platform()
    try:
        if set_cert:
            os.remove(tmp_file)
            logger.info("removing TLS cert and key")
    except:
        raise FileNotFoundError
