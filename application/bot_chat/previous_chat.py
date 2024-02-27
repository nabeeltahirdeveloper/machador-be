from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
import hashlib
import traceback
from datetime import datetime
from application.utils.aes_encryption import encrypt_aes, decrypt_aes
from Crypto.Random import get_random_bytes
from cloudinary import uploader
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from bson import ObjectId

Bot = db["bot"]



aes_key = b'\xb3\xb8(\x8a\xbe0\xa8\x8d\xbe+[\xca{@\xb1\x1d'  # Generate a random AES key for encryption
print(f"AES Key: {aes_key}")
class GetPreviousChat(Resource):
    def post(self):
        try:
            data = request.get_json()
            bot_id = data.get("bot_id")


            if not bot_id:
                return jsonify({"message": "Bot ID is required", "status": 400})
            
            bot = Bot.find_one({"_id": ObjectId(bot_id)})
            if not bot:
                return jsonify({"message": "Bot not found", "status": 404})
            
            bot_data = {
                "previous_chat": bot.get("chat_history", []),
                "bot_id": str(bot.get("_id")),
                "bot_name": bot.get("bot_name"),


            }

            retJson = {
                "status": 200,
                "message": "Success",
                "data": bot_data
            }
            
            return jsonify(retJson)
            

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 500})

