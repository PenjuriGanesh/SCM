from confluent_kafka import Consumer
from dotenv import load_dotenv
import json, logging, os
from pymongo import MongoClient
from pymongo.database import Database
 
# Load environment variables
load_dotenv(dotenv_path=".env")
 
# Retrieve and validate MongoDB connection details
connection_string = os.getenv("MONGODB_URI")
database_name = os.getenv("MONGODB_DATABASE")
 
if not connection_string or not database_name:
    raise ValueError("MongoDB connection string or database name is not set in .env")
 
# Create MongoDB client and access the database
client = MongoClient(connection_string)
database = client[database_name]
device_data_stream1= database["Device_Data_Stream"]
 
# Kafka Configuration
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
if not bootstrap_servers:
    raise ValueError("Kafka bootstrap servers are not set in .env")
 
consumer_config = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}
 
consumer = Consumer(consumer_config)
consumer.subscribe(['device_data_stream'])
 
try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                continue
 
            try:
                raw_message = msg.value().decode('utf-8')
                logging.info(f"Raw message received: {raw_message}")
                data = json.loads(raw_message)
 
                if isinstance(data, str):
                    data = json.loads(data)
 
                logging.info(f"Deserialized data: {data}")
 
                if isinstance(data, list):
                    device_data_stream1.insert_many(data)
                    logging.info(f"Inserted data: {data}")
                elif isinstance(data, dict):
                    device_data_stream1.insert_one(data)
                    logging.info(f"Inserted data: {data}")
                else:
                    logging.warning(f"Invalid data format: {data}")
            except Exception as e:
                logging.error(f"Error processing message: {str(e)}")
 
except KeyboardInterrupt:
        logging.info("Consumer interrupted by user.")
   
finally:
        consumer.close()
        logging.info("Consumer closed")      
   