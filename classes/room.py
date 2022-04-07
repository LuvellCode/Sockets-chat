from classes.message import Message
from classes.user import User


class Room:
    MAX_USERS: int = 20

    def __init__(self, id, limit: int = None):
        self.id = id
        self.limit = limit if limit else self.MAX_USERS
        self.__connected_users = []
        self.__messages = []

        # TODO: add log class for logging messages
        # self.log = {}  # '24.04.2021 23:35:12': {'user': 'username', 'message': 'hi!'}

    @property
    def size(self):
        return len(self.__connected_users)

    @property
    def messages_sent(self):
        return len(self.__messages)

    def add_user(self, user: User, force: bool = False):
        length = len(self.__connected_users)
        if length >= self.MAX_USERS or (length >= self.limit and not force):
            return False
        self.__connected_users.append(user)

    def del_user(self, user):

        if isinstance(user, User):
            if user in self.__connected_users:
                self.__connected_users.remove(user)
                return True
        elif isinstance(user, str):
            user_ = self.get_user_by_name(user)
            if user_:
                self.__connected_users.remove(user_)
            return True
        elif isinstance(user, int):
            user_ = self.get_user_by_id(user)
            if user_:
                self.__connected_users.remove(user_)
        return False

    def get_user_by_name(self, username: str) -> User or None:
        for i in self.__connected_users:
            if i.name == username:
                return i

    def get_user_by_id(self, id):
        for i in self.__connected_users:
            if i.id == id:
                return i

    def add_message(self, message: Message):
        self.__messages.append(message)

    @property
    def messages(self):
        return self.__messages

    def __repr__(self):
        string = f"Room(id: {self.id}, limit: {self.limit}, users: {self.size}, messages sent: {self.messages_sent})"

        return string
