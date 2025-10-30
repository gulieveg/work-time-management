from flask_login import UserMixin


class User(UserMixin):
    def __init__(
        self,
        user_id: str,
        name: str,
        department: str,
        login: str,
        permissions_level: str,
        is_enabled: int,
        is_factory_worker: int,
    ) -> None:
        self.id: str = user_id
        self.name: str = name
        self.department: str = department
        self.login: str = login
        self.permissions_level: str = permissions_level
        self.is_enabled: int = is_enabled
        self.is_factory_worker: int = is_factory_worker
