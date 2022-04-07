

class Commands:
    NEW_MESSAGE = 'new_message|'
    SET_USERNAME = 'set_user|'
    SET_PREFIX = 'set_prefix|'
    GET_ROOM = 'get_room|'

    @staticmethod
    def get():
        return Commands.NEW_MESSAGE, Commands.SET_USERNAME, \
               Commands.SET_PREFIX, Commands.GET_ROOM

