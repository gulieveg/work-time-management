from typing import Callable, Optional

from flask import Flask, request
from user_agents import parse
from user_agents.parsers import UserAgent


def store_user_agent_info(app: Flask) -> Callable:
    @app.before_request
    def wrapper() -> None:
        user_agent: UserAgent = parse(request.user_agent.string)

        request.platform = user_agent.os.family
        request.os_version = ".".join(map(str, user_agent.os.version))
        request.browser = user_agent.browser.family
        request.browser_version = ".".join(map(str, user_agent.browser.version))

    return wrapper
