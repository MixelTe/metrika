from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import Session
from ..db_session import SqlAlchemyBase


class Permission(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Permission"

    userId    = Column(Integer, ForeignKey("User.id"), primary_key=True)
    operation = Column(String(32), primary_key=True)
    objectId  = Column(Integer, default=-1, primary_key=True)

    def __repr__(self):
        return f"<Permission> {self.userId} {self.operation}"

    @property
    def id(self):
        if self.objectId > 0:
            return f"{self.userId}-{self.operation}-{self.objectId}"
        return f"{self.userId}-{self.operation}"

    def get_creation_changes(self):
        return []

    def to_string(self):
        if self.objectId > 0:
            return f"{self.operation}-{self.objectId}"
        return self.operation

    @staticmethod
    def new(db_sess: Session, user_id: int, operation: str, objectId: int):
        permission = Permission(userId=user_id, operation=operation, objectId=objectId)
        db_sess.add(permission)
        return permission


class Operations:
    view_app = "view_app"
    add_app = "add_app"
    edit_app = "edit_app"

    def get_all():
        obj = Operations()
        members = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]
        return map(lambda x: getattr(obj, x), members)
