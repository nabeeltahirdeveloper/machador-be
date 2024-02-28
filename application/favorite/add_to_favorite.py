from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
import hashlib
import traceback
from datetime import datetime
from application.utils.aes_encryption import encrypt_aes, decrypt_aes
from flask_jwt_extended import get_jwt_identity, jwt_required

Users = db["users"]
Bot = db["bot"]



class AddToFavorite(Resource):
    @jwt_required()
    def post(self):
        try:

            data = request.get_json()
            email = get_jwt_identity()
            bot_id = data.get("bot_id", None)

            if not bot_id:
                return jsonify({"message": "Bot ID is required", "status": 400})
            
            data = {
                "isFavorite": True
            }            
            Bot.update_one({"_id": bot_id}, {"$set": data})



            
            return jsonify({"message": "Bot  added successfully in favorite", "status": 200})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 500})


