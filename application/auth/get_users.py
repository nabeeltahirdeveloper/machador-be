
from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from traceback import format_exc
from math import ceil
from application.utils.generate_filter_object import generate_filter_object

Users = db["users"]

class GetUsers(Resource):
    def get(self):
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))
            filter_obj = generate_filter_object(request.args.get("filter", "").split(","))

            total_count = Users.count_documents(filter_obj)
            last_page = ceil(total_count / limit)
            users = Users.find(filter_obj).skip((page - 1) * limit).limit(limit)
            ret_json = []
            for user in users:
                user['_id'] = str(user['_id'])
                # del user['_id']
                del user['password']
                ret_json.append(user)

                
            
            return jsonify({
                "message": "Users fetched successfully",
                "status": 200,
                "users": ret_json,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total_count": total_count,
                    "last_page": last_page
                }
            })
        except Exception as e:
            print(format_exc())
            return jsonify({"message": "Something went wrong"}), 500