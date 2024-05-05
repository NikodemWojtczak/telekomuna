import socket


class TCP:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_file(self, file_path):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            with open(file_path, 'rb') as file:
                data = file.read()
                s.sendall(data)

    def receive_file(self, file_path):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with open(file_path, 'wb') as file:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    file.write(data)
