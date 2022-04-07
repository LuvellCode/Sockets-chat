import logging
import pickle

import threading
from _thread import *

from classes.room import Room
from classes.user import User
from classes.message import Message
from classes.network import Network


class Client:
    def __init__(self):
        self.network = Network()

        username = input("Enter your name > ")
        prefix = "[SUPPA DUPPA COOL]"

        self.user: User = self.network.connect()  # User is returned when connection is established
        self.room: Room = self.network.get_room()

        self.user.name = username
        self.user.prefix = prefix

        self.network.set_username(username)
        self.network.set_prefix(prefix)

        print(self.user)
        print(self.room)

        # Inputting
        in_data = input("-> ")

        self.network.send_msg(in_data)

        # Logging
        self.main()

    def main(self):
        logging.debug("Executing main script...")
        logging.debug("---")

        run = True

        self.network.send_msg("Hello world!")

        while run:
            try:
                data = pickle.loads(self.network.client.recv(2048*2))

                if not data:
                    break

                print(data)

            except Exception as e:
                logging.error(f"Error occurred: {str(e)}")
                logging.debug(f"Breaking receiving loop...")
                break

        logging.error("Couldn't get room.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(message)s')

    Client()
