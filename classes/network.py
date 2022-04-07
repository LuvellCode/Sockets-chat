import socket
import pickle

from classes.server_commands import Commands
from classes.user import User
from classes.message import Message
from host_info import *


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = IP_ADDRESS
        self.port = PORT
        self.addr = (self.ip, self.port)

    def connect(self):  # returns pickle User object
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.receive())
        except:
            pass

    # returns pickle object Message to be updated in chat
    def send_msg(self, message: str):
        self.send_str(Commands.NEW_MESSAGE + message)

    # returns pickle Room object
    def get_room(self):
        self.send_str(Commands.GET_ROOM)

        return pickle.loads(self.receive())

    def send_str(self, message: str):
        self.send(message.encode())

    def receive(self):
        return self.client.recv(2048*2)

    def send(self, message: bytes):
        try:
            self.client.send(message)
        except socket.error as e:
            print(e)

    # returns pickle User object
    def set_username(self, username: str):
        self.send_str(Commands.SET_USERNAME + username)

    # returns pickle User object
    def set_prefix(self, prefix: str):
        self.send_str(Commands.SET_PREFIX + prefix)
