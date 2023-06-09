from client_socket import client_socket
#from arena import auth_screen



class App():

    def __init__(self, HOST="localhost", PORT=10000) -> None:
        print("START GAME")
        #register_page = auth_screen.MainApp()
        clienet_socket = client_socket.ClientConnection(HOST, PORT)

if __name__ == "__main__":
    App()

    #App("172.4.181.76", 8000)
    #App("172.4.181.221", 10000)
