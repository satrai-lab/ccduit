import requests
import json
import time 

# Define the NGSI-LD API endpoint and headers
ngsi_ld_endpoint = 'http://localhost:1032/ngsi-ld/v1/entities'  # Verify this URL

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
            return data
        # else:
        #     return "No data found. Ensure entities of type 'Observation' with 'DateObserved' attribute exist."
    else:
        return f"Error: {response.status_code}, {response.text}"

# Specify the type of entities to retrieve
entity_type = "OccupancyReading"

# Fetch and print the observations of the specified type
while True: 
    observations_data = get_ngsi_ld_observations_by_type(entity_type)

    print(json.dumps(observations_data, indent=2))
    print("====================================================")
    time.sleep(2.9)
# url_delete=f"{ngsi_ld_endpoint}?type=OccupancyObservation"
# response = requests.delete(url_delete)
# # Check if the request was successful
# if response.status_code == 204:
#     print("Entities of type 'OccupancyObservation' deleted successfully.")
# else:
#     print(f"Failed to delete entities. Status code: {response.status_code}, Response: {response.text}")