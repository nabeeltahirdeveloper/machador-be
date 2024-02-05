

from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
from bson import ObjectId
import traceback

Bot = db["bot"]


class DeleteBotById(Resource):
    def delete(self):
        try:
            data = request.json
            id = data.get("id", "")
            if not id:
                return jsonify({"message": "id is required"}), 400
            
            Bot.delete_one({"_id": ObjectId(id)})
            ret_json = {
                "message": "Bot deleted successfully",
                "status": 200
            }
            

            return jsonify(ret_json)


        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 400})