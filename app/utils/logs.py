from typing import Dict, Union

from flask import request
from flask_login import current_user


def get_user_and_request_log_info() -> Dict[str, Union[str, int]]:
    return {
        "user_id": current_user.id,
        "user_name": current_user.name,
        "ip_address": request.remote_addr,
        "platform": request.platform,
        "os_version": request.os_version,
        "browser": request.browser,
        "browser_version": request.browser_version,
    }


def get_log_data() -> Dict[str, Union[str, int]]:
    user_and_request_log_info: Dict[str, Union[str, int]] = get_user_and_request_log_info()
    return {
        "action": None,
        "entity_id": None,
        "entity_type": None,
        "user_id": user_and_request_log_info["user_id"],
        "user_name": user_and_request_log_info["user_name"],
        "ip_address": user_and_request_log_info["ip_address"],
        "platform": user_and_request_log_info["platform"],
        "os_version": user_and_request_log_info["os_version"],
        "browser": user_and_request_log_info["browser"],
        "browser_version": user_and_request_log_info["browser_version"],
    }
