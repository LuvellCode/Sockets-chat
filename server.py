import socket
import logging
import pickle
from _thread import *

from classes.server_commands import Commands
from host_info import *
from classes.room import Room
from classes.user import User
from classes.message import Message


class Server:
    def __init__(self, ip: str = None, port: int = None):
        self.ip = ip if ip is not None else '127.0.0.1'
        self.port = port if port is not None else 55555
        logging.info(f"Starting new server on {self.ip}:{self.port}...")
        logging.debug("---")

        self.rooms = {}
        self.users_count = 0
        self.connected = set()
        logging.debug(f"Creating new TCP socket using IPv4 address family...")
        # AF_INET     - IPv4
        # AF_INET6    - IPv6
        # ------------------
        # SOCK_STREAM - TCP
        # SOCK_DGRAM  - UDP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        logging.debug(f"Binding socket to {self.ip}:{self.port}..")
        try:
            self.socket.bind((self.ip, self.port))
        except Exception:
            logging.exception("Binding exception occured", exc_info=True)
            exit()

        # 2 - The maximum length of the pending connections queue
        self.socket.listen(2)

        logging.info("Server started successfully!")
        logging.debug("---")

    def threaded_client(self, connection, user_id, room_id):
        user = User(user_id)
        self.rooms[room_id]['room'].add_user(user)
        logging.debug("Sending user object to connected client...")
        connection.send(pickle.dumps(user))

        while True:
            try:
                data: str = connection.recv(4096).decode()

                if room_id not in self.rooms:
                    break

                if not data:
                    break

                logging.debug(f"New data is coming: {data}")

                room: Room = self.rooms[room_id]['room']

                command = None
                for command_ in Commands.get():
                    if data.startswith(command_):
                        command = command_
                        data = data[len(command_):]
                        break

                # logging.debug(f"Recognized command: {command}")

                if command == Commands.GET_ROOM:
                    connection.sendall(pickle.dumps(room))

                elif command == Commands.SET_USERNAME:
                    user.name = data
                    connection.sendall(pickle.dumps(user))

                elif command == Commands.SET_PREFIX:
                    user.prefix = data
                    connection.send(pickle.dumps(user))

                elif command == Commands.NEW_MESSAGE:
                    message = Message(user, data)

                    room.add_message(message)
                    self.rooms[room_id]['room'] = room

                    for conn in self.rooms[room_id]['connections']:
                        conn.sendall(pickle.dumps(message))

                else:
                    connection.send("Unrecognized command!")

            except Exception as e:
                logging.error(f"Error occurred: {str(e)}")
                logging.debug(f"Breaking receiving loop...")
                break

        logging.debug("Client lost connection")
        try:
            self.rooms[room_id].del_user(user_id)
            self.rooms[room_id]['connections'].remove(connection)
        except:
            pass

        self.users_count -= 1

        connection.close()
        logging.debug("Client connection closed.")
        logging.debug("---")

    def mainloop(self):
        logging.debug(f"Starting mainloop...")
        logging.debug("---")
        while True:
            conn, addr = self.socket.accept()

            logging.debug(f"New user connected on {addr[0]}:{addr[1]}, processing...")

            user_id = self.users_count
            self.users_count += 1
            room_id = None

            if not self.rooms:
                room_id = 1
                self.room_setup(room_id)
            else:
                for index, room_info in self.rooms.items():
                    room = room_info['room']
                    if room.size >= room.limit:
                        continue
                    room_id = index

                if not room_id:
                    lst = list(self.rooms.keys())
                    print(lst)
                    room_id = lst[-1] + 1
                    self.room_setup(room_id)

            self.rooms[room_id]['connections'].append(conn)
            logging.debug("---")
            logging.debug(f"Starting new thread for a client...")
            start_new_thread(self.threaded_client, (conn, user_id, room_id))

    @property
    def rooms_size(self):
        return len(self.rooms)

    def room_setup(self, id, limit: int = None):
        self.rooms[id] = {
            'room': Room(id, limit),
            'connections': []
        }


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

    server = Server(IP_ADDRESS, PORT)
    server.mainloop()
