import paho.mqtt.client as mqtt
import time
import threading
import sys

# Configuration for the first MQTT broker (subscriber)
sub_broker = "localhost"
sub_port = 1888
sub_topic = "community1/occupancy"

# Configuration for the second MQTT broker (publisher)
pub_broker = "localhost"
pub_port = 1889
pub_topic = "community4/occupancy"

def log_time(delay_ms):
    """Logs delay time to a file asynchronously."""
    try:
        with open("delay.txt", 'a') as file:
            file.write(f"{delay_ms}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Callback when the subscriber client connects to the broker
def sub_on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber connected to broker successfully.")
        # Get the current time and store it in userdata
        userdata['start_time'] = time.perf_counter_ns()
        # Subscribe to the topic after connecting
        client.subscribe(sub_topic)
    else:
        print(f"Failed to connect to broker. Return code: {rc}")

# Callback when a message is received from the subscribed topic
def on_message(client, userdata, message):
    # print(f"Received message: {message.payload.decode()} on topic {message.topic}")
    
    # Publish the received message to the second broker with verification
    try:
        result, mid = pub_client.publish(pub_topic, message.payload)
        if result == mqtt.MQTT_ERR_SUCCESS:
            # Calculate delay using start_time from userdata
            delay = (time.perf_counter_ns() - userdata['start_time']) / 1_000_000
            threading.Thread(target=log_time, args=(delay,)).start()
            print(f"Message successfully published to {pub_topic} with message ID {mid}")
            
            # Terminate the process after processing the message
            print("Terminating the process...")
            sub_client.disconnect()  # Disconnect the subscriber client
            pub_client.disconnect()  # Disconnect the publisher client
            sys.exit(0)  # Exit the program
        else:
            print(f"Failed to publish message. Error code: {result}")
    except Exception as e:
        print(f"An error occurred while publishing: {e}")

# Setup subscriber client
sub_client = mqtt.Client(userdata={})  # Pass an empty dictionary as userdata
sub_client.on_connect = sub_on_connect  # Assign the on_connect callback
sub_client.on_message = on_message
sub_client.connect(sub_broker, sub_port, 60)

# Setup publisher client
pub_client = mqtt.Client()
pub_client.connect(pub_broker, pub_port, 60)

# Start the loop to process network traffic and dispatch callbacks
sub_client.loop_forever()