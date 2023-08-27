from flask import Blueprint, jsonify


blueprint = Blueprint("docs", __name__)


@blueprint.route("/api")
def docs():
    return jsonify({
        "/api/auth POST": {
            "__desc__": "Get auth cookie",
            "request": {
                "login": "string",
                "password": "string",
            },
            "response": "User",
        },
        "/api/logout POST": {
            "__desc__": "Remove auth cookie",
        },
        "/api/user": {
            "__desc__": "Get current user",
            "response": "User",
        },
        "/api/apps": {
            "__desc__": "Get current user's apps",
            "response": "App[]",
        },
        "/api/app POST": {
            "__desc__": "Add new app",
            "request": {
                "name": "string",
            },
            "response": "App",
        },
        "User": {
            "id": "number",
            "name": "string",
            "login": "string",
            "operations": "string[]",
        },
        "App": {
            "id": "number",
            "code": "string",
            "name": "string",
        },
    }), 200
