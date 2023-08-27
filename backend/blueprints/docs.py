from flask import Blueprint, jsonify


blueprint = Blueprint("docs", __name__)


@blueprint.route("/api")
def docs():
    return jsonify({
        "/api/auth POST": {
            "__desc__": "Get auth cookie",
            "__perm__": "None",
            "request": {
                "login": "string",
                "password": "string",
            },
            "response": "User",
        },
        "/api/logout POST": {
            "__desc__": "Remove auth cookie",
            "__perm__": "None",
        },
        "/api/user": {
            "__desc__": "Get current user",
            "__perm__": "auth",
            "response": "User",
        },
        "/api/apps": {
            "__desc__": "Get current user's apps",
            "__perm__": "auth",
            "response": "App[]",
        },
        "/api/app/<app_id:int>": {
            "__desc__": "Get app by id",
            "__perm__": "view_app/<app_id>",
            "response": "App",
        },
        "/api/app POST": {
            "__desc__": "Add new app",
            "__perm__": "add_app",
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
