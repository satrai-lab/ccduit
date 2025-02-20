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

# Generate random data
def generate_random_data():
    timestamp = datetime.now(pytz.utc).isoformat()
    occupancy_percentage = random.randint(0, 100)
    
    # Determine occupancy status based on percentage
    if 0 <= occupancy_percentage <= 50:
        occupancy_status = "low"
    elif 51 <= occupancy_percentage <= 70:
        occupancy_status = "medium"
    else:
        occupancy_status = "high"
    
    zones_with_high_occupancy = "ZoneA, ZoneB" if occupancy_status == "high" else ""
    
    return {
        "Timestamp": timestamp,
        "Occupancy Status": occupancy_status,
        "Occupancy Percentage": occupancy_percentage,
        "Zones with High Occupancy": zones_with_high_occupancy
    }

# Convert data to Brick TTL format
def convert_to_brick_ttl(data):
    ttl_template = f"""
    @prefix brick: <https://brickschema.org/schema/1.1/Brick#> .
    @prefix ex: <http://example.com#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:Community1:Observation:{int(time.perf_counter_ns())} a brick:OccupancyReading ;
        brick:dateObserved "{data['Timestamp']}"^^xsd:dateTime ;
        brick:occupancyStatus "{data['Occupancy Status']}" ;
        brick:occupancyPercentage "{data['Occupancy Percentage']}"^^xsd:float ;
        brick:zonesWithHighOccupancy "{data['Zones with High Occupancy']}" .
    """
    return ttl_template

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
        for _ in range(105):  # Run the loop 105 times
            observation_data = generate_random_data()
            # Convert to Brick TTL format
            ttl_data = convert_to_brick_ttl(observation_data)
            # Publish to MQTT broker
            publish_to_mqtt(mqtt_client, mqtt_topic, ttl_data)
            # Wait for 1 second before the next iteration
            time.sleep(1)
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    # os.system("mosquitto_sub -h localhost -p 1888 -t 'community1/occupancy' -r -n")
    main()
