import os
import sys
import subprocess
import time
import shutil
import psutil
import multiprocessing
import threading
import plot
import json
from datetime import datetime, timezone
import json
import paho.mqtt.client as mqtt
import requests
from multiprocessing import Process
import time
# --- Import Interaction_Handling_Service from Federation1 ---
# Construct Federation1’s path.
modules_path_1 = os.path.join(os.getcwd(), './Federation1')
if os.path.exists(modules_path_1):
    # Insert at the beginning of sys.path so that it takes priority.
    sys.path.insert(0, modules_path_1)
else:
    raise FileNotFoundError(f"Federation1 path not found: {modules_path_1}")

# Now import the desired functions from Interaction_Handling_Service.
from Interaction_Handling_Service import create_Interaction, terminate_Interaction, remove_Interaction
import policy_monitoring as policy_monitoring1
import Policy_Management_Service as PMS1

# Remove Federation1 from sys.path so that it does not interfere with later imports.
if modules_path_1 in sys.path:
    sys.path.remove(modules_path_1)


# --- Import Policy_Management_Service from Federation2 ---
# Construct Federation2’s path.
modules_path_2 = os.path.join(os.getcwd(), './Federation2')
if os.path.exists(modules_path_2):
    # Again, insert at the beginning of sys.path.
    sys.path.insert(0, modules_path_2)
else:
    raise FileNotFoundError(f"Federation2 path not found: {modules_path_2}")

# Now import Policy_Management_Service.
import Policy_Management_Service
import policy_monitoring as policy_monitoring2


# Ensure necessary directories exist
results_dir = "Results"
os.makedirs(results_dir, exist_ok=True)

# Windows flag to suppress new window creation
CREATE_NO_WINDOW = 0x08000000

FED_BROKER = "localhost"
FED_PORT = 1885
CONTEXT_BROKER_URL = "http://localhost:1029/ngsi-ld/v1/entities"
FEDERATION_ID = "urn:ngsi-ld:Federation:Federation2"

