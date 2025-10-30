from flask import Blueprint

from .dashboard import dashboard_bp
from .employees import employees_bp
from .orders import orders_bp
from .users import users_bp

control_bp: Blueprint = Blueprint("control", __name__, url_prefix="/control")

control_bp.register_blueprint(dashboard_bp)
control_bp.register_blueprint(orders_bp)
control_bp.register_blueprint(users_bp)
control_bp.register_blueprint(employees_bp)
