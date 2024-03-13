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


class GetAllFavorite(Resource):
    @jwt_required()
    def get(self):
        try:

            email = get_jwt_identity().get("username")
            print(email)

            
            
            bots = Bot.find({"email": email, "isFavorite": True}, {
                "_id": 1,
                "bot_name": 1,
                "bot_profile": 1,
            })


            bot_list = []

            for bot in bots:
                print(bots)
                bot["_id"] = str(bot["_id"])
                bot_list.append(bot)

            return jsonify({"message": "Bot get successfully in favorite", "status": 200, "data": bot_list})

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 500})


