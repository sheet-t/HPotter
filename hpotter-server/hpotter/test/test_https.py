import ssl, socket, requests

hostname = '127.0.0.1'
data = b'test'
url = 'http://127.0.0.1'

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        
        response = requests.post(url, data=data, verify='cert.pem')
        if response:
            print("Received:\t", response.content.decode('utf-8'))
            ssock.close()
            sock.close()
        else:
            print("no response received")

        
