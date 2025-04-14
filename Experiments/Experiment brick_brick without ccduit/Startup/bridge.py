import paho.mqtt.client as mqtt
import time
import sys
# Broker configurations
BROKER1 = "localhost"  # Replace with the actual hostname or IP of the first broker
PORT1 = 1888
TOPIC1 = "community1/occupancy"

BROKER2 = "localhost"  # Replace with the actual hostname or IP of the second broker
PORT2 = 1889
TOPIC2 = "community4/occupancy"

# Global variable to store the startup time
startup_time = None

# Publisher client for Broker2
publisher = mqtt.Client()
publisher.connect(BROKER2, PORT2, 60)
publisher.loop_start()  # Run the network loop in a separate thread
def log_time(delay_ms):
    """Logs delay time to a file asynchronously."""
    try:
        with open("delays.txt", 'a') as file:
            file.write(f"{delay_ms}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def on_connect(client, userdata, flags, rc):
    global startup_time
    startup_time = time.perf_counter_ns()  # Capture the time when connected to Broker1
    if rc == 0:
        print("Connected successfully to community1")
        client.subscribe(TOPIC1)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    global startup_time
    # Calculate delay since startup (in nanoseconds, converting to milliseconds)
    
    
    # Process the received message
    message = msg.payload.decode('utf-8')
    print(f"Message received on {msg.topic}: {message}")
    
    # Publish the received message to Broker2 on TOPIC2 and check the result
    result = publisher.publish(TOPIC2, payload=msg.payload)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        delay_ms = (time.perf_counter_ns() - startup_time) / 1e6
        log_time(delay_ms)
        print(f"Message published to Broker2 on {TOPIC2}")
        # Stop the process after publishing
        sys.exit(0)
    else:
        print(f"Failed to publish message to Broker2, return code: {result.rc}")

# Subscriber client for Broker1
subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

subscriber.connect(BROKER1, PORT1, 60)

# Blocking call that processes network traffic, dispatches callbacks, and handles reconnecting.
subscriber.loop_forever()
