from typing import Any

from starter_code.db import db


class UserModel(db.Model):
    __tablename__: str = 'users'
    
    id: Any = db.Column(db.Integer, primary_key=True)
    username: Any = db.Column(db.String(80))
    password: Any = db.Column(db.String())
    
    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password
        
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> Any:
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id: int) -> Any:
        return cls.query.filter_by(id=_id).first()
