
from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
from bson import ObjectId
import traceback

Bot = db["bot"]


class DeleteMultipleBotById(Resource):
    def delete(self):
        try:
            data = request.json
            ids = data
            if not ids:
                return jsonify({"message": "ids is required"}), 400
            
            new_bot_ids = []
            
            for id in ids:
                new_bot_ids.append(ObjectId(id))
            
            bot = Bot.delete_many({"_id": {"$in": new_bot_ids}})

            ret_json = {
                "message": "Bot deleted successfully",
                "status": 200
            }


       
            return jsonify(ret_json)


        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 400})