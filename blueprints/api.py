from datetime import timedelta
from uuid import uuid4
from flask import Blueprint, g, jsonify, make_response, request, url_for
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session
from utils import get_datetime_now, get_json_values, load_file, parse_int, use_db_session, use_user
from data import User, Event


blueprint = Blueprint("api", __name__)
script_js = load_file("static/script.js")


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

    isNew = False
    appUserId = request.cookies.get("userId", None)
    if appUserId is None:
        appUserId = str(uuid4())
        isNew = True
    else:
        isNew = db_sess.query(Event).filter(Event.appCode == app_code, Event.appUserId == appUserId).first() is None

    event = Event.new(db_sess, "open", app_code, appUserId, isNew)
    db_sess.commit()

    script_js = load_file("static/script.js")  # dev
    res = script_js
    res = res.replace("\"%eventId%\"", str(event.id))
    res = res.replace("\"%url%\"", '"' + url_for("docs.docs", _external=True) + '"')
    res = res.replace("\"%appCode%\"", f'"{app_code}"')
    res = make_response(res)
    res.set_cookie("userId", appUserId, max_age=31536000, samesite="None", secure=True)
    return res


@blueprint.route("/api/script/onopen", methods=["OPTIONS"])
def script_onopen_options():
    g.no_cors = True
    return "ok"


@blueprint.route("/api/script/onopen", methods=["POST"])
@use_db_session()
def script_onopen(db_sess: Session):
    g.no_cors = True

    data, is_json = g.json
    if not is_json:
        return jsonify({"msg": "body is not json"}), 415

    (event_id, from_tag, page), values_error = get_json_values(data, "eventId", "fromTag", "page")

    if values_error:
        return jsonify({"msg": values_error}), 400

    appUserId = request.cookies.get("userId", None)

    if type(event_id) != int or event_id < 0 or appUserId is None:
        return jsonify({"msg": "wrong eventId"}), 400

    event = db_sess.query(Event).filter(Event.id == event_id, Event.appUserId == appUserId).first()

    now = get_datetime_now().replace(tzinfo=None)
    if event is None or now - event.date > timedelta(minutes=5):
        return jsonify({"msg": "wrong eventId"}), 400

    event.fromTag = from_tag
    event.page = page
    db_sess.commit()
    return jsonify({"msg": "ok"}), 200


@blueprint.route("/api/script/event", methods=["OPTIONS"])
def script_pagechange_options():
    g.no_cors = True
    return "ok"


@blueprint.route("/api/script/event", methods=["POST"])
@use_db_session()
def script_pagechange(db_sess: Session):
    g.no_cors = True

    data, is_json = g.json
    if not is_json:
        return jsonify({"msg": "body is not json"}), 415

    (app_code, event, from_tag, page), values_error = get_json_values(data, "appCode", "event", "fromTag", "page")

    if values_error:
        return jsonify({"msg": values_error}), 400

    appUserId = request.cookies.get("userId", None)

    if appUserId is None:
        return jsonify({"msg": "no userId"}), 400

    if event not in ["page"]:
        return jsonify({"msg": "wrong event"}), 400

    event = Event.new(db_sess, event, app_code, appUserId, False)
    event.fromTag = from_tag
    event.page = page
    db_sess.commit()

    return jsonify({"msg": "ok"}), 200
