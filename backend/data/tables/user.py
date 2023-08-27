from sqlalchemy import DefaultClause, orm, Column, Integer, String, Boolean
from sqlalchemy_serializer import SerializerMixin
from ..db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "User"

    id       = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    deleted  = Column(Boolean, DefaultClause("0"), nullable=False)
    login    = Column(String(32), index=True, unique=True, nullable=False)
    name     = Column(String(32), nullable=False)
    password = Column(String(128), nullable=False)

    permissions = orm.relationship("Permission")

    def __repr__(self):
        return f"<User> [{self.id} {self.login}] {self.name}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_permission(self, operation):
        for permission in self.permissions:
            if permission.operation == operation:
                return True
        return False

    def get_creation_changes(self):
        return [
            ("login", None, self.login),
            ("name", None, self.name),
            ("password", None, "***"),
        ]

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "login": self.login,
            "operations": list(map(lambda v: v.operation, self.permissions)),
        }
