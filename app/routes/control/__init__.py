from flask import Blueprint

from .employees import employees_bp
from .home import home_bp
from .logs import logs_bp
from .orders import orders_bp
from .users import users_bp
from .works import works_bp

control_bp: Blueprint = Blueprint("control", __name__, url_prefix="/control")

control_bp.register_blueprint(employees_bp)
control_bp.register_blueprint(home_bp)
control_bp.register_blueprint(logs_bp)
control_bp.register_blueprint(orders_bp)
control_bp.register_blueprint(users_bp)
control_bp.register_blueprint(works_bp)
