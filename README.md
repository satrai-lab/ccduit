# CCDUIT Software Overlay Prototype

This README provides detailed instructions for setting up and utilizing the CCDUIT Software Overlay prototype. It enables dynamic collaboration between data space federations, facilitating context exchange and interaction management. The guide outlines the configuration of federations, communities, data models, functions, and policies, along with steps to deploy essential services and reproduce experiments from the paper.
---

# Table of Contents

1. [Prerequisites](#prerequisites)
   - [Operating System](#operating-system)
   - [Required Installations](#required-installations)

2. [Installation and Configuration](#installation-and-configuration)
   - [Step 1: Download the Source Code](#step-1-download-the-source-code)
   - [Step 2: Run the Application](#step-2-run-the-application)
   - [Step 3: Start the Containers](#step-3-start-the-containers)
   - [Step 4: Run the Monitoring Services](#step-4-run-the-monitoring-services)
   - [Step 5: Context Registration for Each Federation](#step-5-context-registration-for-each-federation)
   - [Step 6: Policy Registration for Each Federation](#step-6-policy-registration-for-each-federation)
   - [Step 7: Collaboration Initiation Between Federations](#step-7-collaboration-initiation-between-federations)
   - [Step 8: Manual Context Exchange (Fallback)](#step-8-manual-context-exchange-fallback)

3. [Data Interaction Between Communities Experiments](#data-interaction-between-communities-experiments)
   - [Step 1: Set Up Community1 Endpoint](#step-1-set-up-community1-endpoint)
   - [Step 2: Set Up Community2 Endpoint](#step-2-set-up-community2-endpoint)
   - [Step 3: Set Up Community3 Endpoint](#step-3-set-up-community3-endpoint)
   - [Step 4: Set Up Community4 Endpoint](#step-4-set-up-community4-endpoint)

4. [Experiment A: Interaction Latency](#experiment-a-interaction-latency)
   - [Experiment 1: Community 1 and Community 2 within CCDUIT](#experiment-1-community-1-and-community-2-within-ccduit)
   - [Experiment 2: Community 2 and Community 1 within CCDUIT](#experiment-2-community-2-and-community-1-within-ccduit)
   - [Experiment 3: Community 2 and Community 3 within CCDUIT](#experiment-3-community-2-and-community-3-within-ccduit)
   - [Experiment 4: Community 4 and Community 1 within CCDUIT](#experiment-4-community-4-and-community-1-within-ccduit)
   - [Experiment 5: Community 2 and Community 3 without CCDUIT](#experiment-5-community-2-and-community-3-without-ccduit)
   - [Experiment 6: Community 4 and Community 1 without CCDUIT](#experiment-6-community-4-and-community-1-without-ccduit)

5. [Experiment B: Adaptation Experiment](#experiment-b-adaptation-experiment)
   - [Experiment 1: First Adaptation Experiment](#experiment-1-first-adaptation-experiment)
   - [Experiment 2: Second Adaptation Experiment](#experiment-2-second-adaptation-experiment)

6. [Running the Second Adaptation Experiment](#running-the-second-adaptation-experiment)
   - [Experiment Steps](#experiment-steps)
   - [Expected Results](#expected-results)
---

## Prerequisites

- **Operating System:**  
  - Tested on **Windows 11** and **Ubuntu 22.04.4 LTS**.  
  - The instructions should work on any system supporting Python and Docker.

Ensure the following are installed on your system:

- **Python 3:**  
  Verify the installation by running:

  ```bash
  python3 --version
  ```

- **Docker Engine:**  
  Install Docker Desktop for Windows or Docker Engine for Linux.  
  Ensure Docker is running:

  ```bash
  docker --version
  ```

**Note:** The instructions contain details to create a **federation of federations** using **four example federations** like in the figure below. All context and details have been simplified for easier understanding and experimentation. All commands (e.g., registrations, interactions) should be executed via the API (`app.py`) of the relevant federation.
![Diagram](images/diagram.png)
---

## Installation and Configuration

### Step 1: Download the Source Code

1. Download the provided source code archive.
2. Extract the archive into **separate directories**, each corresponding to one **'redacted' node** for each federation described below.  
   **Important:** Extract each node from the original archive to avoid conflicts caused by duplication.
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

---

### Step 2: Run the Application

1. **Open a terminal** in the directory of the **'redacted' node** you wish to configure.

2. **Modify the `app.py` Port:**  
   Each federation node should run on a **unique port** to avoid conflicts.

   - Open the `app.py` file in a text editor.
   - Locate the line defining the port (e.g., `Api_port = 5000`).
   - Change the port number for each federation. For example:

     ```python
     Api_port = 5001  # Federation 1
     Api_port = 5002  # Federation 2
     Api_port = 5003  # Federation 3
     Api_port = 5004  # Federation 4
     ```

3. **Run the application for each federation:**

   ```bash
   python3 app.py
   ```

4. **Access the API documentation** in your browser by visiting:
    http://127.0.0.1:<Api_port>/docs


5. **Configure the software** via the API’s **Configuration** section to assign unique ports and names to each Docker container.

---

### Example Configuration for Each Federation

#### Federation 1

```json
{
"federation_name": "Federation1",
"orionLd_port": 1028,
"mongo_db_port": 27018,
"mosquitto_port": 1884
}
```

#### Federation 2

```json
{
"federation_name": "Federation2",
"orionLd_port": 1029,
"mongo_db_port": 27019,
"mosquitto_port": 1885
}
```

#### Federation 3

```json
{
"federation_name": "Federation3",
"orionLd_port": 1030,
"mongo_db_port": 27020,
"mosquitto_port": 1886
}
```

#### Federation 4

```json
{
"federation_name": "Federation4",
"orionLd_port": 1031,
"mongo_db_port": 27021,
"mosquitto_port": 1887
}
```


---

### Step 3: Start the Containers

1. **Navigate to the `brokers` folder** of each federation:

   ```bash
   cd brokers
   ```

2. **Start the Docker containers**:

   ```bash
   docker-compose up
   ```

3. To run the containers in **detached mode** (background), use:

   ```bash
   docker-compose up -d
   ```

---

### Step 4: Run the Monitoring Services

1. Access the **Run Monitoring Services** section in the API documentation for each federation node.

2. **Execute the Run Monitoring** function to start monitoring services.

3. **Verify** that all monitoring processes are active and running as expected, you will see on the terminal two messages :
- Hello, Policy Synchronizer!
- Hello, collaboration monitoring!

---

### Step 5: Context Registration for Each Federation

Each federation node requires context registration to manage federations, communities, data models, and functions.

**Note:** The following instructions will create context for **four federations** with simplified configurations to facilitate understanding and experimentation. 
Make sure to follow the exact order [Federation, Data Model, Community, Function etc.] because there are bidirectional relationships created automatically by the system that assume that this order has been followed.

#### Federation 1

**Register Federation:**

```json
{
  "federation_Id": "Federation1",
  "name": "Federation1",
  "topology": "star",
  "structure": "hierarchy",
  "areaCovered": "5000m2",
  "number_Of_Nodes": 1,
  "includes_Communities": [],
  "uses_Interactions": []
}
```

**Register Data Model:**

```json
{
  "dataModel_Id": "datamodel1",
  "name": "Brick Ontology",
  "description": "A metadata schema designed for buildings.",
  "format": "TTL",
  "specific_Ontology": "Brick",
  "ontology_Version": "1.3",
  "ontology_URL": "https://brickschema.org/ontology/1.3/Brick.ttl"
}
```

**Register Community:**

```json
{
  "community_Id": "Community1",
  "name": "Community1",
  "connection_Details": {
    "endpoint": "localhost:1888",
    "protocol": "MQTT"
  },
  "origin": "France",
  "role_In_Federation": "Occupancy Data Provider",
  "has_Data_Models": ["datamodel1"],
  "part_Of_Federation": "Federation1",
  "geographical_Location": ""
}
```

**Register Function:**

```json
{
  "function_Id": "convert_ngsi_ld_to_brick1",
  "call_Function": "convert_ngsi_ld_to_brick",
  "description": "Converts NGSI-LD data model to Brick.",
  "From_model": "NGSI-LD",
  "To_model": "Brick",
  "Version": "1.0",
  "usage_Guide": "Accepts JSON input, outputs TTL format.",
  "packages": ["rdflib", "datetime", "json"]
}
```

---

#### Federation 2

**Register Federation:**

```json
{
  "federation_Id": "Federation2",
  "name": "Federation2",
  "topology": "ring",
  "structure": "hierarchical",
  "areaCovered": "6000m2",
  "number_Of_Nodes": 1,
  "includes_Communities": [],
  "uses_Interactions": []
}
```

**Register Data Model:**

```json
{
  "dataModel_Id": "datamodel2",
  "name": "NGSI-LD",
  "description": "A metadata schema for weather observations, facilitating semantic interoperability.",
  "format": "JSON",
  "specific_Ontology": "https://schema.org/Weather",
  "ontology_Version": "1.0",
  "ontology_URL": "https://schema.org/docs/weather.html"
}
```

**Register Community:**

```json
{
  "community_Id": "Community2",
  "name": "Community2",
  "connection_Details": {
    "endpoint": "http://localhost:1032/ngsi-ld/v1/entities",
    "protocol": "HTTP"
  },
  "origin": "France",
  "role_In_Federation": "Weather Data Provider",
  "has_Data_Models": ["datamodel2"],
  "part_Of_Federation": "Federation2",
  "geographical_Location": ""
}
```

**Register Function:**

```json
{
  "function_Id": "convert_brick_to_ngsi_ld2",
  "call_Function": "convert_brick_to_ngsi_ld",
  "description": "This function converts Brick data into NGSI-LD format.",
  "From_model": "Brick",
  "To_model": "NGSI-LD",
  "Version": "1.0",
  "usage_Guide": "Accepts TTL input, outputs JSON format.",
  "packages": ["rdflib", "datetime", "json"]
}
```

---

#### Federation 3

**Register Federation:**

```json
{
  "federation_Id": "Federation3",
  "name": "Federation3",
  "topology": "ring",
  "structure": "hierarchical",
  "areaCovered": "6000m2",
  "number_Of_Nodes": 1,
  "includes_Communities": [],
  "uses_Interactions": []
}
```

**Register Data Model:**

```json
{
  "dataModel_Id": "datamodel3",
  "name": "NGSI-LD",
  "description": "A metadata schema for weather observations, facilitating semantic interoperability.",
  "format": "JSON",
  "specific_Ontology": "https://schema.org/Weather",
  "ontology_Version": "1.0",
  "ontology_URL": "https://schema.org/docs/weather.html"
}
```

**Register Community:**

```json
{
  "community_Id": "Community3",
  "name": "Community3",
  "connection_Details": {
    "endpoint": "http://localhost:1033/ngsi-ld/v1/entities",
    "protocol": "HTTP"
  },
  "origin": "France",
  "role_In_Federation": "Weather Data Provider",
  "has_Data_Models": ["datamodel3"],
  "part_Of_Federation": "Federation3",
  "geographical_Location": ""
}
```

**Register Function:**

```json
{
  "function_Id": "convert_brick_to_ngsi_ld3",
  "call_Function": "convert_brick_to_ngsi_ld",
  "description": "This function converts Brick data into NGSI-LD format.",
  "From_model": "Brick",
  "To_model": "NGSI-LD",
  "Version": "1.0",
  "usage_Guide": "Accepts TTL input, outputs JSON format.",
  "packages": ["rdflib", "datetime", "json"]
}
```

---

#### Federation 4

**Register Federation:**

```json
{
  "federation_Id": "Federation4",
  "name": "Federation4",
  "topology": "star",
  "structure": "hierarchy",
  "areaCovered": "7000m2",
  "number_Of_Nodes": 1,
  "includes_Communities": [],
  "uses_Interactions": []
}
```

**Register Data Model:**

```json
{
  "dataModel_Id": "datamodel4",
  "name": "Brick Ontology",
  "description": "A metadata schema designed for buildings, facilitating semantic interoperability for building management systems.",
  "format": "TTL",
  "specific_Ontology": "Brick",
  "ontology_Version": "1.3",
  "ontology_URL": "https://brickschema.org/ontology/1.3/Brick.ttl"
}
```

**Register Community:**

```json
{
  "community_Id": "Community4",
  "name": "Community4",
  "connection_Details": {
    "endpoint": "localhost:1889",
    "protocol": "MQTT"
  },
  "origin": "France",
  "role_In_Federation": "Occupancy Data Provider",
  "has_Data_Models": ["datamodel4"],
  "part_Of_Federation": "Federation4",
  "geographical_Location": ""
}
```

**Register Function:**

```json
{
  "function_Id": "convert_ngsi_ld_to_brick4",
  "call_Function": "convert_ngsi_ld_to_brick",
  "description": "This function converts NGSI-LD data model to Brick.",
  "From_model": "NGSI-LD",
  "To_model": "Brick",
  "Version": "1.0",
  "usage_Guide": "Accepts JSON input, outputs TTL format.",
  "packages": ["rdflib", "datetime", "json"]
}
```

---
---

### Step 6: Policy Registration for Each Federation

Each federation requires policies to control the sharing and forwarding of data. The following policies allow federations to share data publicly or with specific federations. These policies should be registered using the **Create Publish Policy** endpoint in the **Policy Management** section of each federation's API.

#### Federation 1

**Register Policy:**

```json
{
  "policy_ID": "Policy1",
  "name": "Policy1",
  "description": "This policy allows sharing and forwarding data publicly.",
  "permittedContextTypes": ["community", "federation", "policies", "functions", "datamodels"],
  "sharingRules": [
    {"federation": "Federation2", "canReceive": true, "canForward": true},
    {"federation": "public", "canReceive": true, "canForward": true}
  ],
  "modifiedBy": "",
  "Geographic_Restrictions": []
}
```

#### Federation 2

**Register Policy:**

```json
{
  "policy_ID": "Policy2",
  "name": "Policy2",
  "description": "This policy allows sharing and forwarding data publicly.",
  "permittedContextTypes": ["community", "federation", "policies", "functions", "datamodels"],
  "sharingRules": [
    {"federation": "public", "canReceive": true, "canForward": true}
  ],
  "modifiedBy": "",
  "Geographic_Restrictions": []
}
```

#### Federation 3

**Register Policy:**

```json
{
  "policy_ID": "Policy3",
  "name": "Policy3",
  "description": "This policy allows sharing and forwarding data publicly.",
  "permittedContextTypes": ["community", "federation", "policies", "functions", "datamodels"],
  "sharingRules": [
    {"federation": "public", "canReceive": true, "canForward": true}
  ],
  "modifiedBy": "",
  "Geographic_Restrictions": []
}
```

#### Federation 4

**Register Policy:**

```json
{
  "policy_ID": "Policy4",
  "name": "Policy4",
  "description": "This policy allows sharing and forwarding data publicly.",
  "permittedContextTypes": ["community", "federation", "policies", "functions", "datamodels"],
  "sharingRules": [
    {"federation": "public", "canReceive": true, "canForward": true}
  ],
  "modifiedBy": "",
  "Geographic_Restrictions": []
}
```

---

### Step 7: Collaboration Initiation Between Federations

Collaboration initiation allows federations to exchange data and context. The following instructions outline how to initiate collaboration requests between federations using the **Initiate Collaboration** endpoint in the API documentation.

#### Federation 1 → Federation 2

**Request Body:**

```json
{
  "destination_broker": "localhost",
  "destination_port": 1885,
  "receiver_Fed_ID": "Federation2",
  "details": "Federation1 sends Collaboration Request to Federation2",
  "policy_ID": "Policy1"
}
```

#### Federation 2 → Federation 3

**Request Body:**

```json
{
  "destination_broker": "localhost",
  "destination_port": 1886,
  "receiver_Fed_ID": "Federation3",
  "details": "Federation2 sends Collaboration Request to Federation3",
  "policy_ID": "Policy2"
}
```

#### Federation 3 → Federation 4

**Request Body:**

```json
{
  "destination_broker": "localhost",
  "destination_port": 1887,
  "receiver_Fed_ID": "Federation4",
  "details": "Federation3 sends Collaboration Request to Federation4",
  "policy_ID": "Policy3"
}
```
#### Federation 1 → Federation 4

**Request Body:**

```json
{
  "destination_broker": "localhost",
  "destination_port": 1887,
  "receiver_Fed_ID": "Federation4",
  "details": "Federation1 sends Collaboration Request to Federation4",
  "policy_ID": "Policy1"
}
```
---

### Step 8: Manual Context Exchange (Fallback)

Due to a recent critical bug, a **manual context exchange** is required for interactions to work correctly. Follow these steps to perform the manual context exchange:

1. In **Federation 1's `app.py`**, use the **Context Exchange After Collaboration** endpoint.

2. Specify **"Federation2"** as the target for context exchange and run the endpoint.

This will initiate a context exchange between **Federation 1** and **Federation 2** using the target federation's ID. The exchange respects the data exchange policy, so if the policy does not allow it, the exchange will fail.

For the rest (to make sure you can "play" with a fully connected network of federations):

1. In Federation 1's app.py, use the Context Exchange After Collaboration endpoint with "Federation2" as the target.

2. In Federation 2's app.py, run the endpoint with "Federation1" as the target, then run it again with "Federation3" as the target.

3. In Federation 3's app.py, run the endpoint with "Federation2" as the target, then run it again with "Federation4" as the target.

4. In Federation 4's app.py, run the endpoint with "Federation3" as the target
---

## Data Interaction Between Communities Experiments

In this section, you will follow the outlined steps to reproduce the experiments measuring latency during data exchange between communities. Pre-configured experiments are provided for your convenience.

### Step 1: Set Up Community1 Endpoint

1. **Open a new terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Communities/community1_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```
   
### Step 2: Set Up Community2 Endpoint

1. **Open a terminal** and navigate to the `community2_endpoint` folder:

   ```bash
   cd Communities/community2_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```
### Step 3: Set Up Community3 Endpoint

1. **Open a terminal** and navigate to the `community2_endpoint` folder:

   ```bash
   cd Communities/community3_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```  
### Step 4: Set Up Community4 Endpoint

1. **Open a terminal** and navigate to the `community2_endpoint` folder:

   ```bash
   cd Communities/community4_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```
# Expeiment A: Interaction Latency: Startup Latency and Ongoing Interaction Latency.  
## Overview
This experiment evaluates the data exchange process between Community X and Community Y **within CCDUIT** and **without CCDUIT**, specifically measuring the delay an iteration takes from the moment Community X requests data from Community Y until Community X successfully receives it. The evaluation is conducted across **two phases**:

1. **Startup Delay Measurement**: The delay of the first iteration over 20 runs.
2. **Steady-State Interaction**: Data exchange performance in subsequent iterations, executed over 5 runs, with each run comprising approximately 100 iterations.

## Expected Output
- A box plot illustrating the **startup delay** over 20 runs.
- A box plot visualizing the **ongoing interaction delay** over 5 runs.
- 
### Experiment 1: Interaction Between Community 1 and Community 2 within CCDUIT
This experiment demonstrates the interaction between Community 1 and Community 2. Here’s how the data flow works:
- **Community 2** generates synthetic occupancy data in **JSON format** and transmits it via **HTTP protocol**.
- **Community 1** retrieves this data using **CCDUIT** and receives it in **TTL format** over the **MQTT protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_brick within ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_brick within ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
### Experiment 2: Interaction Between Community 2 and Community 1 within CCDUIT
This experiment demonstrates the interaction between Community 2 and Community 1. Here’s how the data flow works:
- **Community 1** generates synthetic occupancy data in **TTL format** and transmits it via **MQTT protocol**.
- **Community 2** retrieves this data using **CCDUIT** and receives it in **JSON format** over the **HTTP protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_ngsild within ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_ngsild within ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```

### Experiment 3: Interaction Between Community 2 and Community 3 within CCDUIT
This experiment demonstrates the interaction between Community 2 and Community 3. Here’s how the data flow works:
- **Community 2** generates synthetic occupancy data in **JSON format** and transmits it via **HTTP protocol**.
- **Community 3** retrieves this data using **CCDUIT** and receives it in **JSON format** over the **HTTP protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_ngsild within ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_ngsild within ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```

### Experiment 4: Interaction Between Community 4 and Community 1 within CCDUIT
This experiment demonstrates the interaction between Community 4 and Community 1. Here’s how the data flow works:
- **Community 1** generates synthetic occupancy data in **TTL format** and transmits it via **MQTT protocol**.
- **Community 4** retrieves this data using **CCDUIT** and receives it in **TTL format** over the **MQTT protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_brick within ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_brick within ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
### Experiment 5: Interaction Between Community 2 and Community 3 without CCDUIT
This experiment demonstrates the interaction between Community 2 and Community 3. Here’s how the data flow works:
- **Community 2** generates synthetic occupancy data in **JSON format** and transmits it via **HTTP protocol**.
- **Community 3** retrieves this data using **CCDUIT** and receives it in **JSON format** over the **HTTP protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_ngsild without ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_ngsild without ccduit/the script
   ```
   2. **Run the script**

   ```bash
   python3 script.py
   ```
### Experiment 6: Interaction Between Community 4 and Community 1 without CCDUIT
This experiment demonstrates the interaction between Community 4 and Community 1. Here’s how the data flow works:
- **Community 1** generates synthetic occupancy data in **TTL format** and transmits it via **MQTT protocol**.
- **Community 4** retrieves this data using **CCDUIT** and receives it in **TTL format** over the **MQTT protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_brick without ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_brick without ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
# Expeiment B: Adaptation Experiment  
### Experiment 1: First Adaptation Experiment  

## Overview
This experiment aims to evaluate the response time of CCDUIT to policy changes. Specifically, if an ongoing data interaction is no longer permitted due to an updated policy, CCDUIT should detect the change and promptly terminate the interaction.

## Execution Process
The experiment will be conducted over 100 runs, with each run lasting approximately 9 seconds.

## Expected Output
- A box plot illustrating the **response delay** over 100 runs.
- 
### How to Run

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_brick within ccduit/first_adaptation_experiment
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
### Experiment 2: Second Adaptation Experiment  

## Overview
In this experiment, we have a linear collaboration between federations. Specifically, Federation1 will update its policy, and we will measure how fast CCDUIT propagates this policy update to:
**Federation2**
**Federation3**
**Federation4**
The goal is to analyze the propagation delay of policy updates across federations and evaluate CCDUIT’s responsiveness.

## Running the Second Adaptation Experiment

We include instructions and a premade setup to **easily and quickly recreate the second adaptation experiment** described in the paper. More pre-configured experiments will be added over time. It should be fairly simple to navigate to the appropriate location in the code to add timers (e.g., at the start of a data request) for the rest of the experiments.

### Experiment Steps

1. **Stop All Previous Terminals:**

   Ensure all previously running terminals are stopped (including any rogue zombie processes). Also make sure to terminate any containers still running (to start from a clean-slate)
  
  ```bash
   docker stop $(docker ps -q) && docker rm $(docker ps -aq)
   ```


2. **Navigate to the Experiment Folder:**

   ```bash
   cd Experiments/Second Adaptation Experiment
   ```

3. **Run Experiment Configuration:**

   The configuration script sets up federations and their interactions needed automatically for the experiment (so you don't have to do the previous steps again):

   ```bash
   python3 Experiment_config.py
   ```

4. **Clean the Results Folder:**
  Make sure to remove all .txt files present in the Results folder. You can do so manually or by something like :
   ```bash
   cd Results
   rm -f *.txt
   ```

5. **Update the Policy:**

   In the **Federation 1** folder, run the `update_policy.py` script to execute **100 iterations** of policy updates:

   ```bash
   python3 update_policy.py
   ```

6. **Generate Results:**

   After completing the iterations, compile the results into an **Excel file**:

   ```bash
   python3 Generate_excel.py
   ```

9. **Visualize Results:**

   Analyze and visualize the outcomes:

   ```bash
   python3 show_result.py
   ```

### Expected Results

- **`network_delays.xlsx`**: Contains detailed delay data.
- **`response_time_boxplots.png`**: Visual representation of response times.
