from flask_restful import Resource, request, abort
from config.db import db
import traceback

Users = db["users"]

class VerifyUser(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)  # Ensures that data is parsed as JSON
  
            email = data.get('email')
            code = data.get('code')
            
            if not email or not code:
                abort(400, message="Invalid data")
            
            user = Users.find_one({"email": email})
            if not user:
                abort(404, message="User not found")
            
            if user.get("verification_code") != int(code):
                return {"Status": 400, "message":"Invalid code"}
            
            Users.update_one({"email": email}, {"$set": {"isVerified": True}})
            
            return {"message": "User verified successfully", "status": 200}
        except Exception:
            print(traceback.format_exc())
            abort(500, message="Something went wrong")
