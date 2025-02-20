import random
import time
from datetime import datetime
import pytz
import paho.mqtt.client as mqtt
import os
# MQTT broker details
mqtt_broker = "localhost"  # Replace with your MQTT broker address
mqtt_port = 1888
mqtt_topic = "community1/occupancy"  # MQTT topic to publish the data

# Publish to MQTT
def publish_to_mqtt(client, topic, message):
    client.publish(topic, message)
    print(f"Published to MQTT Topic '{topic}':\n{message}")

# Main simulation loop
def main():
    # Initialize MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.connect(mqtt_broker, mqtt_port, 60)
    mqtt_client.loop_start()

    try:
        # for _ in range(105):  # Run the loop 105 times
            # Generate random data
        observation_data = generate_random_data()
        # Convert to Brick TTL format
        ttl_data = ""
        # Publish to MQTT broker
        publish_to_mqtt(mqtt_client, mqtt_topic, ttl_data)
        # Wait for 1 second before the next iteration
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
