

from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
from bson import ObjectId
import traceback

Bot = db["bot"]


class GetBotById(Resource):
    def post(self):
        try:
            data = request.json
            bot_id = data.get("bot_id" , None)

            if not bot_id:
                return jsonify({"message": "bot_id is required", "status": 400})

            bot = Bot.find_one({"_id": ObjectId(bot_id)})
            if not bot:
                return jsonify({"message": "bot not found", "status": 400})
            

            bot["_id"] = str(bot["_id"])


            ret_json = {
                "message": "bot details fetched successfully",
                "status": 200,
                "bot": bot
            }

            return jsonify(ret_json)


        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 400})