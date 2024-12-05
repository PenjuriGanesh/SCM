from confluent_kafka import Producer
import json, logging, os, socket
from dotenv import load_dotenv
 
load_dotenv()
 
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
Host = os.getenv("HOST")
Port = int(os.getenv("PORT"))
 
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
try:
    # Establish socket connection to server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('127.0.0.1', Port)) 
    server.settimeout(10)
    logging.info(f"Connected to server at {Host}:{Port}")
 
    # Configure Kafka producer
    producer = Producer({"bootstrap.servers": bootstrap_servers})
 
    # Function to send message to Kafka topic
    def send_message(topic, message):
        try:
            producer.produce(topic, value=json.dumps(message))
            producer.flush()
            logging.info(f"Message sent to Kafka topic {topic}: {message}")
        except Exception as kafka_error:
            logging.error(f"Error sending message to Kafka: {kafka_error}")
 
    # Receive messages from socket and send to Kafka
    while True:
        try:
            message = server.recv(1024).decode('utf-8')
            if message:
                logging.info(f"Received message from server: {message}")
                send_message("device_data_stream", message)
            else:
                logging.warning("Received empty message from server")
       
        except socket.timeout:
            logging.warning("No messages received in the last 10 seconds.")
       
        except ConnectionResetError:
            logging.error("Connection reset by peer.")
            break
       
        except Exception as general_error:
            logging.error(f"Unexpected error: {general_error}")
            break
 
except socket.error as socket_error:
    logging.error(f"Socket error: {socket_error}")
 
except Exception as general_error:
    logging.error(f"Unexpected error: {general_error}")
 
finally:
    server.close()
    logging.info("Connection closed")