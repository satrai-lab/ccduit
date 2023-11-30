import paho.mqtt.client as mqtt
import json

# MQTT broker details
BROKER_URL = "localhost"
BROKER_PORT = 1027
TOPIC = "ngsi-ld/data"

# Callback when a message is received
def on_message(client, userdata, message):
    payload = message.payload.decode()  # Convert bytes to string
    try:
        # Attempt to load the payload as JSON
        json_payload = json.loads(payload)
        pretty_payload = json.dumps(json_payload, indent=4)
        print(f"Received message:\n{pretty_payload}\non topic '{message.topic}'")
    except json.JSONDecodeError:
        # If it's not JSON, print it as is
        print(f"Received message '{payload}' on topic '{message.topic}'")

# Callback when connected to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

# Setting up the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connecting to the broker
mqtt_client.connect(BROKER_URL, BROKER_PORT, 60)

# Start the MQTT client loop
mqtt_client.loop_forever()
