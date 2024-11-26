import os
import pymongo
import secrets
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")



    
TITLE: str = "SCMXpertLite"
DESCRIPTION: str = """SCMXpertLite  created in FastAPI"""
PROJECT_VERSION: str = "1.0.0"
MONGODB_USER = os.getenv("mongodb_user")
MONGODB_PASSWORD = os.getenv("mongodb_password")

CLIENT = pymongo.MongoClient(os.getenv("mongouri"))
database = CLIENT[os.getenv("DB_NAME")]

Shipments=database['shipments']
User_details=database["user_details"]
Devicedata=database['devicedata']

ACCESS_TOKEN_EXPIRE_MINUTES= 30
SECRET_KEY=secrets.token_hex(32)
ALGORITHM = "HS256"

   

