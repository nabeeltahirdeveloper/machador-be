
from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
from math import ceil
from application.utils.generate_filter_object import generate_filter_object

Bot = db["bot"]


class GetAllBot(Resource):
    def get(self):
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))
            filter_obj = generate_filter_object(request.args.get("filter", "").split(","))

            total_count = Bot.count_documents(filter_obj)
            last_page = ceil(total_count / limit)
            bot = Bot.find(
                filter_obj
            ).skip((page - 1) * limit).limit(limit)
            ret_json = []
            print(filter_obj)
            for bot_detail in bot:
                bot_detail["_id"] = str(bot_detail["_id"])
                ret_json.append(bot_detail)





            ret_json = {
                "message": "Bot details fetched successfully",
                "status": 200,
                "bot": ret_json,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total_count": total_count,
                    "last_page": last_page
                }
            }
            return jsonify(ret_json)
        except Exception as e:
            return jsonify({"message": "Something went wrong"}), 500