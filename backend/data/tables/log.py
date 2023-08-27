from sqlalchemy import Column, DateTime, ForeignKey, orm, Integer, String, JSON
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import Session
from data import User
from utils import get_datetime_now
from ..db_session import SqlAlchemyBase


class Log(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Log"

    id         = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    date       = Column(DateTime, nullable=False)
    actionCode = Column(String(16), nullable=False)
    userId     = Column(Integer, ForeignKey("User.id"), nullable=False)
    userName   = Column(String(64), nullable=False)
    tableName  = Column(String(16), nullable=False)
    recordId   = Column(Integer, nullable=False)
    changes    = Column(JSON, nullable=False)

    user = orm.relationship("User")

    def __repr__(self):
        return f"<Log> [{self.id}] {self.date} {self.actionCode}"

    @staticmethod
    def commit_with_log(db_sess: Session, user: User, actionCode, tableName, record):
        log = Log(
            date=get_datetime_now(),
            actionCode=actionCode,
            userId=user.id,
            userName=user.name,
            tableName=tableName,
            recordId=-1,
            changes=record.get_creation_changes()
        )
        db_sess.add(log)
        db_sess.commit()
        log.recordId = record.id
        db_sess.commit()

    @staticmethod
    def commit_with_logs(db_sess: Session, user: User, actionCode_tableName_record):
        logs = []
        for (actionCode, tableName, record) in actionCode_tableName_record:
            log = Log(
                date=get_datetime_now(),
                actionCode=actionCode,
                userId=user.id,
                userName=user.name,
                tableName=tableName,
                recordId=-1,
                changes=record.get_creation_changes()
            )
            db_sess.add(log)
            logs.append(log)
        db_sess.commit()
        for i in range(len(logs)):
            record = actionCode_tableName_record[i][2]
            logs[i].recordId = record.id
        db_sess.commit()

    # def get_dict(self):
    #     return self.to_dict(only=("name"))


class Actions:
    added = "added"
    updated = "updated"
    deleted = "deleted"
    restored = "restored"


class Tables:
    User = "User"
    Permission = "Permission"
    App = "App"
