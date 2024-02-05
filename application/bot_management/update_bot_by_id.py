
from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
from bson import ObjectId
import traceback
Bot = db["bot"]




class UpdateBotById(Resource):
    def put(self):
        try:
            data = request.json
            bot_id = data.get("_id", "")
            bot = data.get("bot", {})

            



            if not bot_id:
                return jsonify({"message": "bot_id is required"}), 400
            
            bot_data = {
                "bot": bot,
                "updated_at": datetime.now()
            }
            Bot.update_one({"_id": ObjectId(bot_id)}, {"$set": bot_data})







            ret_json = {
                "message": "bot Details updated successfully",
                "status": 200
            }
            return jsonify(ret_json)
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong"}), 500