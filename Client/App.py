from client_socket import client_socket


class App():

    def __init__(self, HOST="localhost", PORT=10000) -> None:
        print("START GAME")

        client_socket.ClientConnection(HOST, PORT)

if __name__ == "__main__":
    App()

    #App("172.4.181.76", 8000)
    #App("172.4.181.232", 10000)