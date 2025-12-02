from flask import Flask

from .maintenance import check_maintenance
from .user_agent import store_user_agent_info
from .user_status import check_user_status


def register_middlewares(app: Flask) -> None:
    check_maintenance(app)
    check_user_status(app)
    store_user_agent_info(app)
