from datetime import timedelta
from random import random
import sys
from uuid import uuid4
from data import db_session
from data import Actions, Log, Tables, Operations, Permission, User, App, Event
from utils import get_datetime_now


def init_values():
    db_sess = db_session.create_session()

    user_admin = User(login="admin", name="Админ")
    user_admin.set_password("admin")
    db_sess.add(user_admin)
    db_sess.commit()

    permissions = []
    for operation in Operations.get_all():
        p = Permission(userId=user_admin.id, operation=operation)
        permissions.append(p)
        db_sess.add(p)
    db_sess.commit()

    log_changes(db_sess, user_admin, permissions)
    if "dev" in sys.argv:
        init_dev(db_sess)
    db_sess.close()


def log_changes(db_sess, user_admin, permissions):
    now = get_datetime_now()

    def log(tableName, record):
        db_sess.add(Log(
            date=now,
            actionCode=Actions.added,
            userId=user_admin.id,
            userName=user_admin.name,
            tableName=tableName,
            recordId=record.id,
            changes=record.get_creation_changes()
        ))

    log(Tables.User, user_admin)

    for permission in permissions:
        log(Tables.Permission, permission)

    db_sess.commit()


def init_dev(db_sess):
    app = App.new(db_sess, "Test app #1")
    app.code = "ABCD1234"
    Permission.new(db_sess, 1, Operations.view_app, 1)
    Permission.new(db_sess, 1, Operations.edit_app, 1)

    now = get_datetime_now()
    for _ in range(5):
        appUserId = str(uuid4())
        for t in range(4 * 24):
            if random() > 0.05:
                continue
            for m in range(60):
                if random() > 0.05:
                    continue
                event = Event(date=now - timedelta(minutes=t*60+m), actionCode="open", appCode=app.code, appUserId=appUserId)
                db_sess.add(event)

    db_sess.commit()
