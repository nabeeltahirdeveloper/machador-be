from pymongo import MongoClient
from config import config
from dotenv import load_dotenv
import os
load_dotenv()

# DB_NAME = config.db_name
DB_NAME = "qafila"
DB_HOST = os.getenv("DB_HOST_NAME")
DB_PORT = config.db_port
DB_USER = config.db_username
DB_PASS = config.db_password

connection = MongoClient(DB_HOST)
admin_db = connection.admin

# Check the status of the replica set
repl_status = admin_db.command("replSetGetStatus")
print("replica status", repl_status)
# Check if there is no primary member
if repl_status["myState"] != 1:
    print("replica status", repl_status)
    # Initiate a primary election
    admin_db.command("replSetStepDown", primaryStepDownWaitTime=10)
    admin_db.command("replSetElect")
# db = connection.resumas
db = connection[DB_NAME]
# db.authenticate()