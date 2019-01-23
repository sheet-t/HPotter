from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declared_attr
from hpotter.hpotter import ConnectionTable
from hpotter.env import logger, Session
import socket
import socketserver
import threading
from datetime import *

# remember to put name in __init__.py

class HTTPTable(ConnectionTable.Base):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    request = Column(String)

    connectiontable_id = Column(Integer, ForeignKey('connectiontable.id'))
    connectiontable = relationship("ConnectionTable")


Header = '''
HTTP/1.1 200 OK
Date: {now}
Server: Apache/2.4.6 (Red Hat Enterprise Linux) OpenSSL/1.0.2k-fips mod_fcgid/2.3.9 PHP/5.4.16
Last-Modified: {now}
Accept-Ranges: bytes
Content-Length: 1024
Cache-Control: max-age=0
{today}, Expires: {nowplustwelve}
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

<html>
<title>Forbidden</title>
<center>
<body>
<h1>Forbidden</h1>
<p id="date"></p>
<script>
document.getElementById("date").innerHTML = Date();
</script>
</body>
</center>
</html>
'''.format(now=datetime.now(), nowplustwelve=datetime.now() + timedelta(hours=12),
           today=datetime.today()).encode("utf-8")

class HTTPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).decode("utf-8")

        entry = ConnectionTable.ConnectionTable(
            sourceIP=self.client_address[0],
            sourcePort=self.client_address[1],
            destIP=self.server.mysocket.getsockname()[0],
            destPort=self.server.mysocket.getsockname()[1],
            proto=ConnectionTable.TCP)
        http = HTTPTable(request=data)
        http.connectiontable = entry
        Session.add(http)

        self.request.sendall(Header)

    def finish(self):
        Session.commit()
        Session.remove()

class HTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer): pass

def start_server():
    server = HTTPServer('0.0.0.0', 8080), HTTPHandler)
    server.serve_forever()

def stop_server():
    pass