def store_policy(policy):
    # print(json.dumps(policy))
    if policy is None:
        print("Policy is None, skipping storage.")
        return
    if isinstance(policy,str):
        policy=json.loads(policy)
        # print(policy)
    headers = {'Content-Type': 'application/json'}
    policy_id = policy.get('id', None)
    if policy_id is None:
        print("Policy ID is None, cannot store policy.")
        return

    print(f"Processing policy with ID: {policy_id}")

    # Extract the lastModified timestamp from the incoming policy
    incoming_last_modified_str = policy.get('modificationPolicy', {}).get('value', {}).get('lastModified', None)
    if incoming_last_modified_str is None:
        print("Incoming policy does not have a lastModified timestamp.")
        return

    # Convert incoming lastModified to UTC datetime
    try:
        incoming_last_modified = datetime.strptime(incoming_last_modified_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        print(f"Invalid lastModified format in incoming policy: {incoming_last_modified_str}")
        return

    try:
        # Attempt to retrieve the existing policy from the Context Broker
        response = requests.get(f"{CONTEXT_BROKER_URL}/{policy_id}")
        if response.status_code == 200:
            existing_policy = response.json()
            existing_last_modified_str = existing_policy.get('modificationPolicy', {}).get('value', {}).get('lastModified', None)

            if existing_last_modified_str:
                # Convert existing lastModified to UTC datetime
                try:
                    existing_last_modified = datetime.strptime(existing_last_modified_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                except ValueError:
                    print(f"Invalid lastModified format in existing policy: {existing_last_modified_str}")
                    return

                # Compare the timestamps
                if incoming_last_modified > existing_last_modified:
                    print(f"Incoming policy is newer. Updating policy {policy_id}.")
                    # Delete the existing policy
                    delete_response = requests.delete(f"{CONTEXT_BROKER_URL}/{policy_id}")
                    delete_response.raise_for_status()
                    print(f"Policy {policy_id} deleted successfully.")
                else:
                    print(f"Existing policy {policy_id} is up-to-date. No changes made.")
                    return

        # Store the incoming policy
        response = requests.post(CONTEXT_BROKER_URL, json=policy, headers=headers)
        response.raise_for_status()
        print(f"Policy {policy_id} stored successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to process policy {policy_id}: {e}")

def publish_policy(policy_entity,topic, mosquitto_address,port=1883):
    """
    Publishes a policy entity to the specified Mosquitto MQTT broker topic.

    Args:
        policy_entity (dict): The policy entity as a Python dictionary.
        mosquitto_address (str): The address of the Mosquitto broker (e.g., "localhost" or "192.168.1.100").
        topic (str, optional): The MQTT topic to publish to. Defaults to "fred/policy".
    """
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Create MQTT Client
    client = mqtt.Client()
    client.on_connect = on_connect

    # Connect to Mosquitto Broker
    try:
        client.connect(mosquitto_address,port)
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return

    # Start MQTT client loop in the background
    client.loop_start()
    policy_entity["timestamp"] = time.perf_counter_ns()
    # Convert entity to JSON string
    payload = json.dumps(policy_entity)
    # start_time=time.perf_counter_ns()
    # Publish message with QoS 2 for persistence
    result = client.publish(topic, payload, qos=2,retain=True)

    # Check if message was sent successfully
    if result[0] == 0:
        print(f"Policy sent to topic {topic}")
    else:
        print(f"Failed to send policy to topic {topic}")

    # Disconnect after publishing
    client.loop_stop()
    client.disconnect()

def add_extra_slashes(url):
    return url.replace("/", "//")

def create_publish_policy(policy_ID,name,description,providerFederation_ID,permittedContextTypes,
                            sharingRules,modifiedBy,Geographic_Restrictions,mosquitto_address=FED_BROKER,mosquitto_Port=FED_PORT):
    # start_time=time.time_ns()
    
    modified_url = add_extra_slashes(CONTEXT_BROKER_URL)
    # Process(target=register_start_times, args=(start_time,)).start()
    policy_Entity = {
            "id": f"urn:ngsi-ld:ContextPolicy:{policy_ID}",
            "type": "ContextPolicy",
            "name": {
              "type": "Property",
              "value": f"{name}"
            },
            "description": {
              "type": "Property",
              "value": f"{description}"
            },
            "providerFederation": {
              "type": "Relationship",
              "object": f"urn:ngsi-ld:Federation:{providerFederation_ID}"
            },
            "permittedContextTypes": {
              "type": "Property",
              "value": permittedContextTypes
            },
            "ContextBrokerURL": {
              "type": "Property",
              "value": f"{modified_url}"
            },
            "sharingRules": {
              "type": "Property",
              "value": sharingRules
            },
            "modificationPolicy": {
              "type": "Property",
              "value": {
                "lastModified": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "modifiedBy": modifiedBy
              }
            },
            "Geographic_Restrictions": {
              "type": "Property",
                "value": Geographic_Restrictions
            }
    }
    Process(target=store_policy,args=(policy_Entity,)).start()
    # store_policy(policy_Entity)
    # file_path=f"{policy_ID}.jsonld"
    # # Write policy to file with proper JSON-LD formatting
    # with open(file_path, "w") as f:
    #     json.dump(policy_Entity, f, indent=2)  # Use indent for readability
    publish_policy(policy_Entity,f"Federation/urn:ngsi-ld:Federation:{providerFederation_ID}/Policy/urn:ngsi-ld:ContextPolicy:{policy_ID}",
                  mosquitto_address,mosquitto_Port)
    



def run_occupancy_script():
    """Runs community1_Occupancy.py, prints real-time output, and handles failures."""
    print("Running community2_Occupancy.py...")
    
    occupancy_process = subprocess.Popen(
        ["python", "community2_Occupancy.py"],
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        text=True,
        cwd="../Communities/community2_endpoint",
        creationflags=CREATE_NO_WINDOW
    )
    
    # # Optionally, you can capture and print output here if needed
    # for line in occupancy_process.stdout:
    #     print(f"{line.strip()}")
    
    return occupancy_process

def log_time(delay_ms):
    """Logs delay time to a file asynchronously."""
    try:
        with open("policy_update_time.txt", 'a') as file:
            file.write(f"{delay_ms}\n")
    except Exception as e:
        print(f"Error writing to file: {e}")  

def main():
    multiprocessing.Process(target=policy_monitoring1.main).start()
    # multiprocessing.Process(target=policy_monitoring2.main).start()
    time.sleep(4)
    for i in range(100):  # Run the sequence 20 times
        print(f"\n🟢 Run {i + 1} - Starting...")
        moni_process=multiprocessing.Process(target=policy_monitoring2.main)
        moni_process.start()
        time.sleep(3)
        Policy_Management_Service.create_publish_policy("Policy2", "Policy2", "This policy allows sharing and forwarding data publicly", "Federation2",
                                                        ["community", "federation", "policies"],
                                                        [{'public': {'canReceive': "true", 'canForward': "true"}}],
                                                        "",[])
        # PMS1.delete_policy(" urn:ngsi-ld:ContextPolicy:Policy2")
        # PMS1.store_policy(policy_entity)
       
        time.sleep(3)
        # Create interaction
        print("Creating interaction ...")
        occupancy_process = run_occupancy_script()
        interaction_id, pid = create_Interaction("Federation1", "Community2", "Community1", "community", "active",
            "NGSI-LD", "Brick", "/?type=OccupancyReading", "community2/occupancy"
        )
        print(f"Interaction created with ID: {interaction_id} and PID: {pid}")
        # Run the occupancy script
        # occupancy_process = run_occupancy_script()
        # Monitor and eventually terminate the interaction process
        interaction_process = psutil.Process(pid)
        time.sleep(3)  # Wait for the script to start
        
        Policy_Management_Service.create_publish_policy("Policy2", "Policy2", "This policy allows sharing and forwarding data publicly", "Federation2",
                                                        ["community", "federation", "policies"],
                                                        [{'public': {'canReceive': "False", 'canForward': "False"}}],
                                                        "",[])
        moni_process.terminate()
        moni_process.join()
        interaction_process.wait()  # Wait for the process to finish
        occupancy_process.terminate()
        print(f"🟢 Run {i + 1} - Completed.\n")
    plot.main()

if __name__ == '__main__':
    main()
