from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token

Users = db["users"]

class Signup(Resource):
    def post(self):
        try:
            data = request.json
            email = data['email']
            password = data['password']
            
            existing_user = Users.find_one({"email": email})
            
            if existing_user:
                return jsonify({"message": "User already exists"})
            
            hashed_password = encrypt_password(password)
            
            user = {
                "email": email,
                "username": "",
                "password": hashed_password,
                "role": "user",
                "isCreator": False,
                "isVerified": False,
                "isBanned": False,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "current_balance": 0,
                "transactionIds": []

                
                }
            Users.insert_one(user)

            access_token = user_token(email)

            ret_json = {
                "message": "User created successfully",
                "status": 200,
                "access_token": access_token
            }
            return jsonify(ret_json)
        except Exception as e:
            return jsonify({"message": "Something went wrong"}), 500