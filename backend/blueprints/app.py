from flask import Blueprint, g, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session
from utils import get_json_values, permission_required, use_db_session, use_user
from data import Log, Actions, Tables
from data import User, Operations, Permission, App


blueprint = Blueprint("app", __name__)


@blueprint.route("/api/apps")
@jwt_required()
@use_db_session()
@use_user()
def apps(db_sess: Session, user: User):
    app_ids = map(lambda v: v.objectId, filter(lambda v: v.operation == Operations.view_app, user.permissions))
    apps = db_sess.query(App).filter(App.id.in_(app_ids), App.deleted == False).all()

    return jsonify(list(map(lambda v: v.get_dict(), apps))), 200


@blueprint.route("/api/app", methods=["POST"])
@jwt_required()
@use_db_session()
@use_user()
@permission_required(Operations.add_app)
def add_app(db_sess: Session, user: User):
    data, is_json = g.json
    if not is_json:
        return jsonify({"msg": "body is not json"}), 415

    (name,), values_error = get_json_values(data, "name")

    if values_error:
        return jsonify({"msg": values_error}), 400

    app = App.new(db_sess, name)
    Log.commit_with_log(db_sess, user, Actions.added, Tables.App, app)

    permission_view = Permission.new(db_sess, user.id, Operations.view_app, app.id)
    permission_edit = Permission.new(db_sess, user.id, Operations.edit_app, app.id)
    Log.commit_with_logs(db_sess, user, [
        (Actions.added, Tables.Permission, permission_view),
        (Actions.added, Tables.Permission, permission_edit),
    ])

    return jsonify(app.get_dict()), 200


@blueprint.route("/api/app/<int:app_id>")
@jwt_required()
@use_db_session()
@use_user()
@permission_required(Operations.view_app, "app_id")
def app(db_sess: Session, user: User, app_id: int):
    app = db_sess.query(App).filter(App.id == app_id).first()
    return jsonify(app.get_dict()), 200
