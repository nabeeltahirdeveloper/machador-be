
from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
import traceback
Bot = db["bot"]






class AddBot(Resource):
    def post(self):
        try:
            data = request.json
            bot = data.get("bot", {})
            

            if not bot:
                return jsonify({"message": "bot is required"}), 400
            
            Bot.insert_one({
                "bot": bot,
                "created_at": datetime.now(),
                
            })

            ret_json = {
                "message": "Bot Details added successfully",
                "status": 200
            }
            



            return jsonify(ret_json)
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong"}), 500