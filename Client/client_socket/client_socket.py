import socket
import json
import threading
import time
import random
import queue

from tkinter import messagebox
from arena.auth_screen import MainApp
from arena.new_strategy_ui import ActionApp
from arena.arena import start_loop, dict_data_for_screen, json_temp, set_temp_json, set_leader_board, set_dead_list,set_fight_event

class ClientConnection:

    static_user_name = "missing - in client connection"

    def __init__(self, host, port) -> None:
        self.init_message = "teszt hello"
        self.action_types = ["Action", "Registration", "Closed"]

        self.user_name = None
        self.user_password = None

        self.socket_client = None
        
        self.loginRegister_frame_destroy = None

        self.login_closed = False
        self.auth_screen_app = None


        self.incoming_queue = queue.Queue()
        self.incomming = Incomming(self.incoming_queue)

        self.outgoing_queue = queue.Queue()
        self.outgoing = Outgoing(self.outgoing_queue)

        self.connect_to_server(host, port)

    def init_socket(self, socket):
         self.socket_client = socket
    

    def connect_to_server(self, HOST, PORT):        
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.connect((HOST, PORT))

            incomming_messages = threading.Thread(target=self.incomming.accept_incoming, args=(self.socket_client,self.init_socket, self.destroy_frames, self.user_name,))
            incomming_messages.start()

            auth_screen_app = MainApp(self.get_user_name_password_from_form)
            auth_screen_app.mainloop() 

            # a = ActionApp(self.get_user_name_password_from_form)
            # a.mainloop()          
         
    def destroy_frames(self):
        self.loginRegister_frame_destroy()        

    def get_user_name_password_from_form(self, log_type, name, password, frame_destroy):
        ClientConnection.static_user_name = name
        self.loginRegister_frame_destroy = frame_destroy
        self.login_closed = True
        self.user_name = name

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
    def __init__(self, outgoing_queue=None) -> None:
        self.outgoing_queue = outgoing_queue
        pass

    def registration_message(self, user_name_and_password: dict) -> dict:
        # example: {"Type": "Registration","Payload": {"username": "xy","password": "xy"}}
        return {"Type": "Registration", "Payload": user_name_and_password}
    
    def authentication_message(self, user_name_and_password:dict ):
        # example: {"Type": "Auth","Payload": {"username": "xy","password": "xy"}}
        return {"Type": "Login", "Payload": user_name_and_password}

    def action_message(self, action: dict) -> dict:
        # example: {"Type": "Action","Payload": {"1": "hit","2": "defend"}}
        return {"Type": "Action", "Payload": action}
    
    def behavior_message(self, action: dict) -> dict:
        # example: {"Type": "Action","Payload": {"1": "hit","2": "defend"}}
        return {"Type": "Behavior", "Payload": action}


    def close_message(self) -> dict:
        # example: {"Type": "Registration","Payload": {"username": "xy","password": "xy"}}
        return {"Type": "Closed", "Payload": {}}
# endregion
# region INCOMING MESSAGES:
class Incomming:

    counter = 0
    def __init__(self, incoming_data_queue) -> None:
        self.positions = None
        self.event = None
        self.user_name = None
        self.is_logged_in = False
        self.is_started = False

        self.is_login_success = False

        self.action_payload = None
        self.chosen_color = None
        
        self.incoming_queue = incoming_data_queue 
        self.outgoing = Outgoing()      

    def accept_incoming(self, client_socket, set_socket_cb, frame_destroy, user_name):
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
                #print("DATA:", data)
                incoming = self.parse_incoming(data)
                self.process_incoming(incoming, frame_destroy)

                if self.is_login_success:
                    self.is_login_success = False

                    #zárja a regisztárciót:
                    self.destroy_login_ui(frame_destroy)

                    #nyitja a choose_action képrenyőt
                    a = ActionApp(self._get_action_payload)
                    a.mainloop()

                    print("ACTION: ", self.action_payload)

                    #akciók küldése a szerver részére
                    client_socket.sendall(json.dumps(self.outgoing.action_message(self.action_payload["Payload"])).encode("utf-8"))

                    #nyitja az arenát felületet:
                    start_arena = threading.Thread(target=self.start_arena)
                    start_arena.start()

    def _get_action_payload(self, action_payload: dict, chosen_color: str):
        self.action_payload = action_payload
        self.chosen_color = chosen_color

    def process_incoming(self, incoming, frame_destroy):


        if incoming is not None:
            try:
                if incoming["Type"] == "Registration" or incoming["Type"] == "Auth":
                    self.is_login_success = self.login_status(incoming, frame_destroy)

                if incoming["Type"] == "Position":
                    self.put_queue(incoming)

                #TODO:
                #{"Type": "Event", 
                # "Payload": {
                #   "Attila": [{"encounter": "Attila used rock and Andras used rock", "outcome": "tie"}], 
                #   "Andras": [{"encounter": "Attila used rock and Andras used rock", "outcome": "tie"}]}
                # }
                if incoming["Type"] == "Event":
                    event_payloads = incoming["Payload"]
                    if len(event_payloads) > 0:
                        self.process_fight_events(event_payloads)

                #TODO:
                # {"Type": "Death", "Payload": []}' Minden Event-l együtt jön üresen is!
                if incoming["Type"] == "Death":
                    if len(incoming["Payload"]) > 0:
                        payload_list = incoming["Payload"]
                        self.print_dead_msg(payload_list)

                #TODO:
                # Type : Leader , Payload: [{"Andras": 5}, {"Bela": 6 } , { }]
                if incoming["Type"] == "Leader":
                    if len(incoming["Payload"]) > 0:
                        ordered_leaders = sorted(incoming["Payload"], key=self.get_values_for_sort, reverse=True)
                        print("LEADER board", ordered_leaders)
                        set_leader_board(ordered_leaders)
                    
            except:
                pass

    def get_values_for_sort(self, leader_list):
        return list(leader_list.values())[0]            

    def print_dead_msg(self, incoming):
        death_messages = ["Good day to die!", "Oh my God!", "Rest My Peace!", "Holy sh**t!"]
        death_msg_len = len(death_messages)
        
        for dead_user in incoming:
            rand_msg_index = random.randrange(0,death_msg_len-1)
            dead_string =  f"{dead_user}: {death_messages[rand_msg_index]}"
            set_dead_list(dead_string)

    def process_fight_events(self,incoming_payload_event):
        for (user, fight_list) in incoming_payload_event.items():
            payload_list = list(fight_list[0].values())

            encounter_msg = payload_list[0]
            result_msg = payload_list[1]

            fight_string = f"{encounter_msg}, result is {result_msg}!" 
            set_fight_event(fight_string)


    def login_status(self, incoming, frame_destroy):
        if not incoming["Payload"]:
            messagebox.showinfo("Message", f"{'Registration' if incoming['Type']=='Registration' else 'Authentication'} failed!")
            return False
        return True

    def destroy_login_ui(self, frame_destroy):
        self.is_logged_in = True
        #messagebox.showinfo("User registered", "Registration success!")
        print("Registration success!")
        frame_destroy()

    def start_arena(self):
        username = ClientConnection.static_user_name
        print("USRR", username)
        print("COLOR:", self.chosen_color)
        start_loop(self.chosen_color)
        # start_loop({'loluser': [2, 3], 'loluser2': [18, 9]})

    def change_data(self, positions, username):
        set_temp_json(positions, username)

    def pop_queue(self):
        username = None
        while True:
            username = ClientConnection.static_user_name
            if not self.incoming_queue.empty():
                incoming = self.incoming_queue.get()
                print(f"{Incomming.counter} incoming queue:", incoming)
                Incomming.counter += 1
                if incoming["Type"] == "Position":
                    self.change_data(incoming['Payload'], username)
            time.sleep(1)

    def put_queue(self, parsed):
        self.incoming_queue.put(parsed)


    def parse_incoming(self, data):
        try:
            data = data.decode("utf-8")
            parsed = json.loads(data)
            #print("PAAAYLOOAD: ", parsed)

            return parsed
        except Exception as e:
            print("DATA CONGESTIONS!", data)

# endregion
