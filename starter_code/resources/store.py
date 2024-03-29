from typing import Any, Dict, List

from flask_restful import Resource

from starter_code.models.store import StoreModel


class Store(Resource):
    def get(self, name: str) -> Any:
        store: Any = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name: str) -> Any:
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store: StoreModel = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name: str) -> Any:
        store: Any = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self)-> Dict[str, List[Any]]:
        return {'stores': [store.json() for store in StoreModel.query.all()]}
