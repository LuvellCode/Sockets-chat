

class User:
    # USERNAME MUST BE UNIQUE
    def __init__(self, id, name: str = None, admin: bool = False, prefix: str = None):
        self.__id = id
        self.__name = name
        self.__admin = admin
        self.prefix = prefix

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    @property
    def admin(self):
        return self.__admin

    @admin.setter
    def admin(self, is_admin: bool):
        self.__admin = is_admin

    def __repr__(self):
        string = f"User(name: '{self.name}', admin: {self.admin}"
        string += f", prefix: '{self.prefix}'" if self.prefix else ''
        
        string += ")"

        return string
