import queue
import json
import time
import socket
import threading
from game_datab import *
from gnome import *


class Message:
    def __init__(self, type, payload) -> None:
        self.type = type
        self.payload = payload


class Connection:
    def __init__(self, sock: socket.socket) -> None:
        self.incoming_queue = queue.Queue()
        self.sock = sock
        self.name = None
        self.thread = threading.Thread(target=self.incoming_traffic_manager, daemon=True)
        self.thread.start()

    def is_alive(self):
        return self.sock is not None
    
    def close(self):
        if self.is_alive():
            try:
                self.sock.getpeername()
                print(f"Closing connection from {self.name}")
            except OSError:
                print(f"Closed connection by {self.name}.")
            self.sock.close()
            self.sock = None
    
    def incoming_traffic_manager(self):
        while self.is_alive():
            try:
                data = self.sock.recv(1024)
            except ConnectionResetError:
                break
            if not data:
                break
            else:
                try:
                    incoming_data = json.loads(data.decode("utf-8"))
                    print(incoming_data)
                except json.decoder.JSONDecodeError:
                    remote = self.sock.getpeername()
                    print(f"Invalid payload from {remote[0]}:{remote[1]}")
                else:
                    self.incoming_queue.put(incoming_data)
            time.sleep(0.001)
        self.close()

    def outgoing_traffic_manager(self, data):  
        if self.is_alive():
            try:
                self.sock.send(json.dumps(data).encode("utf-8"))
            except ConnectionResetError:
                self.close()

class Gameserver:
    def __init__(self, ip="0.0.0.0", port=10000) -> None:
        self.messages = []
        self.server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        self.connections = {}
        self.db = Gnome_Database()
        self.travel = Map(19, 19, 5)
        self.connections_lock = threading.Lock()
        self.incoming_connections_thread = threading.Thread(
            target=self.new_connection, daemon=True)
        self.incoming_connections_thread.start()
    
    def new_connection(self):
        while True:
            sock, addr = self.server_socket.accept()
            print(f"Connected by {addr}")
            connection_id = f"{addr[0]}:{addr[1]}"
            connection = Connection(sock)
            with self.connections_lock:
                self.connections[connection_id] = connection
            time.sleep(0.001)

    def check_incoming_messages(self):
        new_messages = {}
        for connection_id in self.connections:
            conn_queue = self.connections[connection_id].incoming_queue
            if not conn_queue.empty():
                msg = conn_queue.get()
                msg_obj = Message(msg["Type"], msg["Payload"])
                new_messages[connection_id] = msg_obj
        return new_messages
    
    def process_data(self):
        new_messages = self.check_incoming_messages()
        self.check_connections_liveness()
        for connection_id in new_messages:
            curr_msg = new_messages[connection_id]
            if curr_msg.type:
                if curr_msg.type == "Action":
                    self.send_response(connection_id,
                        {'Type': 'Action', 'Payload': {'1': 'hit', '2': 'defend'}})
                elif curr_msg.type == "Registration":
                    self.send_response(connection_id, self.db.check_user_upon_registration(curr_msg.payload['username'], curr_msg.payload['password']))
                elif curr_msg.type == "Closed":
                    self.connections[connection_id].close()
                elif curr_msg.type == "Position":
                    self.broadcast_message({
                        "Type": "Position",
                        "Payload": {
                            "User": ['x', 'y']
                        }
                    })
                elif curr_msg.type == "Event":
                    self.send_response( connection_id, {
                        "Type": "Event",
                        "Payload": {
                            "happening": "msg",
                            "outcome": "msg"
                        }
                    }) 
                else:
                    self.broadcast_message(800)  # Send code 999 for unknown type
            else:
                self.broadcast_message(999)  # Send code 999 for missing type
    def tik_data(self):
        while True:
            gnomes_list = []
            for n in range (10):
                gnome = Gnome(f"loluser{n}")
                gnomes_list.append(gnome)

            map = Map(19, 19, 5)
            for gnome in gnomes_list:
                map.add_gnome_to_gnome_queue(gnome)
            map.transfer_gnomes_to_active_gnomes()

            for gnome_name, gnome in map.active_gnomes.items():
                for valami in range(20):
                    gnome.random_move(map)
            position_dict = map.move_all_gnomes()
            self.broadcast_message(position_dict)
            print(position_dict)
            time.sleep(2)

    def run_tik_data_thread(self):
        tik_thread = threading.Thread(target=self.tik_data)
        tik_thread.start()

    def broadcast_message(self, data):
        for connection_id in self.connections:
            self.connections[connection_id].outgoing_traffic_manager(data)

    def send_response(self, person_id, data):
        if person_id in self.connections:
            self.connections[person_id].outgoing_traffic_manager(data)

    def check_connections_liveness(self):
        conns_to_del = []
        for connection_id in self.connections:
            if not self.connections[connection_id].is_alive():
                conns_to_del.append(connection_id)
        for id in conns_to_del:
            self.connections.pop(id)

def main():
        server = Gameserver()
        server.db.create_table()
        server.run_tik_data_thread()
        while True:            
            server.process_data()
            time.sleep(0.001)

if __name__ == "__main__":
    main()