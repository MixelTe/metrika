from flask import jsonify
from data import User
from functools import wraps


def permission_required(operation):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if "user" in kwargs:
                user: User = kwargs["user"]
            else:
                return jsonify({"msg": "permission_required: no user"}), 500

            if not user.check_permission(operation):
                return jsonify({"msg": "No permission"}), 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper
