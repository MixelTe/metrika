import sys
import os


def init_values():
    add_parent_to_path()
    if not os.path.exists("db"):
        os.makedirs("db")

    from data import db_session
    from data import Actions, Log, Tables
    from data import Operation, Operations
    from data import Permission
    from data import Role
    from data import User
    from utils import get_datetime_now

    ROLES = {
        "Viewer": [
            Operations.view,
        ],
    }

    def init():
        db_session.global_init("db/TicketSystem.db")
        db_sess = db_session.create_session()

        for operation in Operations.get_all():
            db_sess.add(Operation(id=operation[0], name=operation[1]))

        roles = []
        for role_name in ROLES:
            role = Role(name=role_name)
            roles.append(role)
            db_sess.add(role)
            db_sess.commit()

            for operation in ROLES[role_name]:
                db_sess.add(Permission(roleId=role.id, operationId=operation[0]))

        role_admin = Role(name="Admin")
        roles.append(role_admin)
        db_sess.add(role_admin)
        db_sess.commit()

        for operation in Operations.get_all():
            db_sess.add(Permission(roleId=role_admin.id, operationId=operation[0]))

        user_admin = User(login="admin", name="Админ", roleId=role_admin.id)
        user_admin.set_password("admin")
        db_sess.add(user_admin)
        db_sess.commit()

        log_changes(db_sess, user_admin, roles)

    def log_changes(db_sess, user_admin, roles):
        now = get_datetime_now()

        def log(tableName, recordId, changes):
            db_sess.add(Log(
                date=now,
                actionCode=Actions.added,
                userId=user_admin.id,
                userName=user_admin.name,
                tableName=tableName,
                recordId=recordId,
                changes=changes
            ))

        log(Tables.User, user_admin.id, user_admin.get_creation_changes())

        for role in roles:
            log(Tables.Role, role.id, role.get_creation_changes())

        db_sess.commit()

    init()


def add_parent_to_path():
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)


init_values()
