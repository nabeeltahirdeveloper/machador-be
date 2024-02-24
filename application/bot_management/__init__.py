from application import app
from flask_restful import Api
from .add_bot import AddBot , GetBot
from .delete_bot_by_id import DeleteBotById
from .delete_multiple_bot import DeleteMultipleBotById
from .get_all_bot import GetAllBot
from .get_bot_by_id import GetBotById
from .update_bot_by_id import UpdateBotById


api = Api(app)


api.add_resource(AddBot, '/add_bot')
api.add_resource(GetBot, '/get_bot')
api.add_resource(DeleteBotById, '/delete_bot_by_id')
api.add_resource(DeleteMultipleBotById, '/delete_multiple_bot')
api.add_resource(GetAllBot, '/get_all_bot')
api.add_resource(GetBotById, '/get_bot_by_id')
api.add_resource(UpdateBotById, '/update_bot_by_id')
