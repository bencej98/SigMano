import socket
import json
import threading
import time
import random
import queue

from tkinter import messagebox
from arena.auth_screen import MainApp
from arena.arena import start_loop, dict_data_for_screen, json_temp, set_temp_json

class ClientConnection:
    def __init__(self, host, port) -> None:
        self.init_message = "teszt hello"
        self.action_types = ["Action", "Registration", "Closed"]

        self.user_name = None
        self.user_password = None

        self.socket_client = None
        
        self.loginRegister_frame_destroy = None

        self.incomming = Incomming()
        self.outgoing = Outgoing()

        self.connect_to_server(host, port)

    def init_socket(self, socket):
         self.socket_client = socket
    

    def connect_to_server(self, HOST, PORT):
        
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect((HOST, PORT))

            incomming_messages = threading.Thread(target=self.incomming.accept_incoming, args=(self.socket_client,self.init_socket, self.destroy_frames))
            incomming_messages.start()

            auth_screen_app = MainApp(self.get_user_name_password_from_form)
            auth_screen_app.mainloop()            
         
    def destroy_frames(self):
        self.loginRegister_frame_destroy()        

    def get_user_name_password_from_form(self, log_type, name, password, frame_destroy):
        self.loginRegister_frame_destroy = frame_destroy

        if log_type == "Auth":
            self.auth_client(self.outgoing.authentication_message, name,password)

        if log_type == "Registration":
            self.auth_client(self.outgoing.registration_message, name,password)

    def auth_client(self, auth_or_register, name, password) -> bool:
        user_data={"username": name,"password": password}
        self.send_message(self.socket_client, auth_or_register(user_data))

    def send_message(self, client_socket, message):
        client_socket.sendall(json.dumps(message).encode("utf-8"))


# region OUTGOING MESSAGES:
class Outgoing:
    def __init__(self) -> None:
        pass

    def registration_message(self, user_name_and_password: dict) -> dict:
        # example: {"Type": "Registration","Payload": {"username": "xy","password": "xy"}}
        return {"Type": "Registration", "Payload": user_name_and_password}
    
    def authentication_message(self, user_name_and_password:dict ):
        # example: {"Type": "Auth","Payload": {"username": "xy","password": "xy"}}
        return {"Type": "Auth", "Payload": user_name_and_password}

    def action_message(self, action: dict) -> dict:
        # example: {"Type": "Action","Payload": {"1": "hit","2": "defend"}}
        return {"Type": "Action", "Payload": action}


    def close_message(self) -> dict:
        # example: {"Type": "Registration","Payload": {"username": "xy","password": "xy"}}
        return {"Type": "Closed", "Payload": {}}
# endregion
# region INCOMING MESSAGES:
class Incomming:

    counter = 0
    def __init__(self) -> None:
        self.positions = None
        self.event = None

        self.is_logged_in = False
        self.is_started = False

        self.is_login_success = False
        
        self.incoming_queue = queue.Queue()        

    def accept_incoming(self, client_socket, set_socket_cb, frame_destroy):
        set_socket_cb(client_socket)

        #módosítja a pozíciókat
        change_json = threading.Thread(target=self.pop_queue)
        change_json.start()

        while True:                
            try: 
                data = client_socket.recv(2048)
                if not data:
                    print("Server disconnected!")
                    break
            except OSError as e:
                print(e)
            else:
                incoming = self.parse_incoming(data)
                self.process_incoming(incoming)

                if self.is_login_success:
                    #zárja a regisztárciót:
                    destroy_frame_thread = threading.Thread(target=self.destroy_login_ui, args=(frame_destroy, ))
                    destroy_frame_thread.start()

                    #nyitja az arenát felületet:
                    start_arena = threading.Thread(target=self.start_arena)
                    start_arena.start()
                    self.is_login_success = False

    def process_incoming(self, incoming):
        if incoming["Type"] == "Registration" or incoming["Type"] == "Auth":
            self.is_login_success = self.login_status(incoming)

        if incoming["Type"] == "Position":
            self.put_queue(incoming)

        if incoming["Type"] == "Event":
            print("EVENT:",incoming)
        
    def login_status(self, incoming):
        if not incoming["Payload"]:
            messagebox.showinfo("Message", f"{'Registration' if incoming['Type']=='Registration' else 'Authentication'} failed!")
            return False
        return True

    def destroy_login_ui(self, frame_destroy):
        #self.is_logged_in = True
        print("Registration success!")
        frame_destroy()
        #messagebox.showinfo("User registered", "Registration success!")

    def start_arena(self):
        start_loop({'loluser': [2, 3], 'loluser2': [18, 9]})

    def change_data(self, positions):
        set_temp_json(positions)

    def pop_queue(self):
        while True:
            if not self.incoming_queue.empty():
                incoming = self.incoming_queue.get()
                print(f"{Incomming.counter} incoming queue:", incoming)
                Incomming.counter += 1
                if incoming["Type"] == "Position":
                    self.change_data(incoming['Payload'])
            time.sleep(1)

    def put_queue(self, parsed):
        self.incoming_queue.put(parsed)


    def parse_incoming(self, data):
        try:
            data = data.decode("utf-8")
            parsed = json.loads(data)

            return parsed
        except Exception as e:
            print("DATA CONGESTIONS!", data)

# endregion
