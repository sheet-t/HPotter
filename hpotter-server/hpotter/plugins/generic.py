import socket, ssl
import threading

from hpotter import tables
from hpotter.env import logger, write_db, getLocalRemote

# remember to put name in __init__.py


def wrapper(function):
    try:
        return function()
    except socket.timeout as timeout:
        logger.debug(timeout)
        raise Exception
    except socket.error as error:
        logger.debug(error)
        raise Exception
    except Exception as exc:
        logger.debug(exc)
        raise Exception

# started from: http://code.activestate.com/recipes/114642/


class OneWayThread(threading.Thread):
    def __init__(self, source, dest, table=None, request_type='', limit=0, di=None):
        super().__init__()
        self.source = source
        self.dest = dest
        self.table = table
        self.request_type = request_type
        self.limit = limit
        self.di = di
        
        if self.table:
            self.connection = tables.Connections(
                sourceIP=self.source.getsockname()[0],
                sourcePort=self.source.getsockname()[1],
                destPort=self.dest.getsockname()[1],
                localRemote = getLocalRemote(self.source.getsockname()[0]),
                proto=tables.TCP)
            write_db(self.connection)
        
    def run(self):
        total = b''
        while 1:
            try:
                data = wrapper(lambda: self.source.recv(4096))
                if self.dest.getsockname()[1]:

                    pass
            except Exception:
                break
            
            if data == b'' or not data:
                break

            if self.table or self.limit > 0:
                total += data

            try:
                wrapper(lambda: self.dest.sendall(data))
            except Exception:
                break
            
            if type(len(total)) != type(self.limit):
                self.limit = 4096
                if len(total) >= (self.limit) > 0:
                    break
            elif len(total) >= self.limit > 0:
                break

        if self.table:
            if self.di:
                total = self.di(total)
            # Save this print statement for later debugging
            # logger.info([(k, type(v)) for k,v in vars(self).items()])
            self.request = tables.Requests(request_type=self.request_type, request=str(total), connection=self.connection)
            write_db(self.request)

        self.source.close()
        self.dest.close()


class PipeThread(threading.Thread):
    def __init__(self, bind_address, connect_address, table, limit, request_type='', di=None, tls=False):
        super().__init__()
        self.bind_address = bind_address
        self.connect_address = connect_address
        self.table = table
        self.request_type = request_type
        self.limit = limit
        self.di = di
        self.tls = tls

        self.shutdown_requested = False

    def run(self):
        source_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        source_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        source_socket.settimeout(5)
        source_socket.bind(self.bind_address)
        source_socket.listen()
    
        while True:
            try:
                source = None
                try:
                    source, address = source_socket.accept()
                    if self.tls:
                        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                        context.load_cert_chain(certfile="/tmp/cert.pem", keyfile="/tmp/cert.pem")
                        source = context.wrap_socket(source, server_side=True)
                except socket.timeout:
                    if self.shutdown_requested:
                        logger.info('Shutdown requested')
                        if source:
                            source.close()
                            logger.info('----- %s: Socket closed', self.table)
                        return
                    else:
                        continue

                dest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                dest.settimeout(30)
                dest.connect(self.connect_address)

                if self.request_type == '':
                    OneWayThread(source=source, dest=dest, table=self.table,
                        limit=self.limit, di=self.di).start()
                else:
                    OneWayThread(source=source, dest=dest, table=self.table,
                         request_type=self.request_type, limit=self.limit,
                         di=self.di).start()
                OneWayThread(dest, source).start()

            except OSError as exc:
                dest.close()
                source.close()
                logger.info(exc)
                continue

    def request_shutdown(self):
        self.shutdown_requested = True
