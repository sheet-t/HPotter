import ssl, socket

hostname = '127.0.0.1'
# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('/Users/mattmcmahon/Desktop/Matt/HPotter/hpotter/test/cert.pem')

# TODO - TLS is up and running, but nothing is recv from hpotter
ports = [443, 3307, 8090]
while True:
    for i in ports:
        address = (hostname, i)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # print(ssock.version())
                # print(context)
                # print("sock: ", sock)
                # print("ssock: ", ssock)
                print("i:", i)
                print("hostname: ", hostname)
                ssock.connect(address)
                print(ssock.recv(4096))
                ssock.close()
                sock.close()
                