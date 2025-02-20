import requests
import json
import time 
import threading
import os
import signal
# Define the NGSI-LD API endpoint and headers
ngsi_ld_endpoint = 'http://localhost:1032/ngsi-ld/v1/entities'  
ngsi_ld_endpoint1 = 'http://localhost:1033/ngsi-ld/v1/entities'  

def log_time(delay_ms):
    """Logs delay time to a file asynchronously."""
    try:
        with open("delay.txt", 'a') as file:
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


def get_ngsi_ld_observations_by_type(entity_type):
    url = f"{ngsi_ld_endpoint}?type={entity_type}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    start_time=time.perf_counter_ns()
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if not data:
            print("⚠️ No data found. Skipping this iteration.")
            return None
        
        data = data[0]
        
        post_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response_post = requests.post(ngsi_ld_endpoint1, headers=post_headers, data=json.dumps(data))
        
        if response_post.status_code in [201] and data:
            
            delay = (time.perf_counter_ns() - start_time) / 1_000_000  # Convert to milliseconds
            delete_entity_by_id_after_posting(ngsi_ld_endpoint, data["id"])
            threading.Thread(target=log_time, args=(delay,)).start()
            print(f"✅ Data successfully posted. Status Code: {response_post.status_code}")
        else:
            print(f"❌ Failed to post data. Status Code: {response_post.status_code}")
            print(f"Response: {response_post.text}")
        
        
        return data
    else:
        print(f"❌ Failed to fetch data. Status Code: {response.status_code}")
        return None

def main():
    entity_type = "OccupancyReading"
    while True: 
        observations_data = get_ngsi_ld_observations_by_type(entity_type)
        # if observations_data:
        #     print(json.dumps(observations_data, indent=2))
        #     print("====================================================")
        time.sleep(0.9)

if __name__ == "__main__":
    main() 


