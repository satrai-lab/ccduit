import requests
import json
import time 

# Define the NGSI-LD API endpoint and headers
ngsi_ld_endpoint = 'http://localhost:1033/ngsi-ld/v1/entities'  # Verify this URL


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


def get_ngsi_ld_observations_by_type(entity_type):
    # Ensure proper URL formatting without duplicate slashes
    url = f"{ngsi_ld_endpoint}?type={entity_type}"
    headers = {
        "Accept": "application/json"
    }
    # Make the GET request
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:  # Check if there’s data in the response
            delete_entity_by_id_after_posting(ngsi_ld_endpoint,data[0]["id"])
            return data
        # else:
        #     return "No data found. Ensure entities of type 'Observation' with 'DateObserved' attribute exist."
    else:
        return f"Error: {response.status_code}, {response.text}"

# Specify the type of entities to retrieve
entity_type = "OccupancyReading"
# Fetch all entities of the given type
query_params = {"type": entity_type}
response = requests.get(ngsi_ld_endpoint, params=query_params)

if response.status_code == 200:
    entities = response.json()
    
    # Loop through each entity and delete it
    for entity in entities:
        entity_id = entity["id"]
        delete_url = f"{ngsi_ld_endpoint}/{entity_id}"
        delete_response = requests.delete(delete_url)

        if delete_response.status_code == 204:
            print(f"✅ Deleted entity: {entity_id}")
        else:
            print(f"❌ Failed to delete entity: {entity_id}. Error: {delete_response.text}")
else:
    print(f"❌ Failed to fetch entities of type {entity_type}. Error: {response.text}")

# Fetch and print the observations of the specified type
while True: 
    observations_data = get_ngsi_ld_observations_by_type(entity_type)

    print(json.dumps(observations_data, indent=2))
    print("====================================================")
    time.sleep(0.9)


# import requests

# # Orion-LD Broker URL
# orion_ld_url = "http://localhost:1033/ngsi-ld/v1/entities"

# # Type of entity to delete
# entity_type = "OccupancyReading"

# # Headers
# headers = {
#     "Accept": "application/ld+json",
#     "Content-Type": "application/ld+json"
# }

# # Fetch all entities of the given type
# query_params = {"type": entity_type}
# response = requests.get(orion_ld_url, headers=headers, params=query_params)

# if response.status_code == 200:
#     entities = response.json()
    
#     # Loop through each entity and delete it
#     for entity in entities:
#         entity_id = entity["id"]
#         delete_url = f"{orion_ld_url}/{entity_id}"
#         delete_response = requests.delete(delete_url, headers=headers)

#         if delete_response.status_code == 204:
#             print(f"✅ Deleted entity: {entity_id}")
#         else:
#             print(f"❌ Failed to delete entity: {entity_id}. Error: {delete_response.text}")
# else:
#     print(f"❌ Failed to fetch entities of type {entity_type}. Error: {response.text}")
