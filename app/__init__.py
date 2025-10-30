import datetime
import json
from typing import Dict, Optional, Tuple, Union

from decouple import config
from flask import Flask
from flask_login import LoginManager

from .db import DatabaseManager
from .middlewares import register_middlewares
from .models import User
from .routes import register_routes
from .utils import MESSAGES, encoding, register_error_handlers, register_template_filters

login_manager: LoginManager = LoginManager()
db_manager: DatabaseManager = DatabaseManager()


@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    user_data: Optional[Tuple[str]] = db_manager.users.get_user_data_by_id(user_id)
    if user_data is None:
        return None
    return User(*user_data)


def load_settings() -> Dict[str, Union[bool, str, int]]:
    with open(file="config.json", mode="r") as file:
        data: Dict[str, Dict[str, Union[bool, str, int]]] = json.load(file)
    config_mode: str = encoding.decode_base64(config("APP_ENV"))
    return data[config_mode]


def create_app() -> Flask:
    app: Flask = Flask(__name__, static_folder="static", template_folder="templates")

    app.secret_key = encoding.decode_base64(config("APP_SECRET_KEY"))
    app.config["MAINTENANCE_MODE"] = False

    app.permanent_session_lifetime = datetime.timedelta(hours=9)

    register_template_filters(app)
    register_routes(app)
    register_middlewares(app)
    register_error_handlers(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = MESSAGES["auth"]["login_required"]
    login_manager.login_message_category = "info"
    return app
