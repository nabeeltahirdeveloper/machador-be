
from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
from application.wrappers import login_required
from flask_jwt_extended import get_jwt_identity, jwt_required

Users = db["users"]

class GetMe(Resource):
    @login_required
    def get(self):
        try:
            user = get_jwt_identity()

            users = Users.find_one({"email": user["username"]})
            users['_id'] = str(users['_id'])
            # del users['_id']
            del users['password']
            
            ret_json ={
                "user": users,
                "message": "User found",
                "status": 200
            }



                
            
            return jsonify(ret_json)
        except Exception as e:
            return jsonify({"message": "Something went wrong"}), 500