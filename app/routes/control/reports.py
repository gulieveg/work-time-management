from flask import Blueprint

from app.db import DatabaseManager

reports_bp: Blueprint = Blueprint("reports", __name__, url_prefix="/reports")
db_manager: DatabaseManager = DatabaseManager()
