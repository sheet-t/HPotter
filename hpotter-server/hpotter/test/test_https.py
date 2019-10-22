import ssl, socket

hostname = '127.0.0.1'
# PROTOCOL_TLS_CLIENT requires valid cert chain and hostname
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations('/Users/mattmcmahon/Desktop/cert.pem')

# TODO - TLS is up and running, but nothing is recv from hpotter

address = (hostname, 443)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:

        print("connected to hostname: ", hostname)
        ssock.connect(address)
        message = ssock.recv(4096)
        if message:
            print(message)
            ssock.close()
            sock.close()
        else:
            print("no message received")
       
        