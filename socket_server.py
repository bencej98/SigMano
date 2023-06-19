import queue
import json
import time
import socket
import threading
from game_datab import *
from gnome import *
from action_manager import *

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
    def __init__(self, travel, action_manager:ActionManager, ip="0.0.0.0", port=10000, ) -> None:
        self.messages = []
        self.server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        self.connections = {}
        self.travel = travel
        self.action_manager= action_manager
        self.db = Gnome_Database()
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
        for connection_id, curr_msg in new_messages.items():
            if curr_msg.type:
                if curr_msg.type == "Action":
                    self.handle_action_message(connection_id, curr_msg.payload)
                elif curr_msg.type == "Registration":
                    self.handle_registration_message(connection_id, curr_msg.payload)
                elif curr_msg.type == "Login":
                    self.handle_login_message(connection_id, curr_msg.payload)
                elif curr_msg.type == "Closed":
                    self.connections[connection_id].close()
                else:
                    self.broadcast_message("Invalid payload")

    def handle_action_message(self, connection_id, payload):
        username = self.connections[connection_id].name
        if username not in self.travel.all_gnomes:
            gnome = Gnome(username)
            gnome.strategy = payload
            self.travel.all_gnomes[username] = gnome
            self.travel.add_gnome_to_gnome_queue(gnome)
        else:
            self.action_manager.update_gnomes_strategy(self.travel, payload, username)

    def handle_registration_message(self, connection_id, payload):
        connection = self.connections[connection_id]
        connection.name = payload['username']
        response = self.db.check_user_upon_registration(payload['username'], payload['password'])
        self.send_response(connection_id, response)

    def handle_login_message(self, connection_id, payload):
        connection = self.connections[connection_id]
        is_valid = json.loads(self.db.login_user(payload['username'], payload['password']))
        if is_valid["Payload"]:
            connection.name = payload['username']
            self.send_response(connection_id, is_valid)
        else:
            self.send_response(connection_id, is_valid)

    def tik_data(self):
        while True:
            self.travel.transfer_gnomes_to_active_gnomes()
            position_dict = self.action_manager.move_all_gnomes(self.travel)
            self.broadcast_message(position_dict)
            time.sleep(0.1)
            act_fight = self.action_manager.fight(self.travel)
            print(position_dict)
            if len(act_fight) != 0:
                self.broadcast_message({"Type": "Event", "Payload": act_fight})
                time.sleep(0.1)
                print(act_fight)
                death_check = self.action_manager.check_gnome_death(self.travel)
                if death_check["Payload"]:
                    self.broadcast_message(death_check)
                    for death in death_check["Payload"]:
                        self.db.add_results_upon_death(death["user"], death["score"], death["kills"])
                    self.broadcast_message(self.db.get_sumscores())
            time.sleep(2)


    def run_tik_data_thread(self):
        tik_thread = threading.Thread(target=self.tik_data, daemon=True)
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
        travel = Map(2, 2, 3)
        action = ActionManager()
        server = Gameserver(travel, action)
        server.db.create_table()
        server.run_tik_data_thread()
        while True:            
            server.process_data()
            time.sleep(0.001)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()