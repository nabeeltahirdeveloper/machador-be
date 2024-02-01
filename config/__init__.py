from os import environ
from os.path import abspath
from os.path import dirname
from os.path import join

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

path = dirname(abspath(__file__))
environment = environ.get('ENVIRONMENT', 'development')
load_dotenv(join(path, f'{environment}.env'))


class Config(BaseSettings):
    """It will automatically read environment variables into fields.
    """

    environment: str = "production"
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    jwt_secret_key: str = "change-me"
    refresh_exp_length: int = 60
    access_exp_length: int = 30
    jwt_expiry_time: int = 900
    sentry_dsn: str = ""
    db_username: str = ""
    db_password: str = ""
    db_host: str = ""
    db_port: int = 27017
    db_name: str = ""
    


config = Config()