from flask_restful import Api
from .previous_chat import GetPreviousChat
from .add_chat import AddChat
from application import app
api = Api(app)


api.add_resource(GetPreviousChat, "/get_previous_chat")
api.add_resource(AddChat, "/add_chat")

