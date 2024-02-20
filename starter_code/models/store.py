from typing import Any

from starter_code.db import db


class StoreModel(db.Model):
    __tablename__: str = 'stores'

    id: Any = db.Column(db.Integer, primary_key=True)
    name: Any = db.Column(db.String(80))

    items: Any = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name: str) -> None:
        self.name: str = name

    def json(self) -> Any:
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name: str) -> Any:
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
