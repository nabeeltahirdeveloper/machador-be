
from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
from bson import ObjectId

Users = db["users"]

class DeleteUser(Resource):
    def delete(self):
        try:
            data = request.json
            ids = data
            
            newIds  = []
            for id in ids:
                newIds.append(ObjectId(id))

            Users.delete_many({"_id": {"$in": newIds}})


            ret_json = {
                "message": "User deleted successfully",
                "status": 200,
            }
            

                
            
            return jsonify(ret_json)
        except Exception as e:
            return jsonify({"message": "Something went wrong"}), 500