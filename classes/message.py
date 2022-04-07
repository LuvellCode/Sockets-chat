from classes.user import User


class Message:
    def __init__(self, author: User, text: str):
        self.author = author
        self.text = text

    def __repr__(self):
        string = f"Message(author: {self.author}, text: '{self.text}')"
        return string

    def __str__(self):
        prefix = f"{self.author.prefix} | " if self.author.prefix else ''
        string = f"{prefix}{self.author.name}: {self.text}"

        return string

