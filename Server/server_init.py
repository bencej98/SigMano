from socket_server import *
from action_manager import *
from gnome import *
import time

def main():
    travel = Map(5, 5, 7)
    action = ActionManager()
    server = Gameserver(travel, action)
    server.db.create_table()
    server.run_tik_data_thread()
    while True:            
        server.process_data()
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()