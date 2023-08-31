import sys


def add_permission(login, permission, obj="-1"):
    add_parent_to_path()
    from data import db_session
    from data import User, Permission

    db_session.global_init("db/Metrika.db")
    session = db_session.create_session()
    user = session.query(User).filter(User.login == login).first()
    if user is None:
        print("User does not exist")
        return
    Permission.new(session, user.id, permission, int(obj))
    session.commit()
    print("Permission added")


def add_parent_to_path():
    import os

    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)


if len(sys.argv) == 4:
    add_permission(sys.argv[1], sys.argv[2], sys.argv[3])
elif len(sys.argv) == 3:
    add_permission(sys.argv[1], sys.argv[2])
else:
    print("Add permission: login permission [obj]")
