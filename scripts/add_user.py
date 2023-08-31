import sys


def add_user(login, password, name):
    add_parent_to_path()
    from data import db_session
    from data import User

    db_session.global_init("db/Metrika.db")
    user = User(login=login, name=name)
    user.set_password(password)

    session = db_session.create_session()
    session.add(user)
    session.commit()
    print("User added")


def add_parent_to_path():
    import os

    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)


if len(sys.argv) != 4:
    print("Add user: login password name")
else:
    add_user(sys.argv[1], sys.argv[2], sys.argv[3])
