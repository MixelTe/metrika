from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import Session
from utils import get_datetime_now
from ..db_session import SqlAlchemyBase


class Event(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Event"

    id         = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    date       = Column(DateTime, nullable=False)
    actionCode = Column(String(32), nullable=False)
    appCode    = Column(String(8), nullable=False)
    appUserId  = Column(String(36), nullable=False)

    def __repr__(self):
        return f"<Event> [{self.id}] {self.date} {self.actionCode}"

    @staticmethod
    def new(db_sess: Session, actionCode, appCode, appUserId):
        event = Event(date=get_datetime_now(), actionCode=actionCode, appCode=appCode, appUserId=appUserId)
        db_sess.add(event)
        return event

    def get_dict(self):
        return self.to_dict(only=("id", "date", "actionCode", "appUserId"))
