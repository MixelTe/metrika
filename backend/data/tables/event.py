from flask import request
from sqlalchemy import Boolean, Column, DateTime, DefaultClause, Integer, String
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import Session
from utils import get_datetime_now
from ..db_session import SqlAlchemyBase


class Event(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Event"

    id          = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    date        = Column(DateTime, nullable=False)
    actionCode  = Column(String(32), nullable=False)
    appCode     = Column(String(8), nullable=False)
    appUserId   = Column(String(36), nullable=False)
    isNew       = Column(Boolean, DefaultClause("0"), nullable=False)
    remote_addr = Column(String(96), DefaultClause(""), nullable=False)
    language    = Column(String(96), DefaultClause(""), nullable=False)
    user_agent  = Column(String(160), DefaultClause(""), nullable=False)
    is_desktop  = Column(Boolean, DefaultClause("1"), nullable=False)
    page        = Column(String(128), DefaultClause(""), nullable=False)
    fromTag     = Column(String(64), DefaultClause(""), nullable=False)

    def __repr__(self):
        return f"<Event> [{self.id}] {self.date} {self.actionCode}"

    @staticmethod
    def new(db_sess: Session, actionCode, appCode, appUserId, isNew):
        remote_addr = request.remote_addr
        language = request.accept_languages.to_header()
        user_agent = request.user_agent.string
        is_desktop = "Mobi" not in user_agent
        event = Event(date=get_datetime_now(), actionCode=actionCode, appCode=appCode, appUserId=appUserId,
                      isNew=isNew, remote_addr=remote_addr, language=language, is_desktop=is_desktop, user_agent=user_agent)
        db_sess.add(event)
        return event

    def get_dict(self):
        return self.to_dict(only=("id", "date", "actionCode", "appUserId"))
