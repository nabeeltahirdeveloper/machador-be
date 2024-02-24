from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
import hashlib
import traceback
from datetime import datetime
from application.utils.aes_encryption import encrypt_aes, decrypt_aes
from Crypto.Random import get_random_bytes
from cloudinary import uploader

Bot = db["bot"]

def is_pdf(file):
    """Check if the file is a PDF by reading the first 4 bytes for the PDF header '%PDF'."""
    try:
        
        header = file.read(4)
        file.seek(0)  # Reset file pointer to the beginning.
        return header == b'%PDF'
    except Exception as e:
        print(traceback.format_exc())
        return False


def encrypt_string(input_string):
    """Encrypt a string using SHA256."""
    return hashlib.sha256(input_string.encode()).hexdigest()

def generate_aes_key():
    return get_random_bytes(16)  # AES key size could be 16 (AES-128), 24 (AES-192), or 32 (AES-256) bytes long.



aes_key = b'\xb3\xb8(\x8a\xbe0\xa8\x8d\xbe+[\xca{@\xb1\x1d'  # Generate a random AES key for encryption
print(f"AES Key: {aes_key}")
class AddBot(Resource):
    def post(self):
        try:
            files = request.files.getlist("file")
            encrypted_files = []
            for file in files:
                if is_pdf(file):
                    content = file.read()
                    iv, encrypted_content = encrypt_aes(content, aes_key)  # No need to encode
                    encrypted_files.append({"iv": iv, "content": encrypted_content})



            bot_profile = request.files.get("bot_profile")
            if not bot_profile:
                return jsonify({"message": "Bot profile is required", "status": 400})

            data = request.form.to_dict()
            bot_name = data.get("bot_name", "no-name")
            bot_prompt = data.get("bot_prompt", "no-prompt")
            upload_result = uploader.upload(bot_profile)
            profile_url = upload_result.get('url')  # Get the URL of the uploaded image

            # Encrypt the bot_prompt using AES
            iv, encrypted_bot_prompt = encrypt_aes(bot_prompt, aes_key)

            bot_details = {
                "bot_name": bot_name,
                "bot_profile": profile_url,
                "encrypted_bot_prompt": encrypted_bot_prompt,
                "iv": iv,  # Store IV alongside encrypted data
                "encrypted_files": encrypted_files,
                "creation_date": datetime.now()
            }
            Bot.insert_one(bot_details)

            return jsonify({"message": "Bot Details added successfully", "status": 200})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 500})


class GetBot(Resource):
    def get(self):
        try:
            bots = Bot.find({}, {"_id": 0, "bot_name": 1, 'creation_date': 1, 'bot_profile': 1})
            decrypted_bots = []

            for bot in bots:
                # decrypted_prompt = decrypt_aes(bot["encrypted_bot_prompt"], bot["iv"], aes_key)  # Decrypt prompt
                
                bot_data = {
                    "bot_name": bot["bot_name"],
                    # "decrypted_prompt": decrypted_prompt.decode('utf-8'),
                    "creation_date": bot["creation_date"],
                    "bot_profile": bot["bot_profile"],
                    # Include other necessary fields
                }
                decrypted_bots.append(bot_data)


            return jsonify({"bots": decrypted_bots, "status": 200})
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 500})
