from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password, check_password
from application.utils.generate_token import user_token

Users = db["users"]

class Login(Resource):
    """
        Your GET method description
        ---
        responses:
          200:
            description: A successful response
        """
    def post(self):
        try:
            data = request.json
            email = data['email']
            password = data['password']
            
            user = Users.find_one({"email": email})
            if not user:
                return jsonify({"message": "Incorrect email or password", "status": 400})
            
            hashed_password = user["password"]
            if not check_password(password, hashed_password):
                return jsonify({"message": "Incorrect email or password" , "status": 400})
            
            access_token = user_token(email)

            ret_json = {
                "message": "User login successfully",
                "status": 200,
                "access_token": access_token
            }
            return jsonify(ret_json)
        except Exception as e:
            return jsonify({"message": "Something went wrong"}), 500