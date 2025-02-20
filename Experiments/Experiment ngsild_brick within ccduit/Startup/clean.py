import requests

# Orion-LD Broker URL
orion_ld_url = "http://localhost:1033/ngsi-ld/v1/entities"

# Type of entity to delete
entity_type = "OccupancyReading"

# Headers
headers = {
    "Accept": "application/ld+json",
    "Content-Type": "application/ld+json"
}

# Fetch all entities of the given type
query_params = {"type": entity_type}
response = requests.get(orion_ld_url, headers=headers, params=query_params)

if response.status_code == 200:
    entities = response.json()
    
    # Loop through each entity and delete it
    for entity in entities:
        entity_id = entity["id"]
        delete_url = f"{orion_ld_url}/{entity_id}"
        delete_response = requests.delete(delete_url, headers=headers)

        if delete_response.status_code == 204:
            print(f"✅ Deleted entity: {entity_id}")
        else:
            print(f"❌ Failed to delete entity: {entity_id}. Error: {delete_response.text}")
else:
    print(f"❌ Failed to fetch entities of type {entity_type}. Error: {response.text}")
