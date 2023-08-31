from flask import Blueprint, jsonify


blueprint = Blueprint("docs", __name__)


@blueprint.route("/api")
def docs():
    return jsonify({
        "/api/script": {
            "__desc__": "Get script for web app",
            "__perm__": "None",
            "params": {
                "app": "string",
            },
            "response": "js script",
        },
        "/api/onopen": {
            "__desc__": "Add info to open event",
            "__perm__": "None",
            "request": {
                "eventId": "number",
                "fromTag": "string",
                "page": "string",
                "params": "string",
                "pageHash": "string",
            },
        },
        "/api/event": {
            "__desc__": "Send event",
            "__perm__": "None",
            "request": {
                "appCode": "string",
                "event": "string",
                "fromTag": "string",
                "page": "string",
                "params": "string",
                "pageHash": "string",
            },
        },
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
        "/api/stats/<int:app_id>": {
            "__desc__": "Get statistics",
            "__perm__": "view_app/<app_id>",
            "params": {
                "group": "'minute' | 'hour' | 'day'",
                "type": "'visitors' | 'visits' | 'requests' | 'fromTag'",
                "start": "datetime",
                "end": "datetime",
                "newVisitors": "boolean",
            },
            "response": "Stats[]",
        },
        "/api/stats/visitors/<int:app_id>": {
            "__desc__": "Get visitors count",
            "__perm__": "view_app/<app_id>",
            "params": {
                "start": "datetime",
                "end": "datetime",
                "newVisitors": "boolean",
            },
            "response": "number",
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
        "Stats": {
            "label": "string",
            "values": [{
                "count": "number",
                "date": "string",
            }],
        },
    }), 200
