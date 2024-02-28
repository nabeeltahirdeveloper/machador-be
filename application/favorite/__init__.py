from flask_restful import Api
from application import app
from .add_to_favorite   import AddToFavorite
from .get_all_favorite  import GetAllFavorite
from .remove_from_favorite import RemoveFromFavorite



api = Api(app)


api.add_resource(AddToFavorite, '/add_to_favorite')
api.add_resource(GetAllFavorite, '/get_all_favorite')
api.add_resource(RemoveFromFavorite, '/remove_from_favorite')