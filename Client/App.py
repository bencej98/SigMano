from client_socket import client_socket
#from arena import auth_screen



class App():

    def __init__(self, HOST="localhost", PORT=10000) -> None:
        print("START GAME")
        #register_page = auth_screen.MainApp()
        client_socket.ClientConnection(HOST, PORT)

if __name__ == "__main__":
    #App()

    #App("172.4.181.238", 10000)
    App("172.4.181.226", 10000)
