from flask import Flask, render_template
from werkzeug.exceptions import NotFound, ServiceUnavailable


class DatabaseUnavailable(Exception):
    pass


def handle_error_404(app: Flask) -> callable:
    @app.errorhandler(404)
    def page_not_found(error: NotFound) -> str:
        return render_template("errors/404.html"), 404

    return page_not_found


def handle_error_503(app: Flask) -> callable:
    @app.errorhandler(DatabaseUnavailable)
    def service_unavailable(error: ServiceUnavailable) -> str:
        return render_template("errors/503.html"), 503

    return service_unavailable
