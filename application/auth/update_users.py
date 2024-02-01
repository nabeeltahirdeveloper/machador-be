
from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
import traceback
from bson import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required

Users = db["users"]

class UpdateUser(Resource):
    # @jwt_required
    def put(self):
        try:
            data = request.json
    #         {
    #     "created_at": "Sun, 12 Nov 2023 19:07:47 GMT",
    #     "current_balance": 0,
    #     "email": "nabeeltahiroffice@gmail.com",
    #     "isBanned": false,
    #     "isCreator": false,
    #     "isVerified": false,
    #     "role": "user",
    #     "transactionIds": [],
    #     "updated_at": "Sun, 12 Nov 2023 19:07:47 GMT",
    #     "username": "mewo"
    # },
            email = data.get('email', None)
            current_balance = data.get('current_balance', None)
            isBanned = data.get('isBanned', None)
            isCreator = data.get('isCreator', None)
            isVerified = data.get('isVerified', None)
            role = data.get('role', None)
            transactionIds = data.get('transactionIds', None)
            username = data.get('user_name', None)
            user_id = data.get('_id', None)
            
            
            updatedData ={}

            if email:
                updatedData['email'] = email
            if current_balance:
                updatedData['current_balance'] = current_balance
            if isBanned is not None:
                updatedData['isBanned'] = isBanned
            if isCreator is not None:
                updatedData['isCreator'] = isCreator
            if isVerified is not None:
                updatedData['isVerified'] = isVerified
            if role:
                updatedData['role'] = role
            if transactionIds:
                updatedData['transactionIds'] = transactionIds
            if username:
                updatedData['user_name'] = username
            updatedData['updated_at'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

            


            update_user = Users.update_one({"_id": ObjectId(user_id)}, {"$set": updatedData})

            ret_json = {
                "message": "User updated successfully",
                "status": 200,
            }
            
            
            return jsonify(ret_json)
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong"}), 500