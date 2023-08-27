from data import db_session
from data import Actions, Log, Tables, Operations, Permission, User
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
