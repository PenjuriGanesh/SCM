import json, logging, random, socket, time
 
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
try:
    s = socket.socket()
    logging.info("Socket Created")
    s.bind(('127.0.0.1', 12345))
    s.listen(3)
    logging.info("Waiting for connections")
    c, addr = s.accept()
    logging.info(f"Connected with {addr}")
 
    # Possible routes
    routes = ['New York, USA', 'Pune, India', 'Bengaluru, India', 'London, UK', 'Hyderabad, India', 'Louisville, USA']
 
    while True:
        try:
            data = []
            for _ in range(2):  # Generate 2 random device entries each time
                route_from = random.choice(routes)
                route_to = random.choice(routes)
 
                # Ensure `Route_From` and `Route_To` are different
                while route_from == route_to:
                    route_to = random.choice(routes)
 
                # Generate random data
                device_data = {
                    "Battery_Level": round(random.uniform(2.00, 5.00), 2),
                    "Device_Id": random.randint(1156053070, 1156053090),
                    "First_Sensor_temperature": round(random.uniform(10.0, 40.0), 1),
                    "Route_From": route_from,
                    "Route_To": route_to
                }
                data.append(device_data)
 
            # Send data to client
            userdata = (json.dumps(data) + "\n").encode('utf-8')
            c.send(userdata)
            logging.info(f"Sent data: {userdata.decode('utf-8')}")
            time.sleep(10)
 
        except Exception as e:
            logging.error(f"Error during data generation or sending: {e}")
            break
 
except socket.error as socket_error:
    logging.error(f"Socket error: {socket_error}")
 
except Exception as e:
    logging.error(f"Unexpected error: {e}")
 
finally:
    c.close()
    logging.info("Connection closed")