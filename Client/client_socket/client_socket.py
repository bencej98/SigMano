import socket
import json

class ClientConnection():

    def __init__(self, host="localhost", port=10000) -> None:
        self.socket = None
        self.init_message = "hello"

        self.connect_to_server(host, port)


    def connect_to_server(self, HOST, PORT):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s

            s.connect((HOST, PORT))
            s.sendall(json.dumps(self.init_message).encode("utf-8"))

            while True:
                action = input("teszt üzenet:")
                self.send_message(action)


    def send_message(self, message):
        self.socket.sendall(json.dumps(message).encode("utf-8"))


    
    
    
ClientConnection()