import socket
import json
import threading


class ClientConnection:
    def __init__(self, host="localhost", port=10000) -> None:
        self.init_message = "teszt hello"
        self.action_types = ["Action","Registration","Closed"]

        self.connect_to_server(host, port)

    def connect_to_server(self, HOST, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))

            self.send_message(client_socket, self.init_message)

            incomming_messages=threading.Thread(target=self.accept_incoming, args=(client_socket,))
            incomming_messages.start()

            while True:
                print("ACTIONS:")
                for index, actions_text in enumerate(self.action_types):
                    print(f"{index}:{actions_text}")

                choosen = input("\nKüldöm üzenet:")
                try: 
                    selected_number = int(choosen)

                except ValueError:
                    print("Számot kérek!")
                    continue       

                if selected_number <0 or selected_number >= len(self.action_types):
                    print("A listából válassz!")
                    continue

                action = self.action_types[selected_number]

                match action:
                    case "Action":
                        test_action = {"1": "hit","2": "defend"}
                        self.send_message(client_socket, self.action_message(test_action))
                        
                    case "Registration":
                        test_user_name =  {"username": "xy","password": "xy"}
                        self.send_message(client_socket, self.registration_message(test_user_name))
                        
                    case "Closed":
                        self.send_message(client_socket, self.close_message())

    def send_message(self,client_socket, message):
        client_socket.sendall(json.dumps(message).encode("utf-8"))

#region OUTGOING MESSAGES:
    def action_message(self, action: dict) -> dict:
        # example: {"Type": "Action",Payload": {"1": "hit","2": "defend"}}
        return {"Type": "Action", "Payload": action}

    def registration_message(self, user_name_and_password: dict) -> dict:
        # example: {"Type": "Registration",Payload": {"username": "xy","password": "xy"}}
        return {"Type": "Registration", "Payload": user_name_and_password}
    
    def close_message(self) -> dict:
        # example: {"Type": "Registration",Payload": {"username": "xy","password": "xy"}}
        return {"Type": "Closed", "Payload":{}}    
#endregion
#region INCOMING MESSAGES:
    def accept_incoming(self, client_socket):
        try:
            while True:
                data = client_socket.recv(2048)

                if not data:
                    print("Server disconnected!")
                    break

                incoming = json.loads(data.decode("utf-8"))
                print(f"FROM SERVER:{incoming}")

        except Exception as e:
            print("EXCEPTION", e)


#endregion

ClientConnection()
