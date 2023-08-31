from datetime import timedelta
import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import text
from sqlalchemy.orm import Session
from utils import get_datetime_now, parse_date, parse_int, permission_required, switch_value, use_db_session, use_user
from data import User, Operations, App


blueprint = Blueprint("stats", __name__)


@blueprint.route("/api/stats/<int:app_id>")
@jwt_required()
@use_db_session()
@use_user()
@permission_required(Operations.view_app, "app_id")
def stats(db_sess: Session, user: User, app_id: int):
    app = db_sess.query(App).filter(App.id == app_id).first()
    if app is None:
        return jsonify({"msg": f"app with id [{app_id}] not found"}), 400

    only_new, _ = parse_int(request.args.get("new", None))
    if only_new != 1:
        only_new = 0

    group = request.args.get("group", "minute")
    divider = switch_value(group, [
        ("day", 24 * 60 * 60),
        ("hour", 60 * 60),
        ("minute", 10 * 60),
    ])

    visit_time, is_int = parse_int(request.args.get("visitTime", None))
    if not is_int or visit_time < 10:
        visit_time = 10

    end, is_date = parse_date(request.args.get("end", None))
    if not is_date:
        end = get_datetime_now()
    start, is_date = parse_date(request.args.get("start", None))
    if not is_date:
        start = end - timedelta(days=14)

    stats_type = request.args.get("type", "requests")
    sql = switch_value(stats_type, [
        ("visitors",
            """Select Count(c) as c, date
               From (
                    Select Count(id) as c, strftime("%Y-%m-%dT%H:%M", date) as date
                    From Event
                    Where appCode = :appCode And date Between :start And :end And (isNew = :onlyNew Or isNew = 1)
                    Group By strftime("%s", date) / :divider, appUserId
               )
               Group By strftime("%s", date) / :divider
               Order by date ASC
            """),
        ("visits",
            """Select Count(c) as c, date
               From (
                    Select Count(id) as c, strftime("%Y-%m-%dT%H:%M", date) as date
                    From Event
                    Where appCode = :appCode And date Between :start And :end And (isNew = :onlyNew Or isNew = 1)
                    Group By strftime("%s", date) / :visitDivider, appUserId
               )
               Group By strftime("%s", date) / :divider
               Order by date ASC
            """),
        ("fromTag",
            """Select fromTag, json_group_array(json_object(
                   'c', c,
                   'date', date
               )) as json
               From (
                   Select Count(c) as c, date, fromTag
                   From (
                       Select Count(id) as c, strftime("%Y-%m-%dT%H:%M", date) as date, appUserId, fromTag
                       From Event
                       Where appCode = :appCode And date Between :start And :end And (isNew = :onlyNew Or isNew = 1)
                       Group By strftime("%s", date) / :divider, appUserId, fromTag
                   )
                   Group By strftime("%s", date) / :divider, fromTag
                   Order by date ASC
               )
               Group By fromTag
               Order by fromTag ASC
            """),
        ("requests",
            """Select Count(id) as c, strftime("%Y-%m-%dT%H:%M", date) as date
               From Event
               Where appCode = :appCode And date Between :start And :end And (isNew = :onlyNew Or isNew = 1)
               Group By strftime("%s", date) / :divider
               Order by date ASC
            """),
    ])

    events = db_sess.execute(text(sql), {
        "appCode": app.code,
        "divider": divider,
        "visitDivider": visit_time * 60,
        "start": start.isoformat().replace("T", " "),
        "end": end.isoformat().replace("T", " "),
        "onlyNew": only_new,
    })

    format_date = switch_value(group, [
        ("day", lambda date: date[:-5] + "00:00"),
        ("hour", lambda date: date[:-2] + "00"),
        ("minute", lambda date: date[:-1] + "0"),
    ])

    if stats_type == "fromTag":
        return jsonify(list(map(lambda v: {
            "label": v.fromTag,
            "values": list(map(lambda v: {
                "date": format_date(v["date"]),
                "count": v["c"],
            }, json.loads(v.json)))
        }, filter(lambda v: v.fromTag != "", events)))), 200

    return jsonify([{
        "label": stats_type,
        "values": list(map(lambda v: {
            "date": format_date(v.date),
            "count": v.c,
        }, events))
    }]), 200


@blueprint.route("/api/stats/visitors/<int:app_id>")
@jwt_required()
@use_db_session()
@use_user()
@permission_required(Operations.view_app, "app_id")
def visitors(db_sess: Session, user: User, app_id: int):
    app = db_sess.query(App).filter(App.id == app_id).first()
    if app is None:
        return jsonify({"msg": f"app with id [{app_id}] not found"}), 400

    only_new, _ = parse_int(request.args.get("new", None))
    if only_new != 1:
        only_new = 0

    end, is_date_end = parse_date(request.args.get("end", None))
    start, is_date_start = parse_date(request.args.get("start", None))

    sql = """Select Count(id) as c
             From Event
             Where appCode = :appCode
          """
    if is_date_end and is_date_start:
        sql += " And date Between :start And :end\n"
    if only_new:
        sql += " And isNew = 1\n"
    sql += "Group By appUserId"

    sql = "Select Count(c) as c From (" + sql + ")"

    visitors = db_sess.execute(text(sql), {
        "appCode": app.code,
        "start": start.isoformat().replace("T", " ") if is_date_end else "",
        "end": end.isoformat().replace("T", " ") if is_date_start else "",
    }).first().c

    return jsonify(visitors), 200
