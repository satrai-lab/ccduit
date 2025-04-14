import random
import requests
import time
from datetime import datetime
import pytz
import json
import threading
# URL for the NGSI-LD API endpoint
context_broker_url = 'http://localhost:1032/ngsi-ld/v1/entities/'  # Replace with actual endpoint if different

def log_time(delay_ms):
    """Logs delay time to a file asynchronously."""
    try:
        with open("startup_log_ngsild_ngsild.txt", 'a') as file:
            file.write(f"{delay_ms}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def delete_entity_by_id_after_posting(context_broker_url,entity_id):
    """
    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    entity_url = f"{context_broker_url}/{entity_id}"

    try:
        response = requests.delete(entity_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404 Not Found)

        if response.status_code == 204:  # 204 No Content indicates successful deletion
            return True
        else:
            return False
    
    except requests.exceptions.RequestException as e:
        return False



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
        "id": f"urn:ngsild:Community2:Observation:{time.perf_counter_ns()}",
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
    
    return response.status_code, response.text,observation

# Main simulation loop
# for _ in range(105):

entity_type = "OccupancyReading"
# Fetch all entities of the given type
query_params = {"type": entity_type}
response = requests.get(context_broker_url, params=query_params)
if response.status_code == 200:
    entities = response.json()
    # Loop through each entity and delete it
    for entity in entities:
        entity_id = entity["id"]
        delete_url = f"{context_broker_url}/{entity_id}"
        delete_response = requests.delete(delete_url)
        if delete_response.status_code == 204:
            print(f"✅ Deleted entity: {entity_id}")
        else:
            print(f"❌ Failed to delete entity: {entity_id}. Error: {delete_response.text}")
else:
    print(f"❌ Failed to fetch entities of type {entity_type}. Error: {response.text}")

for _ in range(100):
    observation_data = generate_random_data()
    status_code, response_text, observation_data = send_ngsi_ld_observation(observation_data)
    print(response_text)
    time.sleep(1)


