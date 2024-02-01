
from flask import request, jsonify, make_response, abort
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from config.db import db

UsersDB = db['users']


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            cursor = UsersDB.find_one({"email": user_id})
          
            return fn(*args, **kwargs)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message":'Please login to access this route'}), 403)
    return wrapper