from .signup import Signup
from .login import Login
from flask_restful import Resource, Api
from application import app
from .delete_user import DeleteUser
from .get_users import GetUsers
from .update_users import UpdateUser
from .get_me import GetMe

api = Api(app)

api.add_resource(Signup, '/api/auth/signup')
api.add_resource(Login, '/api/auth/login')
api.add_resource(DeleteUser, '/api/auth/delete_users')
api.add_resource(GetUsers, '/api/auth/get_users')
api.add_resource(UpdateUser, '/api/auth/update_user')
api.add_resource(GetMe, '/api/auth/get_me')
