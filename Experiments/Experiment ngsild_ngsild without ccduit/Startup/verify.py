import requests
import json
import time
import threading
import os
import signal

# Define the NGSI-LD API endpoints and headers
ngsi_ld_endpoint = 'http://localhost:1032/ngsi-ld/v1/entities'
ngsi_ld_endpoint1 = 'http://localhost:1033/ngsi-ld/v1/entities'

def log_time(delay_ms):
    """Logs delay time to a file asynchronously."""
    try:
        with open("delay.txt", 'a') as file:
            file.write(f"{delay_ms}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

def delete_entity_by_id_after_posting(context_broker_url, entity_id):
    """
    Deletes an entity after posting it to the second endpoint.
    
    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    entity_url = f"{context_broker_url}/{entity_id}"
    try:
        response = requests.delete(entity_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.status_code == 204  # 204 No Content indicates successful deletion
    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting entity {entity_id}: {e}")
        return False

def get_ngsi_ld_observations_by_type(entity_type):
    """
    Fetches observations of a specific entity type. If data is received,
    posts the first entry to a secondary endpoint and then deletes the original entity.
    
    Returns:
        tuple: (data, pid) where data is the observation data or None if not found,
               and pid is the process id.
    """
    start_time= time.perf_counter_ns()
    url = f"{ngsi_ld_endpoint}?type={entity_type}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        pid = os.getpid()
        if response.status_code == 200:
            data_list = response.json()
            if not data_list:
                # print(f"⚠️ No data found for entity type '{entity_type}'. Skipping this cycle.")
                return None, pid
            data = data_list[0]
            
            # Post the data to the second endpoint
            post_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            response_post = requests.post(ngsi_ld_endpoint1, headers=post_headers, data=json.dumps(data))
            if response_post.status_code in [200, 201, 204]:
                delay = (time.perf_counter_ns() - start_time)/1e6
                threading.Thread(target=log_time, args=(delay,)).start()
                print(f"✅ Data successfully posted. Status Code: {response_post.status_code}")
            else:
                print(f"❌ Failed to post data. Status Code: {response_post.status_code}")
                print(f"Response: {response_post.text}")
            
            # Delete the entity after posting
            if delete_entity_by_id_after_posting(ngsi_ld_endpoint, data["id"]):
                print(f"✅ Successfully deleted entity {data['id']}")
            else:
                print(f"❌ Failed to delete entity {data['id']}")
                
            return data, pid
        else:
            print(f"❌ Error fetching entities: {response.text}")
            return None, pid
    except Exception as e:
        print(f"Exception in get_ngsi_ld_observations_by_type: {e}")
        return None, os.getpid()

def main():
    entity_type = "OccupancyReading"
    while True:
        observations_data, pid = get_ngsi_ld_observations_by_type(entity_type)
        # if observations_data is None:
        #     # If no data is returned, skip process killing and printing of data.
        #     # print("No observations data received, moving to the next cycle.\n")
        if observations_data:
            try:
                os.kill(pid, signal.SIGTERM)  # SIGTERM for graceful termination
                print(f"✅ Process {pid} killed.")
            except ProcessLookupError:
                print(f"⚠️ Process {pid} not found.")
            except PermissionError:
                print(f"🚫 Permission denied to kill process {pid}.")
            
            print("Posted data:")
            print(json.dumps(observations_data, indent=2))
        print("====================================================")
        time.sleep(0.5)

if __name__ == "__main__":
    main()

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
