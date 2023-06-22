from client_socket import client_socket
#from arena import auth_screen



class App():

    def __init__(self, HOST="localhost", PORT=10000) -> None:
        print("START GAME")
        #register_page = auth_screen.MainApp()
        client_socket.ClientConnection(HOST, PORT)

if __name__ == "__main__":
    try:
        #App()

        App("172.4.181.190", 10000)
        #App("172.4.181.220", 10000)
        
        #App("172.4.181.240", 10000)

    except KeyboardInterrupt:
        exit()
