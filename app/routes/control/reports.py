from flask import Blueprint

reports_bp: Blueprint = Blueprint("reports", __name__, url_prefix="/reports")
