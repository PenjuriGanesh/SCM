from confluent_kafka import Producer
import json, os, socket
# from dotenv import load_dotenv

 
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
Host = os.getenv("HOST")
Port = int(os.getenv("PORT"))

print("Hi")
print(bootstrap_servers)
print(Host)
print(Port)
 

try:
   
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((Host, Port)) 
    server.settimeout(10)
    print(f"Connected to server at {Host}:{Port}")
 
    
    producer = Producer({"bootstrap.servers": bootstrap_servers})
 
    
    def send_message(topic, message):
        try:
            producer.produce(topic, value=json.dumps(message))
            producer.flush()
            print(f"Message sent to Kafka topic {topic}: {message}")
        except Exception as kafka_error:
            print(f"Error sending message to Kafka: {kafka_error}")
 
    while True:
        try:
            message = server.recv(1024).decode('utf-8')
            if message:
                print(f"Received message from server: {message}")
                send_message("device_data_stream", message)
            else:
                print("Received empty message from server")
       
        except socket.timeout:
            print("No messages received in the last 10 seconds.")
       
        except ConnectionResetError:
            print("Connection reset by peer.")
            break
       
        except Exception as general_error:
            print(f"Unexpected error: {general_error}")
            break
 
except socket.error as socket_error:
    print(f"Socket error: {socket_error}")
 
except Exception as general_error:
     print(f"Unexpected error: {general_error}")
 
finally:
    server.close()
