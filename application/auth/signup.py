from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from datetime import datetime
from application.utils.encrypt_password import encrypt_password
from application.utils.generate_token import user_token
import traceback
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, template_id, dynamic_template_data
import random


Users = db["users"]
sg_api_key = os.environ.get('SENDGRID_API_KEY')
if not sg_api_key:
    # Handle missing API key appropriately
    print("SendGrid API key not found. Please set the SENDGRID_API_KEY environment variable.")
    # Exit or throw an exception as appropriate for your application
class Signup(Resource):
    def post(self):
        try:
            print("Sendgrid key", sg_api_key)
            data = request.json
            email = data['email']
            password = data['password']
            username = data['name']
            
            existing_user = Users.find_one({"email": email})
            
            if existing_user and existing_user.get("isVerified", False):
                return jsonify({"message": "User already exists"})
            
            hashed_password = encrypt_password(password)

            random_code = random.randint(1000, 9999)


            template_id = "d-e2edd4b1161b4a14b02e3a6da05b6f56"
            message = Mail(
                from_email="sales@codseed.com",
                to_emails=email,
                subject="Thanks for signup"
            )
            message.dynamic_template_data = {
                "code": f"{random_code}"
            }
            message.template_id = template_id

        

            sg = SendGridAPIClient(sg_api_key)
            response = sg.send(message)
            user = {
                "email": email,
                "username": username,
                "password": hashed_password,
                "role": "user",
                "isCreator": False,
                "isVerified": False,
                "isBanned": False,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "current_balance": 0,
                "transactionIds": [],
                "verification_code": random_code,

                
                }
            Users.insert_one(user)

            ret_json = {
                "message": "User created successfully",
                "status": 200,
            }
            return jsonify(ret_json)
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong"}), 500