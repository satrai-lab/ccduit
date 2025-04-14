import random
import requests
import time
from datetime import datetime
import pytz
import json

# URL for the NGSI-LD API endpoint
context_broker_url = 'http://localhost:1032/ngsi-ld/v1/entities/'  # Replace with actual endpoint if different

# Generate random data
def generate_random_data():
    timestamp = datetime.now(pytz.utc)
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

def send_ngsi_ld_observation(observation_data):
    # Convert data to NGSI-LD entity structure with the @context attribute
    # Convert row to NGSI-LD entity structure with the @context attribute
    url_delete=f"{context_broker_url}?type=OccupancyReading"
    response = requests.delete(url_delete)

    # Check if the request was successful
    if response.status_code == 204:
        print("Entities of type 'OccupancyReading' deleted successfully.")
    else:
        print(f"Failed to delete entities. Status code: {response.status_code}, Response: {response.text}")
    observation = {
        "id": f"urn:ngsild:Community2:Observation:{time.time_ns()}",
        "type": "OccupancyReading",
        "name": "Occupancy Observation",
        "Community": {
            "type": "Relationship",
            "object": ["urn:ngsi-ld:Community:Community2"]
        },
        "DateObserved": {
            "type": "Property",
            "value": observation_data['Timestamp'].isoformat()
        },
        "OccupancyStatus": {
            "type": "Property",
            "value": observation_data['Occupancy Status']
        },
        "OccupancyPercentage": {
            "type": "Property",
            "value": observation_data['Occupancy Percentage']
        },
        "ZonesWithHighOccupancy": {
            "type": "Property",
            "value": observation_data['Zones with High Occupancy']
        }
    }

    # Send data to NGSI-LD endpoint
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(context_broker_url, headers=headers, data=json.dumps(observation))
    return response.status_code, response.text

# Main simulation loop
for _ in range(105):  # Run the loop 100 times
    observation_data = generate_random_data()
    status_code, response_text = send_ngsi_ld_observation(observation_data)
    print(f"Sent data for {observation_data['Timestamp']}: Status {status_code}")
    print(response_text)
    
    # Wait for 1 second before the next iteration
    time.sleep(1)
