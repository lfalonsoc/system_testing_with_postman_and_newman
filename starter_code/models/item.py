from typing import Any

from starter_code.db import db


class ItemModel(db.Model):
    __tablename__: str = 'items'

    id: Any = db.Column(db.Integer, primary_key=True)
    name: Any = db.Column(db.String(80))
    price: Any = db.Column(db.Float(precision=2))

    store_id: Any = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store: Any = db.relationship('StoreModel')

    def __init__(self, name: str, price: float, store_id: int) -> None:
        self.name: str = name
        self.price: float = price
        self.store_id: int = store_id

    def json(self) -> Any:
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name: str) -> Any:
        return cls.query.filter_by(name=name).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
