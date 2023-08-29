from uuid import uuid4
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session
from utils import use_db_session, use_user
from data import User, Event


blueprint = Blueprint("api", __name__)


@blueprint.route("/api/user")
@jwt_required()
@use_db_session()
@use_user()
def user(db_sess: Session, user: User):
    return jsonify(user.get_dict()), 200


@blueprint.route("/api/script")
@use_db_session()
def script(db_sess: Session):
    app_code = request.args.get("app", None)
    if app_code is None or len(app_code) != 8:
        return jsonify({"msg": "wrong app code"}), 400

    appUserId = request.cookies.get("userId", None)
    if appUserId is None:
        appUserId = str(uuid4())

    Event.new(db_sess, "open", app_code, appUserId)
    db_sess.commit()

    res = make_response()
    res.set_cookie("userId", appUserId, max_age=31536000, samesite="None", secure=True)
    return res
