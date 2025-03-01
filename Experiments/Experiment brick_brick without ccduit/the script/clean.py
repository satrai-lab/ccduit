import paho.mqtt.client as mqtt

# Configuration for the MQTT broker
broker = "localhost"  # Replace with your MQTT broker address
port = 1883           # Default MQTT port
topic = "community1/occupancy"

# Create an MQTT client instance
client = mqtt.Client()

try:
    # Connect to the broker
    print(f"Connecting to broker at {broker}:{port}...")
    client.connect(broker, port, 60)
    print("Connected to broker.")

    # Publish an empty message to the topic
    print(f"Publishing to topic: {topic}")
    client.publish(topic, "")

    # Disconnect from the broker
    client.disconnect()
    print("Disconnected from broker.")
except ConnectionRefusedError:
    print("Error: Connection refused. Ensure the broker is running and accessible.")
except Exception as e:
    print(f"An error occurred: {e}")