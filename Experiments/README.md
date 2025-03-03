# Experiments 
In this section, you will find detailed, step-by-step instructions to reproduce all the experiments. For each experiment, we provide a photograph of the results for verification purposes. This folder contains the complete set of experimental setups. To ensure accurate reproduction, we strongly recommend following the steps outlined in the [main guide](https://github.com/satrai-lab/ccduit/) to configure the federations and their respective contexts, as our experiments assume that the collaborative network between federations is already established.

---
# Table of Contents

1. [Set Up Communities](#set-up-communities)
   - [Community 1 Endpoint](#set-up-community1-endpoint)
   - [Community 2 Endpoint](#set-up-community2-endpoint)
   - [Community 3 Endpoint](#set-up-community3-endpoint)
   - [Community 4 Endpoint](#set-up-community4-endpoint)

2. [Experiment A: Interaction Latency](#experiment-a-interaction-latency)
   - [Overview](#overview)
   - [Expected Output](#expected-output)
   - **Experiment 1: Community 1 and Community 2 within CCDUIT**
     - [Startup Delay Output](#startup-delay-output)
     - [Ongoing Interaction Output](#ongoing-interaction-output)
     - [How to Run](#how-to-run)
   - **Experiment 2: Community 2 and Community 1 within CCDUIT**
     - [Startup Delay Output](#startup-delay-output-1)
     - [Ongoing Interaction Output](#ongoing-interaction-output-1)
     - [How to Run](#how-to-run-1)
   - **Experiment 3: Community 2 and Community 3 within CCDUIT**
     - [Startup Delay Output](#startup-delay-output-2)
     - [Ongoing Interaction Output](#ongoing-interaction-output-2)
     - [How to Run](#how-to-run-2)
   - **Experiment 4: Community 4 and Community 1 within CCDUIT**
     - [Startup Delay Output](#startup-delay-output-3)
     - [Ongoing Interaction Output](#ongoing-interaction-output-3)
     - [How to Run](#how-to-run-3)
   - **Experiment 5: Community 2 and Community 3 without CCDUIT**
     - [Startup Delay Output](#startup-delay-output-4)
     - [Ongoing Interaction Output](#ongoing-interaction-output-4)
     - [How to Run](#how-to-run-4)
   - **Experiment 6: Community 4 and Community 1 without CCDUIT**
     - [Startup Delay Output](#startup-delay-output-5)
     - [Ongoing Interaction Output](#ongoing-interaction-output-5)
     - [How to Run](#how-to-run-5)

3. [Experiment B: Adaptation Experiment](#experiment-b-adaptation-experiment)
   - **Experiment 1: First Adaptation Experiment**
     - [Overview](#overview-1)
     - [Expected Output](#expected-output-1)
     - [Response Delay Output](#response-delay-output)
     - [How to Run](#how-to-run-6)
   - **Experiment 2: Second Adaptation Experiment**
     - [Overview](#overview-2)
     - [Experiment Steps](#experiment-steps)
     - [Expected Results](#expected-results)
     - [Response Delay Output](#response-delay-output-1)

---

# Set Up Communities

Before running the experiments, ensure that all community containers are properly configured. To do this, navigate to the `Communities` folder and set up each community individually. This step is crucial for a smooth execution of the experiments.
move the `Communities` folder:

   ```bash
   cd ../Communities
   ```

## Set Up Community1 Endpoint

1. **Open another terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Coomunities/community1_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```
   
## Set Up Community2 Endpoint

1. **Open another terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Coomunities/community2_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```

## Set Up Community3 Endpoint

1. **Open another terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Coomunities/community3_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```
   
 ## Set Up Community4 Endpoint

1. **Open another terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Coomunities/community4_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```

# Experiment A: Interaction Latency: Startup Latency and Ongoing Interaction Latency.  
## Overview
This experiment evaluates the data exchange process between Community X and Community Y **within CCDUIT** and **without CCDUIT**, specifically measuring the delay that an iteration takes from the moment Community X requests data from Community Y until Community X successfully receives it. The evaluation is conducted across **two phases**:

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

### Startup Delay Output

![Startup Delay Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/ngsild-brick-startup.png)

### Ongoing Interaction Output

![Ongoing Interaction Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/ngsild-brick.png)

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

### Startup Delay Output

![Startup Delay Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/brick-ngsild-startup.png)

### Ongoing Interaction Output

![Ongoing Interaction Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/brick-ngsild-within-ccduit.png)

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

### Startup Delay Output

![Startup Delay Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/ngsild-ngsild-within-ccduit-startup.png)

### Ongoing Interaction Output

![Ongoing Interaction Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/nsild-ngsild-within-ccduit.png)

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
> [!NOTE]  
> **In this experiment, we need to establish collaboration between **Federation1** and **Federation4** to enable data interaction.**  
> **Federation 1 → Federation 4**
>
> **Request Body:**
>
> ```json
> {
>  "destination_broker": "localhost",
>  "destination_port": 1887,
>  "receiver_Fed_ID": "Federation4",
>  "details": "Federation1 sends Collaboration Request to Federation4",
>  "policy_ID": "Policy1"
> }
> ```
### Startup Delay Output

![Startup Delay Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/brick-brick-startup.png)

### Ongoing Interaction Output

![Ongoing Interaction Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/brick-brick_next_iterations.png)

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

### Startup Delay Output

![Startup Delay Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/ngsild-ngsild-without-ccduit-startup.png)

### Ongoing Interaction Output

![Ongoing Interaction Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/ngsild-nsgild-without-ccduit.png)

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

### Startup Delay Output

![Startup Delay Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/brick-brick-without-ccduit.png)

### Ongoing Interaction Output

![Ongoing Interaction Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/brick-brick-without ccduit.png)

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

> [!NOTE]  
> For this experiment, we recommend setting all policies to publicly allow sharing.

## Execution Process
The experiment will be conducted over 100 runs, with each run lasting approximately 9 seconds.

## Expected Output
- A box plot illustrating the **response delay** over 100 runs.
  
### Response Delay Output

![Startup Delay Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/first%20adaptation.png).
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
- 
### Response Delay Output
![Startup Delay Box Plot](https://github.com/satrai-lab/ccduit/blob/CCDUIT_Experiments/Experiments/Images/response_time_boxplots.png)

