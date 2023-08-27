from sqlalchemy import Column, Integer, String
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import Session
from ..db_session import SqlAlchemyBase
from utils import randstr


class App(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "App"

    id   = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(8), nullable=False)
    code = Column(String(8), nullable=False)

    def __repr__(self):
        return f"<App> [{self.id}] {self.name}"

    def get_creation_changes(self):
        return [
            ("code", None, self.code),
            ("name", None, self.name),
        ]

    def get_dict(self):
        return self.to_dict(only=("id", "code", "name"))

    def gen_code(self, db_sess: Session):
        while True:
            code = randstr(8)
            existed = db_sess.query(App).filter(App.code == code).first()
            if not existed:
                self.code = code
                return

    @staticmethod
    def new(db_sess: Session, name: str):
        app = App(name=name)
        app.gen_code(db_sess)
        db_sess.add(app)
        return app
