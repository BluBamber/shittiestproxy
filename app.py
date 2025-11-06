import socket
import threading
import requests

class ProxyServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port

    def handle_request(self, client_socket):
        try:
            request = client_socket.recv(1024)
            if not request:
                return
            
            request_str = request.decode()
            parts = request_str.split()
            
            if len(parts) < 2:
                print("Invalid request: No URL found.")
                client_socket.close()
                return
            
            url = parts[1]
            
            if "://" in url:
                url = url.split("://")[1]
            else:
                print("Invalid request: No protocol found in URL.")
                client_socket.close()
                return
            
            domain = url.split("/")[0]
            print(f"Proxying request to: {domain}")
            
            response = requests.get(f'http://{domain}')
            client_socket.send(response.content)
        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
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
