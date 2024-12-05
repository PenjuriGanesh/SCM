# import os
# import pymongo
# import secrets
# from dotenv import load_dotenv


# load_dotenv(dotenv_path=".env")

   
# TITLE: str = "SCMXpertLite"
# DESCRIPTION: str = """SCMXpertLite  created in FastAPI"""
# PROJECT_VERSION: str = "1.0.0"
# MONGODB_USER = os.getenv("mongodb_user")
# MONGODB_PASSWORD = os.getenv("mongodb_password")

# mongo_uri= pymongo.MongoClient(os.getenv(""))
# database = mongo_uri[os.getenv("DB_NAME")]

# Shipments=database['shipments']
# User_details=database["user_details"]
# Devicedata=database['datastream']

# ACCESS_TOKEN_EXPIRE_MINUTES= 30
# SECRET_KEY=secrets.token_hex(32)
# ALGORITHM = "HS256"

   

import os
import pymongo
from dotenv import load_dotenv
import secrets

# Load environment variables from the .env file
load_dotenv(dotenv_path=".env")

# Project info (can be used later)
TITLE: str = "SCMXpertLite"
DESCRIPTION: str = """SCMXpertLite created in FastAPI"""
PROJECT_VERSION: str = "1.0.0"

# MongoDB credentials and URI
MONGODB_USER = os.getenv("mongodb_user")
MONGODB_PASSWORD = os.getenv("mongodb_password")
MONGO_URI = os.getenv("mongouri")  # Correct URI from the .env file

# Connect to MongoDB using the URI from .env
mongo_client = pymongo.MongoClient(MONGO_URI)

# Access the database
database = mongo_client[os.getenv("DB_NAME")]  # Database name from the .env file

# Define the collections you want to use
Shipments = database['shipments']
User_details = database['user_details']
Devicedata = database['datastream']

# JWT settings
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
