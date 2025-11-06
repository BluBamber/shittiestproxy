import socket
import threading
import requests

class ProxyServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port

    def handle_request(self, client_socket):
        request = client_socket.recv(1024)
        url = request.decode().split()[1].split("://")[1].split("/")[0]
        response = requests.get(f'http://{url}')
        client_socket.send(response.content)
        client_socket.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=self.handle_request, args=(client_socket,)).start()

if __name__ == "__main__":
    ProxyServer().start()
