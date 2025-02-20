import subprocess
import os
import time
import requests
import json

# List of federation folders
federations = ["Federation1", "Federation2", "Federation3"]

def run_command(command, working_dir):
    """Runs a shell command in a specified directory."""
    try:
        print(f"Running '{command}' in {working_dir}...")
        subprocess.Popen(command, shell=True, cwd=working_dir)
        time.sleep(2)  # Give a brief pause to ensure commands start properly
    except Exception as e:
        print(f"Error running command in {working_dir}: {e}")

def start_api_services():
    """Starts python3 app.py in each federation folder."""
    for federation in federations:
        run_command("python3 app.py", os.path.abspath(federation))

def start_broker_services():
    """Runs docker-compose up in each federation's /brokers subfolder."""
    for federation in federations:
        brokers_path = os.path.join(os.path.abspath(federation), "brokers")
        run_command("docker-compose up", brokers_path)

if __name__ == "__main__":
    # Start the api.py processes
    start_api_services()

    # Start the docker-compose up processes
    start_broker_services()

    (time.sleep(10))
     # List of ports
    ports = [5001, 5002, 5003]

    # Base URL and endpoint
    base_url = 'http://127.0.0.1:{}/run-monitoring'
    headers = {
        'accept': 'application/json'
    }
    
    # Loop through each port and send the POST request
    for port in ports:
        url = base_url.format(port)
        try:
            response = requests.post(url, headers=headers)
            print(f"Response for port {port}:")
            print("Status Code:", response.status_code)
            print("Response Body:", response.text)
            print("-" * 50)
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to port {port}: {e}")
            print("-" * 50)


    # URL for the POST request
    url = 'http://127.0.0.1:5001/create_publish_policy'

    # Headers for the request
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Data payload for the request
    data = {
        "policy_ID": "Policy1",
        "name": "Policy1",
        "description": "this policy allow sharing and forwarding data publicly",
        "permittedContextTypes": [
            "community",
            "federation",
            "policies",
            "functions",
            "datamodels"
        ],
        "sharingRules": [
            {
                "federation": "Federation2",
                "canReceive": True,
                "canForward": True
            },
            {
                "federation": "public",
                "canReceive": True,
                "canForward": True
            }
        ],
        "modifiedBy": "",
        "Geographic_Restrictions": []
    }
    # Base URL for the requests
    urls = [
        "http://127.0.0.1:5002/create_publish_policy",
        "http://127.0.0.1:5003/create_publish_policy"
    ]

    # Headers for the requests
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Policy data for Policy2 (Federation2)
    policy2_data = {
        "policy_ID": "Policy2",
        "name": "Policy2",
        "description": "this policy allow sharing and forwarding data publicly",
        "permittedContextTypes": [
            "community",
            "federation",
            "policies",
            "functions",
            "datamodels"
        ],
        "sharingRules": [
            {
                "federation": "public",
                "canReceive": True,
                "canForward": True
            }
        ],
        "modifiedBy": "",
        "Geographic_Restrictions": []
    }

    # Policy data for Policy3 (Federation3)
    policy3_data = {
        "policy_ID": "Policy3",
        "name": "Policy3",
        "description": "this policy allow sharing and forwarding data publicly",
        "permittedContextTypes": [
            "community",
            "federation",
            "policies",
            "functions",
            "datamodels"
        ],
        "sharingRules": [
            {
                "federation": "public",
                "canReceive": True,
                "canForward": True
            }
        ],
        "modifiedBy": "",
        "Geographic_Restrictions": []
    }

    # List of policies and corresponding URLs
    policies = [
        (urls[0], policy2_data),
        (urls[1], policy3_data)
    ]

    # Send the POST requests
    for url, data in policies:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print(f"Sent request to {url}")
            print("Status Code:", response.status_code)
            print("Response Body:", response.text)
            print("-" * 50)
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to {url}: {e}")
        # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print the response
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    # First request
    url1 = 'http://127.0.0.1:5001/initiate_collaboration/'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data1 = {
        "destination_broker": "localhost",
        "destination_port": 1885,
        "receiver_Fed_ID": "Federation2",
        "details": "Federation1 sends Collaboration Request to Federation2",
        "policy_ID": "Policy1"
    }

    response1 = requests.post(url1, headers=headers, data=json.dumps(data1))

    print("Response 1 Status Code:", response1.status_code)
    print("Response 1 Body:", response1.text)

    # Second request
    url2 = 'http://127.0.0.1:5002/initiate_collaboration/'
    data2 = {
        "destination_broker": "localhost",
        "destination_port": 1886,
        "receiver_Fed_ID": "Federation3",
        "details": "Federation2 sends Collaboration Request to Federation3",
        "policy_ID": "Policy2"
    }

    response2 = requests.post(url2, headers=headers, data=json.dumps(data2))

    print("Response 2 Status Code:", response2.status_code)
    print("Response 2 Body:", response2.text)
    print("All processes have been started.")
