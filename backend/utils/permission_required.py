from flask import jsonify
from data import User
from functools import wraps


def permission_required(operation, objectIdField=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if "user" in kwargs:
                user: User = kwargs["user"]
            else:
                return jsonify({"msg": "permission_required: no user"}), 500

            objectId = kwargs[objectIdField] if objectIdField is not None else None
            if not user.check_permission(operation, objectId):
                return jsonify({"msg": "No permission"}), 403
            
            return fn(*args, **kwargs)

        return decorator

    return wrapper
