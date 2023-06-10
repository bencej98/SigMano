import socket
import json
import threading
import time
from tkinter import messagebox
from arena.auth_screen import MainApp
from arena.arena import start_loop

class ClientConnection:
    def __init__(self, host, port) -> None:
        self.init_message = "teszt hello"
        self.action_types = ["Action", "Registration", "Closed"]

        self.user_name = None
        self.user_password = None

        self.socket_client = None

        self.frame_destroy = None

        self.incomming = Incomming()
        self.outgoing = Outgoing()

        self.connect_to_server(host, port)

    def init_socket(self, socket):
         self.socket_client = socket

    def connect_to_server(self, HOST, PORT):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))

                incomming_messages = threading.Thread(target=self.incomming.accept_incoming, args=(client_socket,self.init_socket,  self.destroy_frames))
                incomming_messages.start()
                

                while not self.socket_client:
                    print("Wait for init socket", self.socket_client)
                    time.sleep(1)

                auth_screen_app = MainApp(self.get_user_name_password_from_form)
                auth_screen_app.mainloop()
            
                

                #TODO:switch on authentication
                # self.send_message(client_socket, self.init_message)
                # is_authenticated = False
                # while not is_authenticated:
                #     self.user_name = input("Kérem a nevét:")
                #     self.user_password = input("Kérem a jelszót:")

                #     is_authenticated = self.auth_client(client_socket,self.user_name, self.user_password)
                #     if not is_authenticated:                        
                #         print("Authentication failed!")
                #     else:
                #         break


                while True:
                    print("ACTIONS:")
                    for index, actions_text in enumerate(self.action_types):
                        print(f"{index}:{actions_text}")

                    choosen = input("\nAction >> ")
                    if choosen == "q":
                        break
                    try:
                        selected_number = int(choosen)

                    except ValueError:
                        print("Számot kérek!")
                        continue

                    if selected_number < 0 or selected_number >= len(self.action_types):
                        print("A listából válassz!")
                        continue

                    action = self.action_types[selected_number]

                    match action:
                        case "Action":
                            test_action = {"1": "hit", "2": "defend"}
                            self.send_message(client_socket, self.outgoing.action_message(test_action))

                        case "Registration":
                            test_user_name = {"username": "xy", "password": "xy"}
                            self.send_message(client_socket, self.outgoing.registration_message(test_user_name))

                        case "Closed":
                            self.send_message(client_socket, self.outgoing.close_message())
                            break

            client_socket.close()

        except ConnectionError as e:
            print("[Something went wrong]: ConnectionError", e)

    def destroy_frames(self):
        self.frame_destroy()

    def get_user_name_password_from_form(self, log_type, name, password, frame_destroy):
        print("frame dest:",frame_destroy)
        self.frame_destroy = frame_destroy

        if log_type == "Auth":
            self.auth_client(self.outgoing.authentication_message, name,password)

        if log_type == "Registration":
            self.auth_client(self.outgoing.registration_message, name,password)

    def auth_client(self, auth_or_register, name, password) -> bool:
        user_data={"username": name,"password": password}
        self.send_message(self.socket_client, auth_or_register(user_data))

        # message = self.process_incomming_register_login(self.socket_client)
        # print("auth_client", message)

    # def process_incomming_register_login(self, client_socket):
    #     data = client_socket.recv(2048)
    #     incoming = self.incomming.parse_incoming(data)
    #     print("AUTH", incoming)

    #     self.frame_destroy()

    #     if incoming["Type"] == "Auth" and incoming["Payload"]:
    #         return True

    #     return False


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
class Message:
    def __init__(self, incoming_type, payload) -> None:
        self.Type = incoming_type
        self.Payload = payload


class Incomming:
    def __init__(self) -> None:
        self.positions = None
        self.event = None
        pass

    def accept_incoming(self, client_socket, set_socket_cb, frame_destroy):
        set_socket_cb(client_socket)

        try:
            while True:
                data = client_socket.recv(2048)
                if not data:
                    print("Server disconnected!")
                    break

                incoming = self.parse_incoming(data)

                print(f"FROM SERVER: {incoming}")

                if incoming["Type"] == "Registration" or incoming["Type"] == "Auth":
                    if not incoming["Payload"]:
                        messagebox.showinfo("Message", f"{'Registration' if incoming['Type']=='Registration' else 'Authentication'} success!")
                        return
                    
                #TODO: nyissa meg az arénát.
                    messagebox.showinfo("User registered", "Registration success!")
                    frame_destroy()
                    start_loop()
                    # temp_valami()

        except Exception as e:
            #print("EXCEPTION", e)
            pass

    def parse_incoming(self, data):
        return json.loads(data.decode("utf-8"))



# endregion
