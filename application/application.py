from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config["JWT_SECRET_KEY"] =os.getenv("JWT_SECRET_KEY")  # Change this!
jwt = JWTManager(app)

SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'application/static/swagger.json'  # URL for exposing the Swagger specification

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Qafila API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

