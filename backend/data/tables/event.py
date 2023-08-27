from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy_serializer import SerializerMixin
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

    # def get_dict(self):
    #     return self.to_dict(only=("name"))
