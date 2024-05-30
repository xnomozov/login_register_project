from typing import Optional

from models import User


class Session:
    instance = None
    user: User = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self, session: User | None = None):
        if not hasattr(self, 'session'):
            self.session = session

    def add_session(self, user: User):
        self.session = user
        Session.user = user

    def check_session(self):
        return self.session
